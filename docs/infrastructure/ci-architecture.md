# CI Architecture

> Status: Proposed (Phase 0 roadmap). Owner: Phase 1 infrastructure workstream.
> Scope: defines the container execution boundary, the four image roles, every CI job, and the four pipeline tiers. A Phase 1 implementer must be able to write the four Containerfiles and the GitHub Actions workflow YAML from this document alone (tool versions come from toolchain-pins.md).

## Principles

1. **Rootless by default** - every build, test, scan and sign step runs inside a rootless Podman container; the host (runner or dev machine) only runs Podman, git, and artifact staging.
2. **One digest everywhere** - the exact image digest built on a dev machine is the digest executed in CI; there is no separate "local image" and "CI image".
3. **Promotion is gated** - no image reaches the `ci` or `release` tag without SBOM, vulnerability scan, signature, and provenance attestation.
4. **Caches are explicit and keyed** - every mount is declared (source, cache, output); nothing is written back into the source tree.

---

## Podman

Rootless Podman as default execution boundary. Image promotion requires SBOM, vulnerability scan, signature, provenance. Same image digest locally and in CI. Cache keys: image digest + lockfile hash + toolchain version + target architecture.

### Execution boundary
- All CI steps run as `podman run` against images referenced **by digest** (see Container Base Images in toolchain-pins.md). The runner host executes no build logic directly.
- Rootless mode everywhere: self-hosted Linux runners run rootless podman (`--userns=keep-id`, user uid 1000 `builder`); Windows dev machines use `podman machine` with the WSL2 backend, rootless default. Privileged containers are banned; no job ever uses `--privileged` or `--device`.
- Hosts carry: podman, git, and a staging dir only. Version drift is prevented by the podman pin (toolchain-pins.md) enforced by a runner preflight check.

### Image promotion flow
Build -> scan -> attest -> promote. Gate: any missing/failed step blocks promotion.

1. `podman build --digestfile=image.digest -f infra/containers/<role>/Containerfile .` - produces the canonical digest.
2. **Vulnerability scan** - `trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 <digest>` (trivy DB updated by the nightly job; scan runs offline against the pinned DB volume).
3. **SBOM** - `syft <digest> -o cyclonedx-json` attached to the image record (also produced per-commit for app artifacts, see `sbom-delta`).
4. **Signature** - `cosign sign --key <KMS key ref> <digest>`; signature is stored in the registry (cosign keyless or KMS-backed per ADR; decision recorded at Phase 1).
5. **Provenance** - `actions/attest-build-provenance` (GitHub) or sigstore attestation for self-hosted builds: records repo, commit SHA, workflow, image digest, and inputs.
6. **Promote** - only now may the digest be tagged `ci` (per-PR) or `release` (release-candidate) and referenced by workflows.

### Same digest locally and in CI
- Dev and CI run the identical `podman build` command; CI asserts `git diff`-clean build context (no untracked files affect the build), then verifies that the local `image.digest` equals the CI digest recorded in the workflow run.
- Any image change (base digest bump, tool version bump) changes the digest, which automatically re-keys every cache (below) and retriggers the promotion gate - this is intentional.

### Cache keys
Composite key used for every cache volume (gradle home, android SDK, pip, npm, trivy DB, go/pkg):
`<image-digest> + <lockfile-hash> + <toolchain-version> + <runner-arch>`
- `image-digest`: `sha256:<...>` of the job's image (changes on any tooling change)
- `lockfile-hash`: `hashFiles('app/.../gradle.lockfile', '**/requirements*.txt', '**/package-lock.json')` (or equivalent resolved dependency manifest; exact files listed per job)
- `toolchain-version`: e.g. `jdk17-ndk27-agp8.13` (from toolchain-pins.md)
- `runner-arch`: `${{ runner.arch }}` (x64 / arm64)
Example key: `sha256:abcd...-h:a1b2c3d4-jdk17-ndk27-agp8.13-x64`. Read-only cache on per-commit tier; read-write only on PR and nightly tiers.

---

## Images

Define 4 image roles: candelamoon-android (JDK 17, Android SDK 36, NDK 27, Gradle 8.13, native build tools, unit/Robolectric), candelamoon-docs (Python 3.11, schema validation, Markdown/link checks, ADR/capability-matrix validation), candelamoon-security (SAST, dependency review, secret scanning, SBOM, license check, artifact verification), luminal-contract (Python 3.11, protocol fixtures, host-response simulation, parser validation). Each: Containerfile location, base image, installed tools, non-root user, read-only source mount, explicit cache/output mounts, network policy.

### Common conventions (applied to every image)
- **Non-root user**: user `builder`, uid/gid 1000; `USER builder` as the final directive in every Containerfile. All cache/output mounts are `chown builder:builder` at creation.
- **Source mount**: the repo is bind-mounted read-only at `/workspace` (`-v <repo>:/workspace:ro`); containers never write into the source tree. Generated files (lint reports, test results, SBOMs) land only in declared output mounts.
- **Cache mounts** (named volumes, keyed per the cache-key rule): `gradle-home:/home/builder/.gradle`, `android-sdk:/opt/android-sdk`, `pip-cache:/home/builder/.cache/pip`, `npm-cache:/home/builder/.npm`, `trivy-db:/root/.cache/trivy` (mounted read-only for scans), `go-pkg:/home/builder/go/pkg`.
- **Output mounts** (writable bind mounts): `reports:/workspace-out/reports`, `artifacts:/workspace-out/artifacts`. Jobs copy results from `/workspace-out/*` into the runner workspace for artifact upload.
- **Network policy**: `--network=none` is the default for every step; steps that need network declare it explicitly (see per-image "run-time network") via `--network=host` or an allowlisted proxy. Image *build* time may need network (package downloads) and is documented per image.

### candelamoon-android
- **Containerfile**: `infra/containers/candelamoon-android/Containerfile` *(implemented per P1-001; green-verified 2026-08-08, review phases 1+2 closed, STR-06 applied 2026-08-08. See handoff at `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/handoff.md`.)*
- **Base image**: `docker.io/eclipse-temurin:17-jdk@sha256:<DIGEST android>` (see toolchain-pins.md)
- **Installed tools**: JDK 17 (from base); Android SDK - cmdline-tools 16.0, platform-tools 36.x, `platforms;android-36`, `build-tools;36.0.0`, licenses pre-accepted at build time; NDK `27.0.12077973`; CMake 3.22.1 + Ninja (NDK-bundled); Gradle 8.13 (distribution pre-downloaded into `GRADLE_USER_HOME` at build time so builds run offline); Robolectric: `android-all` jars pre-fetched into the Gradle cache at build time (otherwise the first unit-test run hits the network).
- **Purpose**: unit/Robolectric tests, lint, native build, APK assembly. Compiles `app` for all flavors (`root`, `nonRoot_game`).
- **Build-time network**: `dl.google.com` (SDK packages), `services.gradle.org` (Gradle distribution), `maven.google.com`/`repo.maven.apache.org` (AGP deps), Robolectric artifact mirror.
- **Run-time network**: none by default; unit tests are hermetic. If a job must resolve dependencies at run time (explicitly discouraged - pre-warm caches at image build), it declares `--network=host` in that job only.
- **Run-time mounts**: source ro, `android-sdk` + `gradle-home` cache, `reports` + `artifacts` output.

### candelamoon-docs
- **Containerfile**: `infra/containers/candelamoon-docs/Containerfile`
- **Base image**: `docker.io/library/python:3.11-slim@sha256:<DIGEST docs>`
- **Installed tools**: Python 3.11 + pinned pip deps (jsonschema, pyyaml, yamllint, link checker e.g. `linkchecker` or `markdown-link-check`); Node.js 22 LTS + `markdownlint-cli`; design validator entrypoint (`validate-design` - schema validation of architecture schemas, ADR register, capability matrix, evidence manifest); ADR/capability-matrix validation scripts.
- **Purpose**: docs-validate job, memtrace-sync support, evidence audit.
- **Build-time network**: PyPI, npm registry.
- **Run-time network**: none - all validation is file-based and offline.
- **Run-time mounts**: source ro, `pip-cache` + `npm-cache`, `reports` output.

### candelamoon-security
- **Containerfile**: `infra/containers/candelamoon-security/Containerfile`
- **Base image**: TBD Phase 1 (candidate: `python:3.11-slim` + statically-linked scanner binaries; alternative: distroless base for scanners only - decided by ADR before this Containerfile lands)
- **Installed tools**: Python SAST (semgrep, bandit); dependency review (osv-scanner or `pip-audit` + `npm audit`); secret scanning (gitleaks); SBOM (syft); vulnerability scan (trivy); license check (licensecheck / ORT-lite); artifact verification (cosign). Scanner binary versions pinned in the Containerfile, never `latest`.
- **Purpose**: security-scan, sbom-delta, image-promotion scans, release-sign verification.
- **Build-time network**: GitHub releases (scanner binaries), PyPI.
- **Run-time network**: none for scans (trivy DB and semgrep rules are mounted from the pinned DB volumes refreshed nightly); `cosign verify` in release-sign needs registry access and declares it explicitly.
- **Run-time mounts**: source ro, `trivy-db` (ro), `go-pkg`, `reports` + `artifacts` output.

### luminal-contract
- **Containerfile**: `infra/containers/luminal-contract/Containerfile`
- **Base image**: `docker.io/library/python:3.11-slim@sha256:<DIGEST luminal>`
- **Installed tools**: Python 3.11 + pinned pip deps; protocol fixtures generator (shared with LuminalShine host contract), host-response simulation harness, parser validation tooling.
- **Purpose**: contract-fixture generation and validation, host-response simulation, extended stream/reconnect tests on the simulated host.
- **Build-time network**: PyPI.
- **Run-time network**: none - host simulation is loopback/in-process.
- **Run-time mounts**: source ro, `pip-cache`, `artifacts` output (fixture outputs).

---

## Jobs

Enumerate each CI job with name, image used, triggers (push/pull_request/nightly/release), inputs, outputs, what it validates. Jobs: lint-format, unit-tests, docs-validate, security-scan, sbom-delta, memtrace-sync, device-test, compat-test, windows-host-test, release-sign.

Common metadata: all container jobs run on self-hosted Linux runners with rootless podman; `windows-host-test` runs on `windows-latest` (no container, parity with AppVeyor). "Trigger" values: **push** = push to any branch (per-commit tier), **PR** = pull_request (+synchronize), **nightly** = cron schedule, **release** = workflow_dispatch / tag `v*`.

### 1. lint-format
- **Image**: candelamoon-android | **Trigger**: push, PR
- **Inputs**: source tree, toolchain-pins.md
- **Outputs**: `reports/lint/lint-results-*.html` + `.xml` (from `app/build/reports/lint-results-nonRootDebug.*`), format-diff report
- **Validates**: Kotlin/Java formatting (ktlint/checkstyle per repo config), Android lint (gradle `lintNonRootDebug`), that pin files match build files (AGP/NDK/Gradle wrapper vs toolchain-pins.md)

### 2. unit-tests
- **Image**: candelamoon-android | **Trigger**: push (fast lane: unit tests only), PR (full), nightly
- **Inputs**: source tree, gradle cache volume
- **Outputs**: `reports/test/*/TEST-*.xml` (JUnit XML), JaCoCo coverage report (`app/build/reports/jacoco/jacoco.xml`), aggregated `test` task output (root `build.gradle:21-32` aggregates all `*UnitTest` tasks)
- **Coverage**: JaCoCo XML report uploaded to Codecov via `codecov/codecov-action@v5` with `CODECOV_TOKEN` secret. Flags: `unit`. Coverage trends tracked at codecov.io.
- **Validates**: JVM unit tests + Robolectric tests (targetSdk 34 runtime) for all flavors; no native/hardware dependency

### 3. docs-validate
- **Image**: candelamoon-docs | **Trigger**: push, PR
- **Inputs**: `docs/`, schemas, ADR register, capability matrix, evidence manifest
- **Outputs**: `reports/docs/validator-report.txt`, link-check report, markdownlint report
- **Validates**: architecture/capability/ADR/evidence schemas against their JSON Schemas; Markdown lint + link check; ADR status consistency (no superseded ADR marked active); capability-matrix completeness (every capability row has ADR, task, PR, evidence)

### 4. security-scan
- **Image**: candelamoon-security | **Trigger**: PR (fast: secrets + dependency), nightly (full), release
- **Inputs**: source tree, lockfiles, pinned trivy DB + semgrep rules
- **Outputs**: SARIF findings (uploaded as security artifact), secret-scan report, dependency-review report, license report
- **Validates**: SAST findings (semgrep/bandit), dependency vulnerabilities (osv/pip-audit/npm audit), secrets (gitleaks), license compliance. Policy: PR tier fails on new HIGH/CRITICAL findings introduced by the diff; nightly fails on any HIGH/CRITICAL in the full tree.

### 4a. mobsfscan (Android SAST)
- **Image**: none — runs on GitHub-hosted runner directly | **Trigger**: PR (on changes to `app/src/**`, `app/build.gradle`)
- **Inputs**: source tree (Android source + build files)
- **Outputs**: SARIF findings (uploaded to GitHub Code Scanning tab)
- **Validates**: Android-specific security issues — WebView SSL bypass, certificate pinning, root detection, tapjacking, insecure broadcast receivers, exported components, weak cryptography. Complements CodeQL's general Java/Kotlin queries with Android-specific checks.
- **Workflow**: `.github/workflows/mobsfscan.yml`

### 4b. secret-scan (TruffleHog)
- **Image**: none — runs on GitHub-hosted runner directly | **Trigger**: push (`moonlight-noir`), PR
- **Inputs**: full git history (`fetch-depth: 0`), commit range (`base..head`)
- **Outputs**: scan results logged to workflow run; fails on verified live credentials
- **Validates**: leaked credentials with active verification (800+ detectors). Unlike static regex matching, TruffleHog calls upstream APIs to confirm leaked keys are actually live. Complements the containerized gitleaks scan (job #4) which runs inside `candelamoon-security` when that image is built (P1-003).
- **Workflow**: `.github/workflows/trufflehog.yml`
- **Note**: This is a pre-container bridge — it runs on GitHub-hosted runners until the `candelamoon-security` image (P1-003) provides the containerized gitleaks scan. Both will coexist: TruffleHog for live credential verification, gitleaks for comprehensive regex-based scan.

### 4c. dependency-review
- **Image**: none — runs on GitHub-hosted runner directly | **Trigger**: PR
- **Inputs**: PR diff, dependency graph
- **Outputs**: dependency change report with vulnerability and license findings
- **Validates**: every dependency change introduced by the PR — new/updated/removed packages checked against the GitHub Advisory Database. Fails on `high` severity vulnerabilities. Denies GPL-3.0 and AGPL-3.0 licensed dependencies. Complements the containerized dependency review (osv-scanner + trivy in candelamoon-security, P1-003).
- **Workflow**: `.github/workflows/dependency-review.yml`
- **Note**: First-party GitHub action; pre-container bridge until P1-003 lands. Will coexist with the image-based scan as a fast PR-time gate.

### 5. sbom-delta
- **Image**: candelamoon-security | **Trigger**: PR, nightly
- **Inputs**: source tree, lockfiles, previous SBOM (from last green run, stored as artifact)
- **Outputs**: `reports/sbom/sbom.cyclonedx.json`, `sbom-delta.txt`
- **Validates**: dependency-set delta between base and head (added/removed/updated), new vulnerabilities introduced by the delta, drift between declared lockfiles and resolved SBOM

### 6. memtrace-sync
- **Image**: candelamoon-docs (+ memtrace CLI) | **Trigger**: push (main), nightly
- **Inputs**: source tree, Memtrace index config
- **Outputs**: index/coherence report
- **Validates**: indexed graph matches repo HEAD (no stale/missing symbols), spec-review and plan-review records in `.memtrace/` agree with the committed docs (specs, ADRs, capability rows)

### 7. device-test
- **Image**: candelamoon-android | **Trigger**: nightly (emulator), release (real device)
- **Inputs**: APK artifact (from unit-tests/build job), emulator/device profile
- **Outputs**: `reports/device/instrumentation-*.xml`, screenshots (visual evidence for capability rows)
- **Validates**: instrumented tests on Android TV emulator profile API 34 (nightly); on release-candidate, runs on the real Google TV Streamer hardware (see Pipeline Tiers)

### 8. compat-test
- **Image**: candelamoon-android | **Trigger**: nightly, release
- **Inputs**: APK artifact, device/API matrix
- **Outputs**: `reports/compat/matrix-*.csv`, failure classification report
- **Validates**: API-tier compatibility matrix across minSdk 28 .. compileSdk 36 (Android TV 9-11 focus per ADR 0007); targetSdk 34 behavior; flavor behavior (`root` maxSdk 25 vs `nonRoot_game`)

### 9. windows-host-test
- **Image**: none - runs on `windows-latest` runner (host build; the deliberate exception to the container boundary) | **Trigger**: push, PR
- **Inputs**: source tree, submodules (`git submodule update --init --recursive` per appveyor.yml:8)
- **Outputs**: `app/build/reports/lint-results-nonRootDebug.html`, connectedCheck results
- **Validates**: AppVeyor equivalence - `gradlew.bat build connectedCheck` with `JAVA_HOME=C:\Program Files\Java\jdk17` (appveyor.yml:11) and Android SDK at `C:\android-sdk`; catches Windows-only issues (line endings, path length, native lib loading) that containers cannot. Uses `actions/setup-java` JDK 17 + `actions/cache` for the SDK.

### 10. release-sign
- **Image**: candelamoon-android (build) + candelamoon-security (verify) | **Trigger**: release
- **Inputs**: release-candidate APK/AAB, SBOM (from sbom-delta), cosign key/KMS ref
- **Outputs**: signed APK/AAB, `checksums.txt` (SHA-256 per artifact), signed SBOM, provenance attestations (actions/attest-build-provenance), release notes evidence bundle
- **Validates**: artifact signature + provenance; SBOM signature; checksum integrity; that promotion gates (scan + SBOM + signature + provenance) all passed for the exact digest being released

---

## Pipeline Tiers

**Fork-PR security model:** Pull requests from forks run only non-secret jobs (lint, unit-tests, docs-validate, security-scan with public scanner rules). No GitHub Secrets, signing keys, device runners, or Memtrace daemon access are exposed to fork PRs. Fork PRs cannot trigger release-sign, device-test, compat-test, windows-host-test, or memtrace-sync jobs. Cache keys include a fork flag to prevent cache poisoning from fork builds affecting main-branch caches.

Define per-commit (formatting, lint, fast unit tests, docs validate, secret/dependency checks), per-PR (full tests, API-tier matrix, Memtrace review, acceptance/edge/blind/security reviews, SBOM delta, evidence audit), nightly (emulator/device compat, dependency freshness, contract fixtures, extended stream/reconnect tests), release-candidate (real Google TV Streamer + compat hardware, official host integration, long-session/fault tests, signed artifacts, provenance, SBOM, checksums, rollback rehearsal). Each tier: jobs included, triggers, timeout, cache policy, required artifacts.

### Per-commit
- **Jobs**: lint-format, unit-tests (fast lane - JVM unit tests only), docs-validate, security-scan (fast lane - secret scan + dependency review only), mobsfscan (Android SAST), TruffleHog (secret verification), dependency-review (PR dependency gate)
- **Triggers**: push to any branch (including PR branches). Always-blocking: a failed per-commit job blocks merge.
- **Timeout**: 15 minutes total.
- **Cache policy**: read-only. Caches are only *read* on this tier; misses are tolerated (image digest + lockfile + toolchain + arch key). No cache writes, no SBOM refresh.
- **Required artifacts**: lint report, unit-test JUnit XML, docs validator report, secret-scan report (all uploaded, retained 14 days).

### Per-PR
- **Jobs**: everything from per-commit, plus: unit-tests (full - all flavors + Robolectric), API-tier matrix (compat-test on emulators across the supported API range), memtrace-sync (Memtrace review of the diff vs indexed graph), acceptance/edge/blind/security reviews (the roadmap's review gate - each review type produces a report into the evidence bundle), sbom-delta, evidence audit (docs-validate extended: evidence manifest must agree with the diff, per spec-review.md:353)
- **Triggers**: pull_request (+ synchronize on push to the PR branch)
- **Timeout**: 60 minutes.
- **Cache policy**: read-write. This is the tier that refreshes caches (gradle, SDK package cache, pip, npm) under the composite key; SBOM and scan DBs are refreshed here only if older than 24h.
- **Required artifacts**: full test reports, compatibility matrix CSV, Memtrace coherence report, review evidence bundle (acceptance/edge/blind/security), SBOM + delta report, evidence audit report. Every PR must pass this tier before review approval.

### Nightly
- **Jobs**: device-test (emulator compat - Android TV emulator profile, API 34), compat-test (full device/API matrix), dependency freshness (security-scan full: fresh trivy DB, osv, npm/pip audit on current lockfiles), contract fixtures (luminal-contract: regenerate + validate fixtures, host-response simulation), extended stream/reconnect tests (long-running stream and reconnect fault tests on the simulated host)
- **Triggers**: cron, 00:30 UTC daily (configurable via workflow dispatch for ad-hoc runs)
- **Timeout**: 6 hours (extended tests are long-running by design).
- **Cache policy**: write. Refreshes trivy DB, semgrep rules, dependency caches, and SBOM baselines; publishes a nightly freshness report to the repo's evidence area.
- **Required artifacts**: device matrix results, contract fixture outputs, dependency freshness report (with any new HIGH/CRITICAL findings), extended stream/reconnect test logs. A nightly failure opens a blocking issue; it does not block merges by itself unless the issue stays open past SLA.

### Release-candidate
- **Jobs**: device-test on real Google TV Streamer + compat hardware (the physical device matrix, not emulators), official host integration (against the official LuminalShine host build, per spec-review.md scope rules - browser WebRTC path is out of scope), long-session/fault tests (multi-hour sessions, disconnect/reconnect/fault injection on real hardware), release-sign (sign APK/AAB, SBOM, checksums), image promotion gates (scan + SBOM + signature + provenance on the release digests), rollback rehearsal (publish the previous release's artifacts to the rollback slot and verify install/launch/rollback procedure end-to-end)
- **Triggers**: release workflow (manual dispatch on the release branch + tag `v*`)
- **Timeout**: 12 hours.
- **Cache policy**: frozen. No cache writes on this tier; the exact cache/key set from the green PR run is reused so the RC build is byte-reproducible. Any cache miss fails the tier (nothing may change between PR and RC).
- **Required artifacts**: signed APK/AAB, `checksums.txt`, signed SBOM, provenance attestations (actions/attest-build-provenance), real-device test reports, official-host integration logs, long-session/fault test evidence, rollback rehearsal evidence. Release is only cut when this tier is green.

---

## Cross-references
- Tool versions and digest resolution: toolchain-pins.md (same directory)
- Promotion gate policy and ADR/evidence rules: `.memtrace/spec-review.md` (sections 4-6)
- Native build shape (flavors, ndkBuild): `app/build.gradle`
- Windows host parity baseline: `appveyor.yml`
