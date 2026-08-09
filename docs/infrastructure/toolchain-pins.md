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
- **Digest/SHA**: pinned via `docker.io/eclipse-temurin:17-jdk@sha256:23441a35a47dca0fdd77b1b406adc1f86f29d042033ca9fece736a2633f8ba43` (resolved at Phase 1 on 2026-08-08 via `podman pull docker.io/eclipse-temurin:17-jdk && podman image inspect --format '{{index .RepoDigests 0}}'`; image ID `9da03b73ed12ca502e28ddd65a4d60302f084c484f0235f523808f796c0f7947`, created 2026-08-04 01:27:24 UTC, in-image `java -version` reports `openjdk 17.0.19 2026-04-21` / `OpenJDK Runtime Environment Temurin-17.0.19+10`).
- **Rationale**: AGP 8.x (here 8.13.0) requires JDK 17 as its minimum; the project has not moved to JDK 21. The Windows host build already runs JDK 17 (`appveyor.yml:11` sets `JAVA_HOME=C:\Program Files\Java\jdk17`); the container must use the same major version so host and container builds produce equivalent bytecode and behave identically. JDK 17 is LTS and supported until at least 2029.
- **Where used**: `candelamoon-android` image (runtime JDK for Gradle/AGP), `windows-host-test` job (`actions/setup-java` with `java-version: '17'`).

## Android SDK

compileSdk 36, targetSdk 34 (Google Play Aug 2026 requires TV apps to target API 34+), minSdk 28 (per ADR 0007). Pin cmdline-tools and platform-tools versions.

- **Tool**: Android SDK (cmdline-tools, platform-tools, platform 36, build-tools 36)
- **Exact versions** (installed with `sdkmanager --sdk_root=$ANDROID_HOME`):

  | Component | Package ID | Version | Resolved at Phase 1 |
  |---|---|---|---|
  | Command-line tools | `cmdline-tools;16.0` | 16.0 (build 13114758) | downloaded from `https://dl.google.com/android/repository/commandlinetools-linux-13114758_latest.zip`; SHA-256 of the zip to be pinned at Phase 1 follow-up (recorded as `TODO(P1-001-followup)` in the Containerfile) |
  | Platform tools | `platform-tools` (no versioned package ID in repository2-3.xml; pinned in the Containerfile by direct download of the versioned archive) | 37.0.1 (resolved exact) | `platform-tools_r37.0.1-linux.zip` from dl.google.com, verified against the SHA-1 published in repository2-3.xml (`477254aa5f903c15cf51001717bdf347fb6b53e0`) before extraction; the spec said "36.x", 37.0.1 is the resolved exact that ships with cmdline-tools 16.0 |
  | Android platform | `platforms;android-36` | 36 (matches `compileSdk = 36`, `app/build.gradle:7`) |
  | Build tools | `build-tools;36.0.0` | 36.0.0 |
  | NDK | `ndk;27.0.12077973` | 27.0.12077973 (see NDK section) |

- **Source URLs**: https://developer.android.com/studio#command-line-tools-only ; package metadata from https://dl.google.com/android/repository/repository2-3.xml
- **Digest/SHA**: cmdline-tools zip downloaded at build time from the URL above; the resulting `$ANDROID_HOME` is a pinned cache volume. SHA-256 of the cmdline-tools zip to be recorded here once captured.
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
- **Exact version**: 22 LTS (pin the concrete `22.x.y` at Phase 1; 22 is Active LTS in 2026). **Resolved 2026-08-09 to `22.23.2`** (latest 22.x LTS security release, published 2026-07-28, from the "Jod" LTS line).
- **Source URL**: https://nodejs.org/en/download (official tarballs; install from `node-v22.x.y-linux-x64.tar.xz`)
- **Digest/SHA**: `node-v22.23.2-linux-x64.tar.xz` SHA-256 = `d60acfe00a2932254bb0ad20e01b0d74397a0875595de719654b214f4b03f307` (from `https://nodejs.org/dist/v22.23.2/SHASUMS256.txt`; verified by `sha256sum -c` in the Containerfile at build time). To bump Node 22.x.y: download the new `SHASUMS256.txt` entry and update this line plus the `NODE_VERSION` / `NODE_SHA256_LINUX_X64` ENV lines in `infra/containers/candelamoon-docs/Containerfile` in lockstep.
- **Where used**: `candelamoon-docs` (markdownlint-cli, markdown-link-check), `candelamoon-security` (npm-based scanners: `npm audit`, gitleaks via npm distribution, semgrep engine dependencies).
- **candelamoon-docs npm pins** (resolved 2026-08-09; **transitive tree lock-locked 2026-08-09** in `infra/containers/candelamoon-docs/package-lock.json`, lockfileVersion 3, generated with `npm install --package-lock-only`; the Containerfile installs the exact locked tree with `npm ci --ignore-scripts` and wires the global layout under `/opt/node`):
  - `markdownlint-cli@0.45.0` (registry.npmjs.org; single bin `markdownlint`)
  - `markdown-link-check@3.13.7` (registry.npmjs.org; chosen over the pip alternative `linkchecker` to keep the link checker on the same npm toolchain as markdownlint-cli and avoid `linkchecker`'s additional Python deps)
- **Rationale**: LTS-only policy keeps both images on one supported major; Node 22 is the longest-supported current LTS line and matches the tooling used by the docs/security images. Never float to `latest`.

## Python

Pin Python 3.11+ for design validator and contract fixtures.

- **Tool**: CPython
- **Exact version**: 3.11.x (min 3.11; pin concrete patch via `python:3.11-slim` digest)
- **Source URL**: https://www.python.org/downloads/ ; base image `docker.io/library/python:3.11-slim`
- **Digest/SHA**: `@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` for the `candelamoon-docs` image; same digest applies to `luminal-contract` because both images use the same base. (See Container Base Images section for resolution details.)
- **Where used**: `candelamoon-docs` (design validator: architecture schema, ADR, capability-matrix, evidence validation; link/format checks), `luminal-contract` (protocol fixtures, host-response simulation, parser validation). Both images install pinned pip dependencies from `requirements-*.txt`/lockfiles at build time.
- **candelamoon-docs pip pins** (resolved 2026-08-09 by `podman build` against the pinned base; **hash-locked 2026-08-09** in `infra/containers/candelamoon-docs/requirements.lock`, regenerated with `uv pip compile --generate-hashes --python-version 3.11 --python-platform x86_64-unknown-linux-gnu requirements.txt`):
  - `jsonschema==4.23.0` (transitive: `attrs==26.1.0`, `jsonschema-specifications==2025.9.1`, `referencing==0.37.0`, `rpds-py==2026.6.3`, `typing-extensions==4.16.0`)
  - `pyyaml==6.0.2` (no transitive deps)
  - `yamllint==1.37.1` (transitive: `pathspec==1.1.1`)
  - `packaging==26.3` (pre-installed in the `python:3.11-slim` base image itself — not part of the lock; appears in `pip freeze` because it ships with the base's setuptools)
  - The Containerfile installs with `pip install --require-hashes --no-deps -r requirements.lock` (B-06/BAR-003/BAR-004 fix): every artifact's SHA-256 is verified and no live PyPI resolution happens at build time.
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
| `candelamoon-android` | Eclipse Temurin 17 JDK | `docker.io/eclipse-temurin:17-jdk` | `@sha256:23441a35a47dca0fdd77b1b406adc1f86f29d042033ca9fece736a2633f8ba43` (resolved 2026-08-08; image ID `9da03b73ed12ca502e28ddd65a4d60302f084c484f0235f523808f796c0f7947`, created 2026-08-04 01:27:24 UTC) |
| `candelamoon-docs` | Python 3.11 slim | `docker.io/library/python:3.11-slim` | `@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` (resolved 2026-08-09; image ID `245f9d32fabaec22e749aa5cfef79996088135e9d4410f4e7ebe133c2be98132`, created 2026-08-05 01:12:29 UTC; in-image `python3 --version` reports `Python 3.11.15`; in-image `cat /etc/os-release` reports `Debian GNU/Linux 13 (trixie)` / `DEBIAN_VERSION_FULL 13.6`) |
| `candelamoon-security` | TBD Phase 1 (candidate: python:3.11-slim + distroless/static scanner binaries) | TBD | `@sha256:<DIGEST security>` |
| `luminal-contract` | Python 3.11 slim | `docker.io/library/python:3.11-slim` | `@sha256:<DIGEST luminal>` |

Resolution procedure (Phase 1, recorded in this file next to each digest):
1. `podman pull <base>@<tag>` then `podman image inspect --format '{{index .RepoDigests 0}}' <base>` to obtain the digest.
2. Verify provenance: pull the digest form and compare `podman image inspect` metadata; record image ID and creation date.
3. Write the digest into the Containerfile `FROM` line and into the cache-key composition (ci-architecture.md). Never use the bare tag in a `FROM` once the digest is resolved.

**Rationale**: digest-pinned bases give bit-reproducible images; a base-image digest change is a reviewable event that bumps cache keys and retriggers the security-scan promotion gate. `candelamoon-security`'s base stays TBD until Phase 1 decides between python:3.11-slim (scanner scripting) and a distroless/static base (smaller surface) — the choice is recorded in an ADR before the Containerfile lands.
