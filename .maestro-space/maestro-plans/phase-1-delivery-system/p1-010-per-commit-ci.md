# P1-010: Per-commit CI workflow

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: P1-001, P1-002, P1-003, P1-004, P1-005
**Complexity**: L
**Related ADRs**: 0014

## Description

Add the per-commit CI workflow running lint, format, fast tests, docs validate,
secret scan, and JaCoCo coverage upload to Codecov. Provides fast feedback on
every commit. Workflow YAML at `.github/workflows/ci.yml`.

## Acceptance Criteria

- `.github/workflows/ci.yml` triggers on every push.
- Jobs run in the appropriate container images (from P1-005).
- Lint and format checks run and fail on violations.
- Fast unit tests run and report results.
- Docs validator runs and fails on invalid docs.
- Secret scan runs and reports findings.
- JaCoCo coverage uploaded to Codecov.

## Implementation Plan

1. Read CI architecture doc and existing workflow files.
2. Create `.github/workflows/ci.yml` with per-commit trigger.
3. Configure containerized jobs using images from GHCR.
4. Add each job: lint, format, test, docs-validate, secret-scan, coverage.
5. Test with a push to verify all jobs run.

## Evidence Requirements

- Workflow run succeeds on push.
- Each job produces output in the GitHub Actions log.
- Codecov receives coverage data.

## Known Risks

- Container image pull from GHCR must work for public repos or authenticated pulls.
- Fast tests must be a subset that runs in <5 minutes.

## References

- Infra: `docs/infrastructure/ci-architecture.md`
- Images: P1-005
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
