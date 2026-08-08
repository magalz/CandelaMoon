# P1-011: Per-PR CI workflow

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: P1-010
**Complexity**: L
**Related ADRs**: 0013, 0014

## Description

Add the per-PR CI workflow running full tests, the API-tier matrix, and the
Memtrace synchronization check. Serves as the required status gate for PR merge.

## Acceptance Criteria

- `.github/workflows/pr.yml` triggers on PR open, push, and synchronize.
- Full test suite runs (not just fast tests).
- API-tier matrix tests run (API 28, 29, 30, 31+).
- Memtrace sync check runs and gates the merge.
- Required status check configured in branch protection (P1-006).

## Implementation Plan

1. Extend the per-commit workflow or create a new PR-specific workflow.
2. Add full test suite job with API-tier matrix.
3. Add Memtrace synchronization check job.
4. Configure required statuses in branch protection.

## Evidence Requirements

- PR workflow runs successfully.
- API-tier matrix shows results for each tier.
- Memtrace sync job passes.

## Known Risks

- Full test suite may be slow — consider caching Gradle/Maven artifacts.
- API-tier matrix requires emulator or Robolectric at multiple SDK levels.

## References

- Infra: `docs/infrastructure/ci-architecture.md`
- ADRs: 0013, 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
