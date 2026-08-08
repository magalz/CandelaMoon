# P1-002: candelamoon-docs Containerfile

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: none
**Complexity**: S
**Related ADRs**: 0014

## Description

Define the containerized documentation build and validation environment, including
the design validator. Used by the docs validate job in CI.

## Acceptance Criteria

- Containerfile at `infra/containers/candelamoon-docs/Containerfile` builds successfully with Podman.
- Image contains Python 3.x with jsonschema and pyyaml.
- `python scripts/validate_design.py --strict` succeeds inside the container.
- Image runs as non-root.

## Implementation Plan

1. Read handoff, toolchain pins, and CI architecture docs.
2. Create `infra/containers/candelamoon-docs/Containerfile`.
3. Install Python, pip deps from `scripts/requirements.txt`.
4. Configure non-root user.
5. Build and verify the validator runs inside.

## Evidence Requirements

- `podman build` succeeds.
- `python scripts/validate_design.py --strict` passes with exit code 0.

## Known Risks

- Python version must be pinned per toolchain-pins.md.

## References

- Infra: `docs/infrastructure/ci-architecture.md`, `docs/infrastructure/toolchain-pins.md`
- Validator: `scripts/validate_design.py`, `scripts/requirements.txt`
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
