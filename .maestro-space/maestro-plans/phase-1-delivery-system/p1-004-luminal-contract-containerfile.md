# P1-004: luminal-contract Containerfile

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: none
**Complexity**: S
**Related ADRs**: 0014

## Description

Define the containerized contract-testing environment for Luminal contract fixtures.
Provides a stable runtime for contract validation jobs.

## Acceptance Criteria

- Containerfile at `infra/containers/luminal-contract/Containerfile` builds with Podman.
- Image provides the runtime needed to execute contract fixtures.
- Image runs as non-root.

## Implementation Plan

1. Read handoff, toolchain pins, and CI architecture docs.
2. Identify the contract fixture runtime requirements from the spec.
3. Create `infra/containers/luminal-contract/Containerfile`.
4. Build and verify.

## Evidence Requirements

- `podman build` succeeds.

## Known Risks

- Contract fixture format may evolve; Containerfile should be simple to update.

## References

- Infra: `docs/infrastructure/ci-architecture.md`, `docs/infrastructure/toolchain-pins.md`
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
