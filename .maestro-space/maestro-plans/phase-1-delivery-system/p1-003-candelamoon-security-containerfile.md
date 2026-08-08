# P1-003: candelamoon-security Containerfile

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: none
**Complexity**: M
**Related ADRs**: 0014

## Description

Define the containerized security-scanning environment covering secret scan,
dependency audit, and SBOM generation. Used by per-commit and per-PR security gates.
Resolves M0-001 (candelamoon-security base image decision from D2).

## Acceptance Criteria

- Containerfile at `infra/containers/candelamoon-security/Containerfile` builds successfully with Podman.
- Image contains secret scanning tools (e.g., truffleHog or gitleaks).
- Image contains dependency audit tools (e.g., OWASP Dependency-Check or pip-audit).
- Image contains SBOM generation capability.
- Image runs as non-root.

## Implementation Plan

1. Read handoff, toolchain pins, CI architecture, and security policies.
2. Research and select security scanning tools compatible with the project's stack.
3. Create `infra/containers/candelamoon-security/Containerfile`.
4. Install selected tools, verify they work against the codebase.
5. Configure non-root user.

## Evidence Requirements

- `podman build` succeeds.
- Each security tool produces output when run against the repo (even if no findings).

## Known Risks

- Tool selection must balance coverage with container size and build time.
- Some tools may require network access for vulnerability database updates.

## References

- Infra: `docs/infrastructure/ci-architecture.md`, `docs/infrastructure/toolchain-pins.md`
- Security: `docs/infrastructure/threat-model.md`, `docs/infrastructure/supply-chain-policy.md`
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
