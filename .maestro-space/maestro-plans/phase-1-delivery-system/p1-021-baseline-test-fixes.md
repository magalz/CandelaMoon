# P1-021: Fix baseline unit test failures

**Phase**: Phase 1
**Status**: Completed
**Dependencies**: none
**Complexity**: M
**Related ADRs**: 0014, 0016, 0019, 0020

## Current Evidence

- PR #6 merged. Branch: `phase1/p1-021-baseline-test-fixes`.
- 68/68 tests pass (`testNonRoot_gameDebugUnitTest`).
- Coverage audit: PASS, risk-weighted score 50/50.
- Memtrace reconciliation: clean (head `584dc970`).
- Review Phase 1: 6 findings triaged (PH1-001 through PH1-006).
- Review Phase 2: Red/Blue security review clean (SEC-001).
- UAT: Accepted.
- Local Podman image `localhost/candelamoon-android:dev` used for containerized test runs.
- Containerfile preserved outside repo for P1-001.

## Description

Fixed pre-existing unit test failures surfaced by Phase 0 CI:
- `LayoutInflationTest.allLayoutsInflateSuccessfully` (InflateException — FAB theme enforcement).
- `SimpleStartupTest.testApplicationOnCreate` (NPE — null-base Context in startup).
- `StartupCrashTest.testUiHelperCrash` (was green under Robolectric 4.16).

## Acceptance Criteria

- [x] `LayoutInflationTest` passes without InflateException.
- [x] `SimpleStartupTest` passes without null-base Context failure.
- [x] `StartupCrashTest` passes (was already green).
- [x] `./gradlew testNonRoot_gameDebugUnitTest` green (68/68).
- [x] Preserves API 28 compatibility; does not weaken production behavior.

## Artifacts

- Handoff: `docs/handoffs/phase1-p1-021-baseline-test-fixes-handoff.md`
- ATDD checklist: `docs/handoffs/phase1-p1-021-atdd-checklist.md`
- Coverage audit: `docs/audits/p1-021-coverage-audit.md`
- Session handout: `docs/handoffs/phase1-p1-021-session-handout.md`

## Known Debt

- DOC-001: Narrative discrepancy in review-patch Agent Output (24 vs 20 tests).
- DOC-002: JaCoCo line-coverage report not generated (needs CI job).
- PH1-005: LayoutInflationTest pre-existing retry behavior (deferred).

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| 2026-08-07 | In Development | `976f5354` | — | `docs/handoffs/phase1-p1-021-baseline-test-fixes-handoff.md` |
| 2026-08-07 | Review Phase 1 | `0aa9b711` | — | same |
| 2026-08-07 | Coverage Audit | `0aa9b711` | — | same |
| 2026-08-07 | Completed | `584dc970` | PR #6 | same |
