# RFC Workflow Proposal: Decisions in Q&A Format

## 1. What problem are we trying to solve?

We are trying to make RFC authors focus on the idea, decision, trade-offs, and technical proposal, instead of spending energy on document design and formatting.

The core goal is not "move from Google Docs to Markdown". The core goal is to standardize RFC structure with the minimum necessary process so the content becomes easier to write, review, search, validate, and consume.

## 2. Is this already a pilot proposal?

No.

This is a discovery proposal. The goal is to validate whether the demand exists and identify blockers before proposing a pilot.

## 3. What should be validated with engineering first?

The first validation should answer:

- Does this pain exist for engineers who write and review RFCs?
- Does the current Google Docs flow create friction around structure, formatting, consistency, or approval?
- Would reviewing RFCs through GitHub PRs be acceptable for engineering RFCs?
- What parts of Google Docs must not be lost?
- What blockers would make this workflow unviable?
- Which future RFCs would be good candidates for a small pilot?

## 4. What is the main framing?

This is a workflow hypothesis, not a migration plan.

Main question:

> Can we keep RFC authoring simple while making structure, history, approval, and publication more consistent?

## 5. What is the strongest expected objection?

Collaboration.

Google Docs is extremely good for easy comments, real-time editing, suggestions, and low-friction participation. The proposal must acknowledge this directly.

Working answer:

> Google Docs is better for free-form collaboration. The question is whether, for engineering RFCs, GitHub PR comments are good enough in exchange for better structure, history, review traceability, and automation. If collaboration gets materially worse, the workflow should not be forced.

## 6. Are RFCs mostly engineering documents today?

Current observation from the Drive folder is that RFCs appear to be mostly engineering documents.

This matters because the workflow can be evaluated first against the actual audience. If an RFC needs heavy Product, Design, Legal, or external participation, it may need a different path or extra support.

## 7. Should the first future pilot be mandatory?

No.

If a pilot happens later, it should start with voluntary new RFCs only. It should not migrate legacy RFCs and should not force all teams into the workflow immediately.

## 8. Should legacy Google Docs RFCs be migrated?

No, not initially.

Legacy migration is not part of the initial scope. Migrating old documents before validating the workflow adds effort and risk without proving whether the new flow works.

## 9. Should Markdown be considered the final user experience?

No.

Markdown is the source format and automation contract. The user experience can be GitHub, Backstage, or another UI later.

For the initial version, GitHub is sufficient for authoring, rendering, comments, and approval. Backstage can become the read/index surface.

## 10. What is the expected role of Backstage?

Backstage should be treated as the read, index, and discovery surface, not the collaboration surface.

GitHub remains responsible for:

- authoring in the repo;
- PR discussion;
- inline comments;
- review approvals;
- final merge/close decision.

Backstage can later provide:

- RFC list;
- filtering by year, status, design review, approvers;
- friendly rendering;
- links back to GitHub PRs;
- possibly draft creation or editing in the future.

## 11. Why not use Backstage for PR comments?

Because GitHub PRs already own inline review comments, approvals, and merge/close semantics.

Backstage can help with reading and discovery, but replacing GitHub PR review would add complexity and weaken the audit trail.

## 12. What is the proposed folder structure?

The proposed structure is:

```txt
rfcs/
  README.md
  _template/
    rfc.md
    assets/
      .gitkeep
  2026/
    service-boundary-example/
      rfc.md
      assets/
        optional-image.png
```

The canonical RFC path is:

```txt
rfcs/<year>/<slug>/rfc.md
```

## 13. Why use a folder per RFC instead of a single file?

A folder per RFC keeps the main RFC as a single Markdown file while leaving a natural place for optional assets.

This avoids future cleanup if a document needs images, diagrams, or supporting files.

## 14. Should each RFC be one Markdown file?

Yes.

The pilot-style design should use a single `rfc.md` per RFC. Multi-file RFCs add authoring and navigation friction too early.

The template can remain rich, but the document should be one file.

## 15. How should RFC folders be named?

RFC folders should be slugs derived from the title:

- lowercase;
- ASCII;
- kebab-case;
- separated by dashes;
- no spaces;
- no accents;
- no `rfc-` prefix;
- no number required initially.

Good examples:

```txt
rfcs/2026/service-boundary-example/rfc.md
rfcs/2026/iam-authoritative-source/rfc.md
rfcs/2026/one-app-experience/rfc.md
```

Bad examples:

```txt
rfcs/2026/rfc-service-boundary-example/rfc.md
rfcs/2026/Service Boundary Example/rfc.md
rfcs/2026/iam_authoritative_source/rfc.md
rfcs/2026/001-service-boundary-example/rfc.md
```

## 15a. What naming convention should RFC branches and PR titles use?

RFC branches should use:

```txt
rfc/<slug>
```

Example:

```txt
rfc/service-boundary-example
```

RFC PR titles should use:

```txt
RFC: Service Boundary Example
```

Prefer `RFC: <Title>` over `(rfc): <title>`. The `RFC:` prefix is easier to scan in GitHub PR lists and avoids mixing RFC workflow with commit-message conventions.

## 16. Should RFCs be numbered?

Not initially.

Numbering adds coordination: reservation, sequencing, abandoned numbers, and migration questions. Year plus slug is enough for the first version.

## 17. Should unrelated folders or old files break validation?

No.

Automation should only consider files that match:

```txt
rfcs/<year>/<slug>/rfc.md
```

Unrelated folders, test folders, backups, or historical noise should be ignored.

## 18. What should `rfcs/README.md` do?

It should explain the workflow. It should not be a manual RFC index and should not parse or duplicate frontmatter metadata.

It should document:

- how to create an RFC;
- folder structure;
- required frontmatter;
- review lifecycle;
- how comments and approvals work;
- how images work;
- how GitHub and Backstage fit together.

## 19. Who should build the RFC index?

Backstage.

The README should not maintain an index manually. Backstage should consume frontmatter and render the RFC list/status view.

## 20. What should be the minimum frontmatter?

The minimum frontmatter should be:

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

When the RFC leaves draft, dates and approvers become progressively more required depending on `review_status`.

## 21. Why use frontmatter?

Frontmatter gives automation and Backstage a structured contract while keeping the RFC as a human-readable Markdown document.

It allows validation of status, dates, design review area, approvers, and required sections without requiring a custom app.

## 22. Why not use a separate YAML or JSON file?

For the initial version, a separate metadata file creates more moving parts and can drift from the RFC.

The preferred model is:

- one `rfc.md`;
- frontmatter at the top;
- content below.

This keeps the source of truth together.

## 23. Why YAML instead of JSON?

YAML frontmatter is more natural in Markdown documents and is widely supported by static site generators, documentation tools, and parsers.

JSON is stricter but less pleasant for humans to edit.

## 24. Should there be a visual metadata table in the Markdown body?

Not required initially.

The frontmatter should be the canonical source of metadata. A visual table duplicates the same information and can become inconsistent.

If people miss the Google Docs-style table, a generated table can be added later.

## 25. Should current Google Docs status values be changed?

No.

The workflow should preserve the status values already used today to make conversion and mental mapping easier:

- `Draft`
- `Accepting comments`
- `In review`
- `Closed`
- `Deprecated`

In frontmatter these can be normalized as:

- `draft`
- `accepting_comments`
- `in_review`
- `closed`
- `deprecated`

Backstage can render them with friendly labels.

## 26. Who controls the RFC status?

The author controls the status.

This mirrors the current Google Docs flow, where the author sets labels/status and assumes responsibility for moving the document through the process.

Automation validates consistency but should not decide when the author is done collecting comments.

## 27. Should the author be allowed to move from `Accepting comments` to `In review`?

Yes.

The author decides when the comment window is done. `comments_until` is a process signal, not a governance mechanism that needs heavy enforcement.

## 28. What should validation enforce by `review_status`?

Validation should become stricter as the RFC progresses.

For `draft`:

- valid path;
- valid frontmatter;
- title present;
- valid `review_status`;
- basic Markdown structure.

For `accepting_comments`:

- `design_review` required;
- `comments_until` required and valid;
- minimum body sections exist.

For `in_review`:

- `review_until` required and valid;
- `required_approvers` not empty;
- PR must not be Draft;
- minimum body sections are complete enough for review.

For `closed`:

- approvals must be complete if the PR is being merged;
- merge means accepted;
- close without merge means rejected or withdrawn.

## 29. What are the minimum body sections?

The proposal should follow the existing RFC template as the starting point, but distinguish between core and expandable sections.

Core sections:

- Overview
- Goals & Non-Goals
- Background & Motivation
- Detailed Proposal
- Alternatives Considered & Prior Art
- Risks
- Revisions

Expandable sections:

- Timeline
- Dependencies
- Operations
- Observability
- Data & AI
- Security & Privacy & Compliance

## 30. Should the template be rigid?

No.

It should have a minimum required core and expandable sections.

Principle:

> We standardize the skeleton, not the reasoning.

Each RFC can have particularities, and the template should support that without becoming a form that people fill mechanically.

## 31. How should approvals work?

Approvals should come from GitHub PR reviews, not from manually editable fields in the Markdown.

The frontmatter lists required GitHub users:

```yaml
required_approvers:
  - 1001Josias
```

The GitHub PR review proves who approved, when they approved, and which version they approved.

## 32. Why not let the author mark approvers as approved in the Markdown?

Because that repeats a weakness of Google Docs: anyone with edit access can change the label or approval table.

GitHub Review is a better approval source because it is tied to identity, timestamp, commit, and PR state.

Approval rule:

> The author controls the process status, but approvers prove approval through GitHub Review.

## 33. Should `required_approvers` be GitHub users?

Yes.

For the initial version, required approvers should be GitHub usernames, not teams or abstract areas. This makes validation simpler and auditability clearer.

Teams can be considered later if needed.

## 34. Can the PR author count as an approver?

No.

The author should not satisfy their own required approval.

## 35. What happens if new commits are pushed after approvals?

The preferred behavior is that approvals should apply to the current PR HEAD.

If branch protection invalidates approvals after new commits, that should be treated as desirable. RFC approval should apply to the final version.

## 36. What does `Closed` mean?

`Closed` means the RFC review cycle is finished.

The outcome is derived from the PR:

- PR merged = RFC accepted;
- PR closed without merge = RFC rejected or withdrawn.

This avoids adding a separate `final_decision` field in the first version.

## 37. How do we distinguish rejected from withdrawn?

For the first version, the distinction can be captured in the final PR comment.

If the distinction becomes important for reporting, it can later become structured metadata.

## 38. Can an accepted RFC change later?

Yes.

An accepted RFC can be updated later, but only via a new PR. Significant changes should be recorded in the `Revisions` section.

This keeps RFCs living but auditable.

## 39. Should one PR edit multiple RFCs?

No, not initially.

The first version should enforce one RFC per PR. This keeps review status, comments, approvers, and final decision unambiguous.

## 40. Should validation run on all RFCs in the repo?

No.

Validation should run only for the RFC created or modified in the PR. It should not block unrelated PRs because of existing legacy content or unrelated folders.

## 41. What if a PR does not touch an RFC?

The RFC validation should exit successfully without doing anything.

It should not affect normal PRs in the repository.

## 42. Should GitHub labels be automatically synchronized with frontmatter?

No.

For the initial version, automation should only validate. It should not create labels, edit PRs, change statuses, or synchronize metadata.

Labels can be used manually for filtering, but they are not part of the core workflow.

## 43. What should the GitHub Action do?

The GitHub Action should validate only.

It should check:

- exactly one RFC file changed when the PR is an RFC PR;
- path matches `rfcs/<year>/<slug>/rfc.md`;
- slug is valid kebab-case;
- frontmatter is valid;
- `review_status` is allowed;
- required fields exist according to status;
- dates are valid;
- `review_until` is not before `comments_until`;
- minimum sections exist;
- required approvers are GitHub users;
- required approvers approved the PR before merge.

## 44. Should validation block merge?

Yes.

The checks should block merge for objective issues. This is the mechanism that makes the workflow more reliable than a manually editable Google Docs table.

## 45. What should be blocked?

Blocking issues:

- invalid path;
- invalid slug;
- invalid frontmatter;
- missing title;
- invalid status;
- missing fields required by current status;
- invalid dates;
- missing required sections;
- multiple RFCs in one PR;
- missing required approvals when merging.

## 46. What should not be blocked initially?

The initial checks should not block:

- pasted GitHub image attachments;
- optional `assets/` usage;
- lack of Backstage index;
- non-RFC PRs;
- unrelated old folders;
- purely subjective content quality.

## 47. What should happen with images?

Images pasted into GitHub Markdown should be allowed.

GitHub uploads them as attachments and inserts URLs such as:

```html
<img width="3438" height="1814" alt="image" src="https://github.com/user-attachments/assets/..." />
```

For internal/private repositories, these attachments follow repository access. Only people with access to the repo can view them.

Backstage image rendering still needs validation. Backstage may not be able to
access GitHub attachment URLs, and it probably will not have permission to
download private images by default.

## 48. Should `assets/` be required?

No.

`assets/` should be optional. People working locally in an IDE can use it for versioned images, Mermaid files, diagrams, or supporting material.

People using GitHub directly can paste images into the Markdown for convenience.

## 49. Why allow pasted GitHub images?

Because the purpose is to reduce friction and let authors focus on the idea.

Forcing authors to download, rename, commit, and reference every image in `assets/` recreates the formatting/document-management burden the proposal is trying to reduce.

## 50. When should `assets/` be preferred?

Use `assets/` when an image or diagram:

- must be versioned with the repo;
- must be reused outside GitHub;
- must be preserved as a controlled artifact;
- is edited locally;
- is part of a generated diagram workflow.

For screenshots or lightweight illustrations, GitHub attachments are acceptable.

For RFCs that must render reliably outside GitHub, prefer `assets/` or another
image hosting path that the rendering surface can access. The exact Backstage
approach is intentionally unresolved until the workflow is validated.

## 51. How should a new RFC be created?

Initially, by copying a template:

```txt
rfcs/_template/rfc.md
```

to:

```txt
rfcs/<year>/<slug>/rfc.md
```

Then the author fills the frontmatter, writes the RFC, opens a Draft PR, and follows the review lifecycle.

The branch should be named `rfc/<slug>` and the PR title should be `RFC: <Title>`.

## 52. Should there be a custom RFC creation tool?

Not initially.

The first version should use a template and README. A script or GitHub form can be added later if creation friction becomes a real problem.

## 53. Can GitHub provide a native PR template?

Yes.

GitHub supports PR templates. For RFCs, a specific PR template can live at:

```txt
.github/PULL_REQUEST_TEMPLATE/rfc.md
```

This is different from the RFC document template:

```txt
rfcs/_template/rfc.md
```

## 54. Should there be a default PR template for all PRs?

No, if the repository has other types of PRs.

A global `.github/PULL_REQUEST_TEMPLATE.md` would affect every PR. Since RFC validation and workflow should only apply to RFC PRs, a specific RFC PR template is safer.

## 55. Is the PR template the source of truth?

No.

The PR template is only guidance. The source of truth is:

- `rfc.md` frontmatter;
- RFC body;
- GitHub Review approvals;
- PR merge or close state.

## 56. How should comments work?

Comments during review should happen in the GitHub PR.

This includes:

- general PR comments;
- inline comments on specific lines;
- review comments;
- change requests;
- approval reviews.

This keeps discussion, changes, and decision history together.

## 57. What is lost compared to Google Docs comments?

GitHub PRs are weaker than Google Docs for real-time coauthoring, casual comments, and long-lived point comments after publication.

This is a known blocker to validate with engineering.

## 58. What is gained compared to Google Docs comments?

GitHub PRs provide:

- review tied to exact diffs;
- approval tied to identity and commit;
- full change history;
- branch protection;
- checks before merge;
- a single audit trail for discussion and decision.

## 59. Should Google Docs conversion be possible?

Yes, as a fallback path.

If Markdown is not accepted for a specific RFC or the broader process, there should be a simple Markdown-to-Google-Docs conversion route.

## 60. Should there be bidirectional sync with Google Docs?

No.

Bidirectional sync would create ambiguity and drift. There should be one source of truth at a time.

Source-of-truth rule:

> If an RFC is converted to Google Docs and the team decides to continue there, Google Docs becomes the source of truth and the Markdown version becomes historical context or a snapshot.

## 61. Is GitHub enough for reading Markdown?

Yes for the initial version.

GitHub already renders Markdown, headings, tables, links, Mermaid diagrams, and images well enough for a first workflow.

Backstage can improve discovery and rendering later.

## 62. What is the relationship between PR state and RFC state?

Suggested mapping:

- Draft PR + `review_status: draft`: author is still shaping the RFC.
- PR collecting comments + `review_status: accepting_comments`: broad feedback phase.
- Ready PR + `review_status: in_review`: formal approval phase.
- `review_status: closed` + merged PR: accepted RFC.
- `review_status: closed` + PR closed without merge: rejected or withdrawn RFC.

## 63. What is the smallest useful version of this workflow?

The smallest useful version is:

- `rfcs/<year>/<slug>/rfc.md`;
- one Markdown file per RFC;
- minimum frontmatter;
- existing RFC template adapted to core and optional sections;
- Draft PR for authoring;
- PR comments for collaboration;
- GitHub Review for approvals;
- validation Action for objective checks;
- Backstage deferred to read/index enhancement.

## 64. What is out of scope for now?

Out of scope:

- migrating legacy RFCs;
- forcing all RFCs into the new workflow;
- custom editor UI;
- automatic label synchronization;
- automatic PR editing;
- mandatory Backstage index before validation;
- bidirectional Google Docs sync;
- requiring `assets/` for every image;
- multi-file RFCs;
- numbering RFCs;
- validating unrelated folders or all historical RFCs.

## 65. What are the main blockers to validate?

Main blockers:

- loss of Google Docs-style collaboration;
- difficulty reviewing in PRs;
- image and diagram handling;
- whether engineers are comfortable editing Markdown;
- whether PR comments are enough for RFC discussions;
- whether approval via GitHub Review feels natural;
- whether the template feels helpful or bureaucratic;
- how post-acceptance changes should be handled;
- whether Backstage publication matters for adoption.

## 66. What evidence would justify a pilot?

A pilot would make sense if:

- engineering recognizes the current pain;
- the minimum structure feels useful;
- PR-based review is acceptable for at least some RFCs;
- the main blockers are solvable;
- there are volunteers willing to try the workflow later.

## 67. How should success be measured if a pilot happens later?

Potential signals:

- authors report that the template helped them focus on the idea;
- reviewers report that RFCs became easier to scan and compare;
- PR comments were sufficient for the reviewed RFCs;
- required approvals were clearer than in Google Docs;
- validation caught real issues without becoming the main friction;
- people would use the workflow again.

## 68. What is the concise proposal?

Concise version:

> This proposal evaluates whether RFCs can become more structured and easier to review through a Markdown-first workflow in the engineering docs repo. Each RFC would be a single `rfc.md` under `rfcs/<year>/<slug>/`, with minimal frontmatter for status, deadlines, design review area, and GitHub approvers. Authors would still control the RFC status, but formal approval would come from GitHub Reviews. GitHub would handle comments and review, while Backstage could later provide indexing and a friendlier read surface. This is not a migration plan; it is a way to validate demand and blockers with engineering.

## 69. What is the key trade-off?

The key trade-off is:

> Less Google Docs-style collaboration in exchange for better structure, history, approval traceability, automation, and future Backstage indexing.

The open question is whether this trade-off is acceptable for engineering RFCs.

## 70. What is the main discussion question?

Main discussion question:

> Would this workflow help us write and review RFCs with more clarity, or would the loss of Google Docs collaboration outweigh the gains in structure, history, and approval traceability?
