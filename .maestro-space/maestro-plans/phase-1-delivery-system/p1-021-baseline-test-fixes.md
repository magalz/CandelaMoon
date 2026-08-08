# P1-021: Fix baseline unit test failures surfaced by Phase 0 CI

**Phase**: Phase 1
**Status**: Completed
**Dependencies**: none
**Complexity**: M
**Related ADRs**: 0014, 0016, 0019, 0020

## Description

Fix the pre-existing unit test failures first surfaced by the Phase 0 CI run on
PR #3. Failing tests: `LayoutInflationTest.allLayoutsInflateSuccessfully`
(InflateException — component style requires Theme.MaterialComponents),
`SimpleStartupTest.testApplicationOnCreate` and `StartupCrashTest.testUiHelperCrash`
(NullPointerException — app startup code touches Context in a mocked environment).

Repair: fix app theme/layout for MaterialComponents, harden startup path against
null Context. Acceptance: `./gradlew testNonRoot_gameDebugUnitTest` green.

## Acceptance Criteria

- [x] `LayoutInflationTest.allLayoutsInflateSuccessfully` passes without InflateException.
- [x] `SimpleStartupTest.testApplicationOnCreate` passes without null-base Context failure.
- [x] `StartupCrashTest.testUiHelperCrash` passes without null-base Context failure.
- [x] `./gradlew testNonRoot_gameDebugUnitTest` is green (68/68).
- [x] Repair preserves API 28 compatibility and does not weaken production startup/layout behavior.

## Implementation Plan

Tasks A-D per the ATDD checklist:
1. Task A — Fix FAB theme enforcement in `styles.xml` and layout files.
2. Task B — Guard `ArtemisApplication.onCreate()` null-base path.
3. Task C — No change (StartupCrashTest already green live).
4. Task D — Full suite: fix 2 pre-existing `ProfilesNavigationTest` ClassCastExceptions.

## Evidence Requirements

- [x] Red-phase: 22 tests, 2 failed (LayoutInflationTest, SimpleStartupTest).
- [x] Green-phase: 68/68 PASSED, BUILD SUCCESSFUL.
- [x] Base comparison: 51 tests, 5 failed at base → 68/0 at head.
- [x] Coverage audit: PASS, risk-weighted score 50/50, Memtrace reconciliation clean.
- [x] Phase 1 review: 6 triaged findings (PH1-001 through PH1-006).
- [x] Phase 2 security: Red/Blue review clean (SEC-001).
- [x] UAT: Accepted.

## Known Risks

- Pre-existing `minSdk 21` in `app/build.gradle` vs ADR 0007's API 28 target — separate roadmap item.

## References

- Handoff: `docs/handoffs/phase1-p1-021-baseline-test-fixes-handoff.md`
- Coverage audit: `docs/audits/p1-021-coverage-audit.md`
- ATDD checklist: `docs/handoffs/phase1-p1-021-atdd-checklist.md`
- Session handout: `docs/handoffs/phase1-p1-021-session-handout.md`
- PR: #6
- ADRs: 0014, 0016, 0019, 0020

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| 2026-08-07 | In Development | `976f5354` | — | `docs/handoffs/phase1-p1-021-baseline-test-fixes-handoff.md` |
| 2026-08-07 | Review Phase 1 | `0aa9b711` | — | `docs/handoffs/phase1-p1-021-baseline-test-fixes-handoff.md` |
| 2026-08-07 | Coverage Audit | `0aa9b711` | — | `docs/handoffs/phase1-p1-021-baseline-test-fixes-handoff.md` |
| 2026-08-07 | Completed | `584dc970` | PR #6 | `docs/handoffs/phase1-p1-021-baseline-test-fixes-handoff.md` |
