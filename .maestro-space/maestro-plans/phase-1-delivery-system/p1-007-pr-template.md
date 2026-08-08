# P1-007: Add PR template with task/phase/capability/evidence fields

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: none
**Complexity**: S
**Related ADRs**: 0015

## Description

Add a pull-request template carrying task, phase, capability, and evidence fields.
Standardizes the evidence and review documentation in every PR. Template follows
the canonical format in `maestro-templates/pr.md`.

## Acceptance Criteria

- PR template at `.github/PULL_REQUEST_TEMPLATE.md` exists.
- Template includes: task ID, phase, branch, acceptance criteria checklist,
  evidence section, known debt section.
- Template is active — new PRs show the template content.

## Implementation Plan

1. Read the PR template from `maestro-templates/pr.md`.
2. Create `.github/PULL_REQUEST_TEMPLATE.md` with the content.
3. Verify by opening a test PR.

## Evidence Requirements

- Template file committed and pushed.
- Test PR shows the template.

## Known Risks

- Template must not be overly verbose — keep it scannable.

## References

- Template: `maestro-templates/pr.md`
- ADRs: 0015

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
