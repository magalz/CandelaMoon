# P1-009: Create evidence-manifest YAML template

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: none
**Complexity**: S
**Related ADRs**: 0013

## Description

Create the evidence-manifest YAML template used to link red/green TDD evidence in
PRs. Forms the machine-readable contract for the evidence gates.

## Acceptance Criteria

- Template file exists and conforms to `docs/schema/evidence-manifest.schema.json`.
- Template includes fields for: task ID, phase, acceptance criteria, red-phase
  evidence, green-phase evidence, review findings, coverage rating.
- Template is referenced from the PR template.

## Implementation Plan

1. Read the evidence-manifest schema and handoff template.
2. Create the evidence-manifest YAML template in `docs/templates/` or `.github/`.
3. Validate against the JSON Schema.

## Evidence Requirements

- Template validates cleanly against the schema.
- `python scripts/validate_design.py --strict` passes after adding.

## Known Risks

- Template must stay in sync with the evidence-manifest JSON Schema.

## References

- Schema: `docs/schema/evidence-manifest.schema.json`
- ADRs: 0013

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
