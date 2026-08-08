# P1-013: Release-candidate CI workflow

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: P1-010
**Complexity**: L
**Related ADRs**: 0014

## Description

Add the release-candidate CI workflow running device tests, signing, and provenance
generation. Produces the auditable release artifact trail.

## Acceptance Criteria

- `.github/workflows/release.yml` triggers on release tag creation.
- Device tests run on self-hosted runners (P1-014, P1-015).
- Release artifacts are signed.
- SLSA provenance is generated and attached.
- Workflow produces a release with artifacts.

## Implementation Plan

1. Create `.github/workflows/release.yml` with tag trigger.
2. Add device test jobs using self-hosted runners.
3. Add signing job.
4. Add provenance generation job.
5. Test with a pre-release tag.

## Evidence Requirements

- Workflow runs on tag creation.
- Signed artifacts are published.
- Provenance is verifiable.

## Known Risks

- Self-hosted runners must be online for device tests.
- Signing key must be available as a GitHub secret.

## References

- Infra: `docs/infrastructure/ci-architecture.md`, `docs/infrastructure/secrets-and-signing-policy.md`
- Runners: P1-014, P1-015
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
