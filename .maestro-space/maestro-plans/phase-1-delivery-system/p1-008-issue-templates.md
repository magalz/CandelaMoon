# P1-008: Add issue and milestone templates

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: none
**Complexity**: S
**Related ADRs**: 0015

## Description

Add issue and milestone templates aligned with the phase/capability model.
Provides structured intake for phase planning and audit tracking.

## Acceptance Criteria

- Issue templates for: deferred, tech-debt, and secops issues exist.
- Milestone naming convention documented.
- Issue templates reference the tag nomenclature from `maestro-conventions.md`.

## Implementation Plan

1. Read the issue templates from `maestro-templates/issue-*.md`.
2. Create `.github/ISSUE_TEMPLATE/` directory with template files.
3. Create `.github/ISSUE_TEMPLATE/config.yml` if needed.

## Evidence Requirements

- Template files committed.
- New issue creation shows the templates as options.

## Known Risks

- None.

## References

- Templates: `maestro-templates/issue-deferred.md`, `issue-tech-debt.md`, `issue-secops.md`
- Conventions: `maestro-conventions.md` §3
- ADRs: 0015

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
