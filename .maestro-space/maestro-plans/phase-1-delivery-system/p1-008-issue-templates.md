# P1-008: Add issue and milestone templates

**Phase**: Phase 1
**Status**: In Development
**Dependencies**: none
**Complexity**: S
**Related ADRs**: 0015

## Current Evidence

- `.github/ISSUE_TEMPLATE/` exists with: `bug_report.yml`, `feature_request.yml`, `config.yml`.
- These are GitHub-standard templates.
- Maestro-specific templates from `maestro-templates/` (issue-deferred.md,
  issue-tech-debt.md, issue-secops.md) have NOT been added yet.

## Description

Add issue templates aligned with the phase/capability model. Provides structured
intake for phase planning and audit tracking using the maestro tag nomenclature.

## Acceptance Criteria

- [x] GitHub-standard issue templates exist (bug_report, feature_request).
- [ ] Maestro-specific templates added: deferred, tech-debt, secops
  (from `maestro-templates/issue-*.md`).
- [ ] Issue templates reference tag nomenclature from `maestro-conventions.md` §3.

## Remaining Work

1. Create `deferred.yml`, `tech-debt.yml`, `secops.yml` in `.github/ISSUE_TEMPLATE/`
   based on the templates in `maestro-templates/issue-*.md`.
2. Update `config.yml` to include the new templates.

## References

- Templates: `maestro-templates/issue-deferred.md`, `issue-tech-debt.md`, `issue-secops.md`
- Conventions: `maestro-conventions.md` §3
- Existing: `.github/ISSUE_TEMPLATE/`
- ADRs: 0015

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| 2026-08-06 | In Development | — | PR #3 | — |
