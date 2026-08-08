# P1-007: Add PR template with task/phase/capability/evidence fields

**Phase**: Phase 1
**Status**: Completed
**Dependencies**: none
**Complexity**: S
**Related ADRs**: 0015

## Current Evidence

- `.github/PULL_REQUEST_TEMPLATE.md` exists with full content.
- Template includes: task ID, phase, branch, AC checklist, evidence section
  (handoff, ATDD, coverage audit, session handout), review stack checklist,
  rollback strategy.
- References the maestro framework templates and conventions.
- PR #3 (merged).

## Description

Add a pull-request template carrying task, phase, capability, and evidence fields.
Standardizes the evidence and review documentation in every PR.

## Acceptance Criteria

- [x] PR template at `.github/PULL_REQUEST_TEMPLATE.md` exists.
- [x] Template includes: task ID, phase, branch, AC checklist, evidence, review stack.
- [x] Template is active — new PRs show the template content.

## Known Debt

- Template could be further aligned with `maestro-templates/pr.md` v2 format
  (musician agent names, Bernstein references). Non-blocking.

## References

- Template: `.github/PULL_REQUEST_TEMPLATE.md`
- Framework template: `maestro-templates/pr.md`
- ADRs: 0015

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| 2026-08-06 | Completed | — | PR #3 | — |
