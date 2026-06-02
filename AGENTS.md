# Agent Instructions

This repository is a proof of concept for an RFC workflow based on Markdown,
GitHub pull requests, GitHub Reviews, and future Backstage indexing.

## Mission

Keep the POC focused on validating whether engineering RFCs can be easier to
write, review, approve, and index when they follow a predictable Markdown
structure.

Do not turn this into a full documentation platform or custom editor.

## Core decisions

- One RFC is one Markdown file.
- Canonical path: `rfcs/<year>/<slug>/rfc.md`.
- `<slug>` is lowercase ASCII kebab-case and must not start with `rfc-`.
- One PR should create or update exactly one RFC.
- RFC branches should be named `rfc/<slug>`.
- RFC PR titles should use `RFC: <Title>`.
- YAML frontmatter is the metadata source of truth.
- GitHub PR comments are the collaboration surface.
- GitHub Review is the formal approval source.
- Backstage is the future read/index surface, not the review surface.
- `assets/` is optional.
- Pasted GitHub image attachments are allowed.

## Frontmatter contract

Minimum fields:

```yaml
---
Title: Service Boundary Example
review_status: draft
design_review: platform
comments_until:
review_until:
required_approvers: []
---
```

Allowed `review_status` values:

- `draft`
- `accepting_comments`
- `in_review`
- `closed`
- `deprecated`

Do not add new status values unless the workflow decision is intentionally
reopened.

## Approval model

Do not encode approval as an editable Markdown field.

`required_approvers` lists GitHub usernames. Approval must be proven by GitHub
Review on the PR. The PR author must not count as their own approver.

Interpret final state as:

- merged PR = accepted RFC;
- closed without merge = rejected or withdrawn RFC.

## Validation rules

The validation script is `scripts/validate_rfc.py`.

Before claiming changes are done, run:

```bash
python3 -m unittest tests/test_validate_rfc.py
python3 scripts/validate_rfc.py rfcs/2026/service-boundary-example/rfc.md
python3 -c "import ast, pathlib; ast.parse(pathlib.Path('scripts/validate_rfc.py').read_text()); print('syntax ok')"
```

Validation should:

- validate only RFCs changed in the PR;
- ignore non-RFC PRs;
- ignore unrelated folders and historical noise;
- fail if more than one RFC is changed in one PR;
- validate frontmatter, path, slug, required sections, dates, and approvals;
- avoid modifying labels, PR body, files, or metadata automatically.

## Scope guardrails

Do not add these without an explicit decision:

- custom editor UI;
- bidirectional Google Docs sync;
- mandatory Backstage indexing before the workflow is validated;
- automatic PR label synchronization;
- automatic PR body edits;
- RFC numbering;
- multi-file RFCs;
- mandatory `assets/` for images;
- validation of all historical RFCs.

## Documentation

Keep `README.md`, `docs/qna.md`, `rfcs/README.md`,
`rfcs/_template/rfc.md`, and `.github/PULL_REQUEST_TEMPLATE/rfc.md` aligned
when workflow rules change.

`rfcs/README.md` explains folder convention only. It must not become a manual
index. Backstage should own index/status presentation.
