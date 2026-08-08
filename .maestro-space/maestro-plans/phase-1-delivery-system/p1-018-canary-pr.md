# P1-018: Canary PR proving all paths

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: P1-005, P1-006, P1-007, P1-008, P1-009, P1-010, P1-011, P1-012, P1-013, P1-014, P1-015, P1-016, P1-017
**Complexity**: M
**Related ADRs**: 0014

## Description

Run a canary PR exercising every pipeline path: containerized jobs, device tests,
Windows host integration, evidence manifests, and synchronization gates. Proves
the delivery system end to end.

## Acceptance Criteria

- A PR is opened that touches a representative code change.
- All CI tiers trigger and complete: per-commit, per-PR, nightly, release-candidate.
- Containerized jobs run in the published images.
- Device tests run on the self-hosted TV Streamer runner.
- Windows host integration tests run on the self-hosted Windows runner.
- Evidence manifest is generated.
- Memtrace sync check passes.
- Design validator passes.
- Branch protection gates the merge.

## Implementation Plan

1. Create a small, safe code change (e.g., add a comment or fix a typo).
2. Open a PR with the evidence manifest.
3. Observe all CI tiers triggering and completing.
4. Document which paths passed and which need attention.

## Evidence Requirements

- All CI tiers complete successfully.
- PR can be merged without admin override.

## Known Risks

- Self-hosted runners must be online (P1-014, P1-015).
- Nightly schedule may need manual trigger for the canary test.

## References

- All Phase 1 tasks P1-001 through P1-017
- Infra: `docs/infrastructure/ci-architecture.md`
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
