---
Title: Service Boundary Example
review_status: draft
design_review:
comments_until:
review_until:
required_approvers:
  - 1001Josias
---

# Service Boundary Example

## Overview

This example RFC demonstrates the proposed Markdown workflow. It is intentionally
small and exists to validate the repository structure, frontmatter, rendering,
and pull request review mechanics.

The real proposal would describe how two services should define a clearer
boundary, including ownership, contracts, rollout, and operational impact.

## Goals & Non-Goals

### Goals

- Demonstrate a single-file RFC structure.
- Demonstrate YAML frontmatter for automation and indexing.
- Demonstrate GitHub PR review as the approval mechanism.

### Non-Goals

- Define a real production service boundary.
- Replace existing documentation tools globally.
- Build a custom editor UI.

## Background & Motivation

RFC authors should be able to focus on the technical idea instead of formatting
or designing the document. A Markdown template gives the document a predictable
shape while keeping authoring lightweight.

This example uses the same concepts as the proposed RFC process: status, design
review area, comment deadline, review deadline, and approvers.

## Detailed Proposal

Each RFC lives at `rfcs/<year>/<slug>/rfc.md`.

The frontmatter is the source of truth for automation:

```yaml
Title: Service Boundary Example
review_status: draft
design_review:
comments_until:
review_until:
required_approvers:
  - 1001Josias
```

The body stays normal Markdown. Authors can paste images directly into GitHub or
store files under `assets/` when versioned assets are useful.

## Alternatives Considered & Prior Art

- **Unstructured documents**: keeps authoring flexible, but makes status and
  approvals harder to validate.
- **Custom app**: could provide a tailored UI, but is too much investment before
  validating the workflow.
- **Multi-file RFCs**: can improve review granularity, but add friction for the
  first version.

## Risks

- **Review friction**: GitHub PR comments may be less comfortable than document
  comments. This must be validated with authors and reviewers.
- **Template bureaucracy**: too many required sections may make RFC writing feel
  heavier. The first version should keep a small required core.
- **Approval confusion**: authors may expect Markdown fields to prove approval.
  The workflow must make clear that GitHub Review is the approval source.

## Revisions

| Date | Description |
|------|-------------|
| 2026-06-02 | Created example RFC |
