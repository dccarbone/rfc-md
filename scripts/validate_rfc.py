#!/usr/bin/env python3
"""Validate RFC Markdown files changed in a pull request."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml


RFC_PATH_RE = re.compile(r"^rfcs/(?P<year>\d{4})/(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)/rfc\.md$")
ALLOWED_STATUSES = {"draft", "accepting_comments", "in_review", "closed", "deprecated"}
REQUIRED_SECTIONS = [
    "Overview",
    "Goals & Non-Goals",
    "Background & Motivation",
    "Detailed Proposal",
    "Alternatives Considered & Prior Art",
    "Risks",
    "Revisions",
]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
USERNAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")


class ValidationError(Exception):
    pass


def run_git(args: list[str]) -> str:
    result = subprocess.run(["git", *args], check=True, text=True, capture_output=True)
    return result.stdout.strip()


def event_payload() -> dict:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        return {}
    path = Path(event_path)
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def changed_files_from_event() -> list[str]:
    payload = event_payload()
    pull_request = payload.get("pull_request")
    if pull_request:
        base = pull_request["base"]["sha"]
        head = pull_request["head"]["sha"]
        output = run_git(["diff", "--name-only", f"{base}...{head}"])
        return [line for line in output.splitlines() if line]

    output = run_git(["ls-files"])
    return [line for line in output.splitlines() if line]


def changed_rfc_files() -> list[str]:
    files = changed_files_from_event()
    return [file for file in files if RFC_PATH_RE.match(file)]


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValidationError("missing YAML frontmatter delimited by ---")

    try:
        _, raw_frontmatter, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValidationError("invalid YAML frontmatter block") from exc

    data = yaml.safe_load(raw_frontmatter) or {}
    if not isinstance(data, dict):
        raise ValidationError("frontmatter must be a YAML object")
    return data, body


def require_field(data: dict, field: str) -> None:
    value = data.get(field)
    if value is None or value == "" or value == []:
        raise ValidationError(f"missing required field: {field}")


def validate_date(data: dict, field: str) -> None:
    value = data.get(field)
    if not isinstance(value, str) or not DATE_RE.match(value):
        raise ValidationError(f"{field} must use YYYY-MM-DD")


def validate_sections(body: str) -> None:
    headings = set(re.findall(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE))
    missing = [section for section in REQUIRED_SECTIONS if section not in headings]
    if missing:
        raise ValidationError(f"missing required sections: {', '.join(missing)}")


def validate_h1(body: str, title: str) -> None:
    match = re.search(r"^#\s+(.+?)\s*$", body, flags=re.MULTILINE)
    if not match:
        raise ValidationError("missing H1 title")
    if match.group(1).strip() != title:
        raise ValidationError("H1 title must match frontmatter title")


def validate_approvers(data: dict) -> list[str]:
    approvers = data.get("required_approvers")
    if approvers is None:
        return []
    if not isinstance(approvers, list):
        raise ValidationError("required_approvers must be a list")
    for approver in approvers:
        if not isinstance(approver, str) or not USERNAME_RE.match(approver):
            raise ValidationError(f"invalid GitHub username in required_approvers: {approver}")
    return approvers


def validate_status_requirements(data: dict, body: str) -> list[str]:
    status = data.get("review_status")
    if status not in ALLOWED_STATUSES:
        raise ValidationError(f"review_status must be one of: {', '.join(sorted(ALLOWED_STATUSES))}")

    require_field(data, "Title")
    if not isinstance(data["Title"], str):
        raise ValidationError("Title must be a string")

    approvers = validate_approvers(data)

    if status in {"accepting_comments", "in_review", "closed", "deprecated"}:
        require_field(data, "design_review")
        validate_date(data, "comments_until")
        validate_sections(body)

    if status in {"in_review", "closed"}:
        validate_date(data, "review_until")
        if not approvers:
            raise ValidationError("required_approvers must not be empty for in_review or closed RFCs")

    comments_until = data.get("comments_until")
    review_until = data.get("review_until")
    if comments_until and review_until and str(review_until) < str(comments_until):
        raise ValidationError("review_until must not be before comments_until")

    return approvers


def github_request(path: str) -> dict | list:
    token = os.environ.get("GITHUB_TOKEN")
    repository = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repository:
        raise ValidationError("cannot validate approvals outside GitHub Actions")

    request = urllib.request.Request(
        f"https://api.github.com/repos/{repository}{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise ValidationError(f"GitHub API request failed: {exc}") from exc


def validate_github_approvals(required_approvers: list[str]) -> None:
    payload = event_payload()
    pull_request = payload.get("pull_request")
    if not pull_request:
        print("Skipping approval validation outside pull_request event")
        return

    if not required_approvers:
        return

    pr_number = pull_request["number"]
    author = pull_request["user"]["login"].lower()
    reviews = github_request(f"/pulls/{pr_number}/reviews?per_page=100")

    latest_state_by_user: dict[str, str] = {}
    for review in reviews:
        user = review.get("user") or {}
        login = (user.get("login") or "").lower()
        state = review.get("state")
        if login and state:
            latest_state_by_user[login] = state

    missing = []
    for approver in required_approvers:
        normalized = approver.lower()
        if normalized == author:
            missing.append(f"{approver} (PR author cannot approve their own RFC)")
            continue
        if latest_state_by_user.get(normalized) != "APPROVED":
            missing.append(approver)

    if missing:
        raise ValidationError(f"missing required GitHub approvals: {', '.join(missing)}")


def validate_file(path: str) -> list[str]:
    match = RFC_PATH_RE.match(path)
    if not match:
        raise ValidationError(f"invalid RFC path: {path}")

    year = match.group("year")
    slug = match.group("slug")
    if int(year) < 2010:
        raise ValidationError("RFC year looks invalid")
    if slug.startswith("rfc-"):
        raise ValidationError("RFC slug must not start with rfc-")

    text = Path(path).read_text()
    data, body = split_frontmatter(text)
    title = data.get("Title")
    validate_h1(body, title)
    return validate_status_requirements(data, body)


def validate_pr_merge_gate(data: dict, required_approvers: list[str]) -> None:
    payload = event_payload()
    pull_request = payload.get("pull_request")
    if not pull_request:
        return

    status = data.get("review_status")
    is_draft_pr = pull_request.get("draft", False)

    if is_draft_pr and status == "draft":
        return

    if status != "closed":
        raise ValidationError(
            "non-draft RFC PRs are not merge-ready until review_status is closed"
        )

    if is_draft_pr:
        raise ValidationError("closed RFCs must be marked ready for review before merge")

    validate_github_approvals(required_approvers)


def main() -> int:
    rfc_files = sys.argv[1:] if len(sys.argv) > 1 else changed_rfc_files()
    if not rfc_files:
        print("No changed RFC files found; skipping RFC validation")
        return 0

    if len(rfc_files) > 1:
        print("RFC validation failed: one PR must change exactly one RFC")
        for path in rfc_files:
            print(f"- {path}")
        return 1

    path = rfc_files[0]
    try:
        required_approvers = validate_file(path)
        data, _ = split_frontmatter(Path(path).read_text())
        validate_pr_merge_gate(data, required_approvers)
    except ValidationError as exc:
        print(f"RFC validation failed for {path}: {exc}")
        return 1

    print(f"RFC validation passed for {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
