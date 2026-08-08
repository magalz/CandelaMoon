# P1-017: Integrate design validator into candelamoon-docs image and CI

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: P1-002, P1-010
**Complexity**: S
**Related ADRs**: 0014

## Description

Integrate the design validator into the candelamoon-docs image and the per-commit
CI docs validate job. Enforces design-doc validation on every commit.

## Acceptance Criteria

- candelamoon-docs image (P1-002) includes the design validator.
- Per-commit CI (P1-010) docs-validate job runs inside the candelamoon-docs container.
- `python scripts/validate_design.py --strict` runs and gates the commit.

## Implementation Plan

1. Verify candelamoon-docs image has Python + deps for the validator.
2. Add docs-validate job to per-commit CI workflow.
3. Test with intentional doc failures to confirm gating.

## Evidence Requirements

- CI job runs and passes for valid docs.
- CI job fails for invalid docs.

## Known Risks

- Validator must be fast enough for per-commit CI (<2 minutes).

## References

- Image: P1-002
- Workflow: P1-010
- Validator: `scripts/validate_design.py`
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
