# P1-005: Build and publish images to GHCR with signatures

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: P1-001, P1-002, P1-003, P1-004
**Complexity**: M
**Related ADRs**: 0014

## Description

Build all four images (candelamoon-android, candelamoon-docs, candelamoon-security,
luminal-contract), publish them to GitHub Container Registry, and sign them for
supply-chain verification. Establishes the image release baseline for every CI tier.

## Acceptance Criteria

- All four images build with Podman.
- All four images are pushed to GHCR with tags.
- All four images are signed (Cosign or equivalent).
- Image digests are recorded for reproducibility.

## Implementation Plan

1. Read handoff and verify all four Containerfiles exist and build.
2. Configure GHCR authentication.
3. Build, tag, push, and sign all four images.
4. Record image digests in toolchain pins or a companion file.

## Evidence Requirements

- `podman build` for all four images succeeds.
- `podman push` to GHCR succeeds.
- Signatures verified with `cosign verify`.
- Image digests recorded.

## Known Risks

- GHCR authentication requires a PAT or GITHUB_TOKEN with packages:write.
- Signing key must be available in CI but never committed.

## References

- Containerfiles: P1-001 through P1-004
- Infra: `docs/infrastructure/ci-architecture.md`, `docs/infrastructure/secrets-and-signing-policy.md`
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
