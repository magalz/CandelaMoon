# P1-016: Integrate Memtrace synchronization check into CI

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: P1-011
**Complexity**: M
**Related ADRs**: 0013, 0019

## Description

Integrate the Memtrace synchronization check into CI, verifying the sync state
tuple and gates. Prevents graph/commit drift from reaching review or merge.

## Acceptance Criteria

- Memtrace sync check runs in the per-PR CI workflow (P1-011).
- Job verifies that the Memtrace indexed SHA matches the PR head SHA.
- Job fails if the index is stale or desynchronized.
- Failure blocks merge (via branch protection ruleset).

## Implementation Plan

1. Add a job to `.github/workflows/pr.yml` that runs `memtrace status`.
2. Parse the output to verify sync state.
3. Gate merge on this check.

## Evidence Requirements

- Job passes when Memtrace is synchronized.
- Job fails when Memtrace is stale or desynchronized.
- Failure blocks merge.

## Known Risks

- Memtrace indexing must be fast enough for CI — consider incremental indexing.
- First-time index may be slow; accept cached index from previous runs.

## References

- Workflow: P1-011 (per-PR CI)
- ADRs: 0013, 0019

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
