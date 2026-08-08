# P1-012: Nightly CI workflow

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: P1-010
**Complexity**: M
**Related ADRs**: 0014

## Description

Add the nightly CI workflow covering emulator compatibility, dependency freshness,
and contract fixtures. Detects regressions the per-PR pipeline does not cover.

## Acceptance Criteria

- `.github/workflows/nightly.yml` triggers on schedule (cron).
- Emulator compatibility tests run on a schedule.
- Dependency freshness check runs (e.g., `gradle dependencyUpdates`).
- Contract fixture tests run.
- Failures are reported but do not block PRs.

## Implementation Plan

1. Create `.github/workflows/nightly.yml` with schedule trigger.
2. Add emulator compatibility job.
3. Add dependency freshness job.
4. Add contract fixture job.
5. Configure notifications on failure.

## Evidence Requirements

- Workflow runs on schedule.
- Each job produces output.

## Known Risks

- Emulator jobs may be flaky — accept some instability for nightly.
- Schedule runs consume GitHub Actions minutes.

## References

- Infra: `docs/infrastructure/ci-architecture.md`
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
