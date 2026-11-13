This repo is a POC of an RFC workflow on Markdown, GitHub PRs and Reviews, with future Backstage indexing. Do not turn it into a documentation platform or custom editor.

- One RFC is one Markdown file at `rfcs/<year>/<slug>/rfc.md`; `<slug>` is lowercase ASCII kebab-case and must not start with `rfc-`.
- One PR creates or updates exactly one RFC; branch `rfc/<slug>`, title `RFC: <Title>`.
- YAML frontmatter is the metadata source of truth; do not add `review_status` values (see `ALLOWED_STATUSES` in `scripts/validate_rfc.py`) unless the workflow decision is reopened.
- GitHub PR comments are the collaboration surface; GitHub Review is the formal approval source; Backstage is a future read/index surface, not the review surface.
- Never encode approval as an editable Markdown field. `required_approvers` lists GitHub usernames; approval must be proven by GitHub Review, and the PR author does not count as their own approver.
- Merged PR = accepted RFC; closed without merge = rejected or withdrawn.
- `assets/` is optional; pasted GitHub image attachments are allowed.
- Before claiming done, run `python3 -m unittest tests/test_validate_rfc.py` and `python3 scripts/validate_rfc.py rfcs/2026/service-boundary-example/rfc.md`.
- Validation checks only the RFC changed in the PR, ignores non-RFC PRs, unrelated folders and historical RFCs, fails if a PR changes more than one RFC, and never modifies labels, PR body, files or metadata.
- Do not add without an explicit decision: custom editor UI, Google Docs sync, mandatory Backstage indexing or `assets/`, automatic PR label or body edits, RFC numbering, multi-file RFCs.
- Keep `README.md`, `docs/qna.md`, `rfcs/README.md`, `rfcs/_template/rfc.md` and `.github/PULL_REQUEST_TEMPLATE/rfc.md` aligned when workflow rules change. `rfcs/README.md` documents the folder convention only, never a manual index.
