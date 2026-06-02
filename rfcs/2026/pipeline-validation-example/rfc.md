---
Title: Pipeline Validation Example
review_status: draft
design_review:
comments_until:
review_until:
required_approvers:
  - 1001Josias
---

# Pipeline Validation Example

## Overview

This RFC validates the pull request checks for a new RFC file after the workflow
bootstrap has been merged. It is intentionally small and should not be treated
as a real technical proposal.

## Goals & Non-Goals

### Goals

- Confirm that a PR adding one RFC triggers the RFC validation workflow.
- Confirm that the validator accepts a draft RFC in a draft pull request.
- Confirm that the workflow evaluates only the RFC changed in this PR.

### Non-Goals

- Propose a production architecture change.
- Change the RFC workflow rules.
- Add or modify validation code.

## Background & Motivation

The repository needs one isolated PR that exercises the validation pipeline
after the initial workflow files exist on `main`. This keeps the bootstrap work
separate from the pipeline validation test.

## Detailed Proposal

Add this draft RFC at `rfcs/2026/pipeline-validation-example/rfc.md`.

The expected result is that the GitHub Action runs `scripts/validate_rfc.py`,
detects this single RFC, and passes validation while the PR remains a GitHub
Draft PR.

## Alternatives Considered & Prior Art

- **Reuse the bootstrap PR**: that proves the workflow can run, but it mixes
  workflow creation with workflow validation.
- **Modify the example RFC**: that avoids another file, but it does not test the
  new-RFC creation path independently.

## Risks

- **Temporary repository noise**: this RFC exists only to validate automation.
  It should be removed or closed after the pipeline test.

## Revisions

| Date | Description |
|------|-------------|
| 2026-06-02 | Created pipeline validation RFC |
