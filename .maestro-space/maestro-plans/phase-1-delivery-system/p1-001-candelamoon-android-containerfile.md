# P1-001: candelamoon-android Containerfile

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: none
**Complexity**: M
**Related ADRs**: 0014

## Description

Define the containerized Android build environment (JDK 17, Android SDK, NDK,
Gradle 8.13) used by all containerized CI tiers. Enables reproducible local and
CI builds. A local dev build of the CI-equivalent image was used to validate
P1-021; the official `infra/containers/candelamoon-android/Containerfile` is
this task's deliverable.

## Acceptance Criteria

- Containerfile at `infra/containers/candelamoon-android/Containerfile` builds successfully with Podman.
- Image contains JDK 17, Android SDK cmdline-tools, platform-tools, build-tools, platforms (API 36+), NDK.
- Image runs as non-root (uid 1000).
- `./gradlew testNonRoot_gameDebugUnitTest` succeeds inside the container.
- Containerfile is documented with inline comments explaining each layer.

## Implementation Plan

1. Read the handoff, the toolchain pins (`docs/infrastructure/toolchain-pins.md`), and CI architecture (`docs/infrastructure/ci-architecture.md`).
2. Create `infra/containers/candelamoon-android/Containerfile` from the base image specified in toolchain pins.
3. Install JDK 17, Android SDK components, NDK, and Gradle.
4. Configure non-root user.
5. Build the image with Podman and verify the test suite runs inside it.
6. Update the handoff with build evidence (image SHA, test results).

## Evidence Requirements

- `podman build` succeeds without errors.
- `./gradlew testNonRoot_gameDebugUnitTest` passes inside the container (68/68 or equivalent).
- Image digest recorded in toolchain pins or a companion file.

## Known Risks

- Android SDK license acceptance must be automated in the Containerfile.
- NDK version must match what the project's CMakeLists.txt expects.
- Network access during `podman build` for SDK download — document as one-time.

## References

- Spec: `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md` §9.2, §15
- Infra: `docs/infrastructure/ci-architecture.md`, `docs/infrastructure/toolchain-pins.md`
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
