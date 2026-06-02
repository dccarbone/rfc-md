import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_rfc.py"
SPEC = importlib.util.spec_from_file_location("validate_rfc", MODULE_PATH)
validate_rfc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_rfc)


class ValidateRfcTest(unittest.TestCase):
    def test_frontmatter_uses_capitalized_title_field(self):
        body = """---
Title: RFC - IAM Authoritative Source
review_status: draft
design_review:
comments_until:
review_until:
required_approvers: []
---

# RFC - IAM Authoritative Source
"""

        data, markdown = validate_rfc.split_frontmatter(body)
        validate_rfc.validate_h1(markdown, data.get("Title"))
        approvers = validate_rfc.validate_status_requirements(data, markdown)

        self.assertEqual(approvers, [])

    def test_changed_files_from_name_status_ignores_deleted_files(self):
        output = "\n".join(
            [
                "D\trfcs/2026/old-example/rfc.md",
                "A\trfcs/2026/new-example/rfc.md",
                "M\tscripts/validate_rfc.py",
                "R100\trfcs/2026/renamed-old/rfc.md\trfcs/2026/renamed-new/rfc.md",
            ]
        )

        self.assertEqual(
            validate_rfc.changed_files_from_name_status(output),
            [
                "rfcs/2026/new-example/rfc.md",
                "scripts/validate_rfc.py",
                "rfcs/2026/renamed-new/rfc.md",
            ],
        )

    def test_ready_pr_cannot_keep_draft_review_status(self):
        with patch.object(
            validate_rfc,
            "event_payload",
            return_value={"pull_request": {"draft": False}},
        ):
            with self.assertRaisesRegex(
                validate_rfc.ValidationError,
                "draft RFC PRs must remain GitHub Draft PRs",
            ):
                validate_rfc.validate_pr_merge_gate(
                    {"review_status": "draft"},
                    [],
                )

    def test_ready_pr_can_accept_comments(self):
        with patch.object(
            validate_rfc,
            "event_payload",
            return_value={"pull_request": {"draft": False}},
        ):
            validate_rfc.validate_pr_merge_gate(
                {"review_status": "accepting_comments"},
                [],
            )

    def test_closed_rfc_cannot_remain_draft_pr(self):
        with patch.object(
            validate_rfc,
            "event_payload",
            return_value={"pull_request": {"draft": True}},
        ):
            with self.assertRaisesRegex(
                validate_rfc.ValidationError,
                "closed RFCs must be marked ready for review before merge",
            ):
                validate_rfc.validate_pr_merge_gate(
                    {"review_status": "closed"},
                    [],
                )


if __name__ == "__main__":
    unittest.main()
