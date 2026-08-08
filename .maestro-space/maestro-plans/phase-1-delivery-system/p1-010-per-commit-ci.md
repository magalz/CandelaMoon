# P1-010: Per-commit CI workflow

**Phase**: Phase 1
**Status**: In Development
**Dependencies**: P1-001, P1-002, P1-003, P1-004, P1-005
**Complexity**: L
**Related ADRs**: 0014

## Current Evidence

- `.github/workflows/ci.yml` exists (52 lines).
- Triggers on push to `moonlight-noir` and `docs/**`, and on PR to `moonlight-noir`.
- **Done**: test job (`testNonRoot_gameDebugUnitTest`), JaCoCo coverage, Codecov upload.
- **Missing**: lint job, format check, docs validate (design validator), secret scan.
- Jobs run on `ubuntu-latest` with setup-java and setup-android (not containerized yet).

## Description

Full per-commit CI workflow running lint, format, fast tests, docs validate,
secret scan, and JaCoCo coverage upload to Codecov.

## Acceptance Criteria

- [x] CI triggers on every push.
- [x] Fast unit tests run and report results.
- [x] JaCoCo coverage uploaded to Codecov.
- [ ] Lint check runs and fails on violations.
- [ ] Format check runs.
- [ ] Docs validator runs (design validator via candelamoon-docs image).
- [ ] Secret scan runs.
- [ ] Jobs should run in containerized images (from P1-005) once available.

## Remaining Work

1. Add lint job (e.g., ktlint or spotless for Android).
2. Add format check job.
3. Add docs validate job (requires P1-002 candelamoon-docs image).
4. Add secret scan job (requires P1-003 candelamoon-security image).
5. Migrate jobs to containerized images once P1-005 is complete.

## Known Risks

- Container images not yet built (P1-001..P1-005 pending) — current jobs run on
  ubuntu-latest as interim solution.
- Secret scan on every commit may be noisy — consider gating to PRs only.

## References

- Workflow: `.github/workflows/ci.yml`
- Infra: `docs/infrastructure/ci-architecture.md`
- Images: P1-001..P1-005
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| 2026-08-06 | In Development (PR #3) | — | PR #3 | — |
