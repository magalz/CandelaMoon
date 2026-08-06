# Toolchain Pins

> Status: Proposed (Phase 0 roadmap). Owner: Phase 1 infrastructure workstream.
> Policy: Every version in this file is normative. Changing a pin requires a PR that updates this file, the affected Containerfile(s), and the CI workflow pins in the same change. A pin change that affects build output also requires an ADR update.
> Placeholder rule: values marked `<TBD>` or `<PINNED_SHA>`/`<DIGEST>` must be resolved by the Phase 1 implementer (via `skopeo inspect` / commit SHA lookup) and replaced before the pin is considered active. The resolution date and command output are recorded next to the value.

## Summary

| Tool | Version | Verified source in repo |
|---|---|---|
| JDK | 17 (Temurin) | `appveyor.yml:11` (`JAVA_HOME=C:\Program Files\Java\jdk17`) |
| Android SDK | compileSdk 36, targetSdk 34, minSdk 28 | `app/build.gradle:6,12`; ADR 0007 (minSdk 28) |
| NDK | 27.0.12077973 | `app/build.gradle:4` |
| AGP | 8.13.0 | `build.gradle:8` |
| Gradle | 8.13 | `gradle/wrapper/gradle-wrapper.properties:3` |
| Podman | 5.x (pin at Phase 1) | this file |
| CMake / Ninja | 3.22.1 / 1.12.x (NDK-bundled) | this file |
| Clang | 18.0.2 (NDK-bundled) | this file |
| Node.js | 22 LTS (22.x) | this file |
| Python | 3.11+ (3.11-slim) | this file |
| GitHub Actions | all by commit SHA | this file |

---

## JDK

Pin JDK 17. Eclipse Temurin 17-jdk base for Podman. Rationale: Android Gradle Plugin 8.x requires JDK 17. Current AppVeyor uses JAVA_HOME=C:\Program Files\Java\jdk17.

- **Tool**: JDK 17 (Eclipse Temurin distribution, amd64)
- **Exact version**: Temurin 17 (latest patch, e.g. 17.0.15; the precise patch level is fixed by the base-image digest, not a floating tag)
- **Source URL**: https://adoptium.net/temurin/releases/?version=17
- **Digest/SHA**: pinned via `docker.io/eclipse-temurin:17-jdk@sha256:<DIGEST>` (resolve at Phase 1: `podman pull docker.io/eclipse-temurin:17-jdk && podman image inspect --format '{{index .RepoDigests 0}}'`)
- **Rationale**: AGP 8.x (here 8.13.0) requires JDK 17 as its minimum; the project has not moved to JDK 21. The Windows host build already runs JDK 17 (`appveyor.yml:11` sets `JAVA_HOME=C:\Program Files\Java\jdk17`); the container must use the same major version so host and container builds produce equivalent bytecode and behave identically. JDK 17 is LTS and supported until at least 2029.
- **Where used**: `candelamoon-android` image (runtime JDK for Gradle/AGP), `windows-host-test` job (`actions/setup-java` with `java-version: '17'`).

## Android SDK

compileSdk 36, targetSdk 34 (Google Play Aug 2026 requires TV apps to target API 34+), minSdk 28 (per ADR 0007). Pin cmdline-tools and platform-tools versions.

- **Tool**: Android SDK (cmdline-tools, platform-tools, platform 36, build-tools 36)
- **Exact versions** (installed with `sdkmanager --sdk_root=$ANDROID_HOME`):

  | Component | Package ID | Version |
  |---|---|---|
  | Command-line tools | `cmdline-tools;latest` | pin to 16.0 (pin the concrete release at Phase 1, e.g. `cmdline-tools;16.0`) |
  | Platform tools | `platform-tools` | pin to 36.x (resolve exact at Phase 1) |
  | Android platform | `platforms;android-36` | 36 (matches `compileSdk = 36`, `app/build.gradle:6`) |
  | Build tools | `build-tools;36.0.0` | 36.0.0 |
  | NDK | `ndk;27.0.12077973` | 27.0.12077973 (see NDK section) |

- **Source URLs**: https://developer.android.com/studio#command-line-tools-only ; package metadata from https://dl.google.com/android/repository/repository2-3.xml
- **Digest/SHA**: `<TBD>` — record the SHA-256 of the cmdline-tools zip and the repository XML revision at Phase 1; the SDK is installed at image build time and the resulting `$ANDROID_HOME` is a pinned cache volume.
- **SDK levels**: compileSdk 36 (current stable, `app/build.gradle:6`); targetSdk 34 (`app/build.gradle:12`) — Google Play requires TV apps to target API 34+ from August 2026, so 34 is the floor, not the ceiling; minSdk 28 per ADR 0007 so Android TV 9-11 (API 28-30) devices remain installable. Note: the checkout currently declares `minSdk 21` (`app/build.gradle:11`) — the roadmap raises it to 28 under ADR 0007; the Containerfile and CI matrix must not assume values below 28.
- **Licenses**: all SDK licenses accepted at image build time (`yes | sdkmanager --licenses`); the license acceptance is part of the image layer so runtime steps run network-free.
- **Rationale**: pinning cmdline-tools and platform-tools prevents SDK self-update drift between the container image and cached `$ANDROID_HOME` volumes; version skew here is the classic "works locally, fails in CI" cause.

## NDK

Pin 27.0.12077973 (from app/build.gradle line 4). Matched to AGP 8.13.0.

- **Tool**: Android NDK
- **Exact version**: 27.0.12077973 (`app/build.gradle:4`: `ndkVersion "27.0.12077973"`)
- **Source URL**: https://developer.android.com/ndk/downloads ; SDK package `ndk;27.0.12077973` via sdkmanager
- **Digest/SHA**: `<TBD>` — record the NDK zip SHA-256 at Phase 1.
- **Rationale**: `ndkVersion` in `app/build.gradle` is normative for AGP; the container must install exactly this revision so native builds (`ndkBuild` for the `root`/`nonRoot_game` flavors) use the identical compiler and sysroot on every machine. AGP 8.13.0 is compatible with NDK r27; do not float to r28+ without an ADR. The NDK also supplies CMake/Ninja/Clang (see below), so pinning the NDK pins the native toolchain in one place.

## Gradle

Pin AGP 8.13.0 and Gradle wrapper version (check gradle/wrapper/gradle-wrapper.properties). For Podman, Gradle runs inside candelamoon-android image.

- **Tool**: Gradle (wrapper distribution) and Android Gradle Plugin
- **Exact versions**:
  - Gradle 8.13 — `gradle/wrapper/gradle-wrapper.properties:3`: `distributionUrl=https\://services.gradle.org/distributions/gradle-8.13-bin.zip`
  - AGP 8.13.0 — `build.gradle:8`: `classpath 'com.android.tools.build:gradle:8.13.0'`
- **Source URLs**: https://services.gradle.org/distributions/gradle-8.13-bin.zip ; https://maven.google.com/com/android/tools/build/gradle/8.13.0/
- **Digest/SHA**: `<TBD>` — record the SHA-256 of the Gradle 8.13 distribution zip (published by Gradle) and the AGP artifact checksum at Phase 1.
- **Rationale**: AGP 8.13.0 requires Gradle 8.13 as its minimum and NDK 27 as its default NDK, so Gradle/AGP/NDK pins are a matched set — changing one requires revalidating the other two. In Podman, Gradle runs *inside* the `candelamoon-android` image (never on the host): the wrapper script is executed in-container with `GRADLE_USER_HOME` mounted as a pinned cache volume, so host and container never disagree about the distribution. The `windows-host-test` job is the deliberate exception (see ci-architecture.md) and runs `gradlew.bat` on the Windows runner to mirror AppVeyor.
- **Note**: the wrapper files themselves (`gradlew`, `gradlew.bat`) are part of the repo and should be checked for drift in the same PR as any pin bump.

## Podman

Pin Podman version for local dev and CI runners. WSL2 backend on Windows. Document machine/VM configuration.

- **Tool**: Podman (rootless)
- **Exact version**: 5.x (pin the concrete minor at Phase 1, e.g. 5.4.x, on both Linux runners and Windows dev machines)
- **Source URLs**: https://podman.io/docs/installation ; https://github.com/containers/podman/releases
- **Digest/SHA**: `<TBD>` — record the release tag/commit of the pinned Podman build.
- **Windows/WSL2 machine configuration** (documented and versioned in `infra/`):
  - Backend: WSL2 (not Hyper-V). `podman machine init` with a pinned distro (e.g. Fedora 41 podman-machine image).
  - Machine spec: 4 vCPU, 8 GiB RAM, 100 GiB disk (builds need headroom for `$ANDROID_HOME`, Gradle caches, and container images); rootless default; ssh config on a fixed port.
  - `podman machine set --rootful=false` — all dev flows run rootless to match CI.
  - Networking: user-mode (slirp4netns) default; ports only for adb (`5037`) and the emulator console when device-test runs locally.
- **CI runners**: self-hosted Linux (rootless Podman, `--userns=keep-id` mapping to uid 1000) — identical commands to dev so `podman build` output is byte-comparable.
- **Rationale**: one Podman minor version on dev and CI eliminates engine-behavior drift (volume mounts, userns, seccomp defaults). WSL2 keeps Windows dev builds container-native without Docker Desktop licensing or daemon privileges.

## CMake and Ninja

Pin versions for native builds invoked by NDK build.

- **Tool**: CMake and Ninja (native build orchestration for the NDK build of `app`)
- **Exact versions**: CMake 3.22.1 (SDK package `cmake;3.22.1`, bundled with NDK r27); Ninja 1.12.x (ships inside the NDK's cmake package, `$ANDROID_HOME/cmake/<ver>/bin/ninja`). Verify in-container with `cmake --version` and `ninja --version` during Phase 1 and record the exact outputs in this file.
- **Source URLs**: https://cmake.org/download/ ; https://github.com/ninja-build/ninja/releases ; sdkmanager package list (`cmake;3.22.1`)
- **Digest/SHA**: `<TBD>` — record the sdkmanager package checksums at Phase 1.
- **Rationale**: AGP drives native builds (`externalNativeBuild { ndkBuild { ... } }`, `app/build.gradle:33-52`) through its own bundled CMake/Ninja binaries; installing the matching SDK-provided versions in the image keeps the host and container toolchains identical and avoids the well-known "CMake version X not found" resolution failures. Never install a system CMake newer than the NDK-bundled one — AGP 8.13 pins tool versions internally and ignores newer ones for NDK builds.

## Clang

NDK ships its own clang. Pin the NDK clang version.

- **Tool**: Clang/LLVM (C/C++ compiler for NDK native code)
- **Exact version**: Clang 18.0.2 — the toolchain shipped inside NDK 27.0.12077973 at `$ANDROID_HOME/ndk/27.0.12077973/toolchains/llvm/prebuilt/<host>/bin/clang`. Confirm with `clang --version` in the Phase 1 image and record the output.
- **Source URL**: https://developer.android.com/ndk/downloads (NDK r27 release notes document the bundled LLVM version)
- **Digest/SHA**: `<TBD>` — covered by the NDK zip SHA-256 (see NDK section).
- **Rationale**: The NDK's clang is the only clang that may compile app native code. Host-provided clang (e.g. from a base image's build-essential) must not be used, because sysroot, libc++ and ABI flags are tied to the NDK revision. Pinning the NDK therefore pins the compiler; the rule here is a *negative* constraint (no external clang in `candelamoon-android`) plus a recorded version for diagnostics.

## Node

Pin Node.js LTS for candelamoon-docs and candelamoon-security containers.

- **Tool**: Node.js (JavaScript runtime for docs linting and security scanners)
- **Exact version**: 22 LTS (pin the concrete `22.x.y` at Phase 1; 22 is Active LTS in 2026)
- **Source URL**: https://nodejs.org/en/download (official tarballs; install from `node-v22.x.y-linux-x64.tar.xz`)
- **Digest/SHA**: `<TBD>` — record the official `SHASUMS256.txt` entry at Phase 1.
- **Where used**: `candelamoon-docs` (markdownlint-cli, link-check tooling, JSON Schema tooling), `candelamoon-security` (npm-based scanners: `npm audit`, gitleaks via npm distribution, semgrep engine dependencies).
- **Rationale**: LTS-only policy keeps both images on one supported major; Node 22 is the longest-supported current LTS line and matches the tooling used by the docs/security images. Never float to `latest`.

## Python

Pin Python 3.11+ for design validator and contract fixtures.

- **Tool**: CPython
- **Exact version**: 3.11.x (min 3.11; pin concrete patch via `python:3.11-slim` digest)
- **Source URL**: https://www.python.org/downloads/ ; base image `docker.io/library/python:3.11-slim`
- **Digest/SHA**: via base-image digest (see Container Base Images section)
- **Where used**: `candelamoon-docs` (design validator: architecture schema, ADR, capability-matrix, evidence validation; link/format checks), `luminal-contract` (protocol fixtures, host-response simulation, parser validation). Both images install pinned pip dependencies from `requirements-*.txt`/lockfiles at build time.
- **Rationale**: 3.11 is the floor because validator tooling (jsonschema, yamllint, pydantic-based schema checks) targets 3.11+; python:3.11-slim keeps both images small and guarantees the same interpreter on host and CI for fixture generation.

## GitHub Actions

Pin all actions by commit SHA, never by tag. List each action with pinned SHA placeholder.

Policy: every `uses:` line references a full 40-char commit SHA, never a tag or a branch. Dependabot (or renovate) is configured with `group: all` and commits the SHA bump together with the tag it resolved from; the mapping tag->SHA is recorded in the workflow comment or this file. A floating-tag action is a review-blocking finding.

| Action | Current tag (reference only) | Pinned SHA (fill at Phase 1) | Used by |
|---|---|---|---|
| `actions/checkout` | v5 | `<PINNED_SHA checkout>` | all jobs |
| `actions/setup-java` | v4 | `<PINNED_SHA setup-java>` | windows-host-test (JDK 17) |
| `actions/cache` | v4 | `<PINNED_SHA cache>` | unit-tests, device-test, compat-test |
| `actions/upload-artifact` | v4 | `<PINNED_SHA upload-artifact>` | lint-format, unit-tests, docs-validate, security-scan, sbom-delta, release-sign |
| `actions/download-artifact` | v4 | `<PINNED_SHA download-artifact>` | device-test, compat-test, release-sign |
| `actions/attest-build-provenance` | v2 | `<PINNED_SHA attest-build-provenance>` | release-sign, image promotion |
| `aquasecurity/trivy-action` | v0.x | `<PINNED_SHA trivy-action>` | security-scan, image promotion |
| `anchore/sbom-action` | v0.x | `<PINNED_SHA sbom-action>` | sbom-delta, image promotion |
| `sigstore/cosign-installer` | v3 | `<PINNED_SHA cosign-installer>` | release-sign, image promotion |
| `softprops/action-gh-release` | v2 | `<PINNED_SHA gh-release>` | release-sign |

**Source URL**: https://github.com/<owner>/<repo>/commits/<branch> (resolve SHA at pin time); action metadata additionally checked via the GitHub Marketplace page.

**Rationale**: supply-chain rule from ADR-tracked security posture — tags are mutable, SHAs are not; the security image and threat model (ci-architecture.md) assume third-party code is frozen at review time.

## Container Base Images

Pin base image digests for: candelamoon-android (eclipse-temurin:17-jdk), candelamoon-docs (python:3.11-slim), candelamoon-security (base TBD Phase 1), luminal-contract (python:3.11-slim).

| Image role | Base image | Registry reference | Digest pin (resolve at Phase 1) |
|---|---|---|---|
| `candelamoon-android` | Eclipse Temurin 17 JDK | `docker.io/eclipse-temurin:17-jdk` | `@sha256:<DIGEST android>` |
| `candelamoon-docs` | Python 3.11 slim | `docker.io/library/python:3.11-slim` | `@sha256:<DIGEST docs>` |
| `candelamoon-security` | TBD Phase 1 (candidate: python:3.11-slim + distroless/static scanner binaries) | TBD | `@sha256:<DIGEST security>` |
| `luminal-contract` | Python 3.11 slim | `docker.io/library/python:3.11-slim` | `@sha256:<DIGEST luminal>` |

Resolution procedure (Phase 1, recorded in this file next to each digest):
1. `podman pull <base>@<tag>` then `podman image inspect --format '{{index .RepoDigests 0}}' <base>` to obtain the digest.
2. Verify provenance: pull the digest form and compare `podman image inspect` metadata; record image ID and creation date.
3. Write the digest into the Containerfile `FROM` line and into the cache-key composition (ci-architecture.md). Never use the bare tag in a `FROM` once the digest is resolved.

**Rationale**: digest-pinned bases give bit-reproducible images; a base-image digest change is a reviewable event that bumps cache keys and retriggers the security-scan promotion gate. `candelamoon-security`'s base stays TBD until Phase 1 decides between python:3.11-slim (scanner scripting) and a distroless/static base (smaller surface) — the choice is recorded in an ADR before the Containerfile lands.
