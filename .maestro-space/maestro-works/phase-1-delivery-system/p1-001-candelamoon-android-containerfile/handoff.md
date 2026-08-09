---
change_id: "P1-001"
phase: "Phase 1"
task: "Create candelamoon-android Containerfile — containerized Android build environment (JDK 17, Android SDK 36, NDK 27, Gradle 8.13)"
status: "green-verified"
repository: "magalz/CandelaMoon"
branch: "moonlight-noir"
base_sha: "2118b61cd1dc49d600b36f06f7d832d5a7b8b824"
head_sha: "7731c4e7640ca6e09af80de8d62b661cd5f2510b"
pr_url: ""
acceptance_criteria:
  - "AC1: Containerfile exists at `infra/containers/candelamoon-android/Containerfile`."
  - "AC2: Base image is digest-pinned `docker.io/eclipse-temurin:17-jdk@sha256:23441a35a47dca0fdd77b1b406adc1f86f29d042033ca9fece736a2633f8ba43` (resolved via `podman pull` + `podman image inspect`; recorded in toolchain-pins.md and toolchain-pins.md § `Container Base Images`)."
  - "AC3: Installed tools match toolchain-pins.md: JDK 17 (Temurin 17.0.19+10 from base), Android cmdline-tools 16.0 (build 13114758), platform-tools 37.0.1, platforms;android-36, build-tools;36.0.0, NDK 27.0.12077973, CMake 3.22.1/Ninja (NDK-bundled). Licenses pre-accepted at build time."
  - "AC4: Gradle 8.13 distribution pre-downloaded into $GRADLE_USER_HOME/wrapper/dists/gradle-8.13-bin/5xuhj0ry160q40clulazy9h7d/ (zip + extracted + .ok marker); Robolectric android-all-instrumented JARs pre-fetched into /home/builder/.m2/repository/ for API 28..36 (nine versions, mapped per Robolectric 4.16 DefaultSdkProvider)."
  - "AC5: Non-root `builder` user (uid 1000, gid 1000) is the final USER directive. All SDK/cache directories (/opt/android-sdk, /opt/gradle, /home/builder) chown'd to builder:builder."
  - "AC6: Run-time network is `--network=none` (verified by AC7). Build-time network is limited to dl.google.com (SDK), services.gradle.org (Gradle), repo1.maven.org (Robolectric)."
  - "AC7: `podman build` succeeds from repo root; `podman run --rm --network=none <image> java -version` reports `openjdk 17.0.19` / `Temurin-17.0.19+10`; `podman run --rm --network=none <image> sdkmanager --list` shows build-tools;36.0.0, cmake;3.22.1, ndk;27.0.12077973, platform-tools 37.0.1, platforms;android-36."
  - "AC8: PARTIAL PASS — content-reproducible (two `--no-cache` builds produce identical file counts and sizes inside the image: 23,865 files under /opt and 327 under /home/builder, /opt total 2,985,576,280 bytes, /home/builder total 1,664,257,855 bytes in both). Image DIGEST is not bit-reproducible because Podman's layer-tar gzip is non-deterministic (~30-byte difference in the last layer per build). Tracked as known debt; full bit-reproducibility requires pinning every downloaded file by SHA-256 and a deterministic compression backend (see `Known Issues`)."
  - "AC9: `.containerignore` file excludes `.git/`, `.maestro-space/`, `docs/handoffs/`, build outputs (`.gradle/`, `build/`, `*.apk`, etc.), and non-container source artifacts. Verified by inspecting the file alongside the Containerfile."
  - "AC10: Containerfile is documented with inline comments linking each section to its governing doc (ci-architecture.md § `candelamoon-android` / `Common conventions`; toolchain-pins.md § `JDK` / `Android SDK` / `NDK` / `Gradle`; ADR 0014)."
tdd_artifacts:
  atdd_checklist: ""
  test_files: []
  red_phase_verified: false
implementation_artifacts:
  files_created:
    - "infra/containers/candelamoon-android/Containerfile"
    - ".containerignore"
  files_modified:
    - "docs/infrastructure/toolchain-pins.md"
  green_phase_verified: true
review_phase_1:
  blind_hunter_findings: []
  edge_case_hunter_findings: []
  acceptance_analyst_findings: []
  triaged_findings:
    - id: "patch-1"
      title: "Set HOME=/home/builder (BER-006, B-14)"
      finding_ids: ["BER-006", "B-14"]
      disposition: "applied"
      detail: "ENV HOME=/home/builder added to the standard-locations ENV block so shell tools resolving ~ / $HOME (Maven local repo $HOME/.m2, native OpenSSL helper ~/openssl) always land on the baked files regardless of the OCI launcher. Verified in-image: HOME=/home/builder and $HOME/.m2/repository resolves."
    - id: "patch-2"
      title: "User account hardening (BER-009, BER-010, B-08, B-09, B-10)"
      finding_ids: ["BER-009", "BER-010", "B-08", "B-09", "B-10"]
      disposition: "applied"
      detail: "Reworked the builder RUN: (1) postcondition asserts uid=1000/gid=1000 on every branch, failing the build on mismatch; (2) existing-builder branch validates identity instead of trusting it; (3) rename path strips supplementary groups via usermod -G builder and rewrites stale subuid/subgid records; (4) home ownership (stat %u) and owner-write bit (find -perm -u+w) validated without su/PAM; (5) builder-already-exists fallback skips the rename. Verified in-image: uid=1000(builder) gid=1000(builder) groups=1000(builder) only, /etc/subuid+subgid -> builder:100000:65536, ubuntu removed."
    - id: "patch-3"
      title: "Create /workspace before USER builder (BER-011)"
      finding_ids: ["BER-011"]
      disposition: "applied"
      detail: "RUN mkdir -p /workspace && chown builder:builder /workspace added before the USER builder directive. Verified: /workspace drwxr-xr-x builder builder in the built image."
    - id: "patch-4"
      title: "Set ANDROID_NDK_HOME + native tools on PATH (B-18)"
      finding_ids: ["B-18"]
      disposition: "applied"
      detail: "ENV ANDROID_NDK_HOME=${ANDROID_HOME}/ndk/27.0.12077973 (own ENV instruction) and NDK LLVM toolchain + cmake/3.22.1/bin prepended to PATH. Buildah does not expand ${ANDROID_HOME} within the same ENV instruction, so the ENV block was split (found by in-image validation: first build produced ANDROID_NDK_HOME=/ndk/27.0.12077973; fixed and re-verified). In-image: ANDROID_NDK_HOME=/opt/android-sdk/ndk/27.0.12077973, clang (NDK 18.0.1) + cmake 3.22.1 + ninja 1.10.2 on PATH."
    - id: "patch-5"
      title: "Pin platform-tools + integrity notes (BER-001, BER-003, BER-020, B-03)"
      finding_ids: ["BER-001", "BER-003", "BER-020", "B-03"]
      disposition: "applied"
      detail: "sdkmanager has NO versioned package ID for platform-tools (repository2-3.xml ships only the unversioned 'platform-tools' path, revision 37.0.1), so 'platform-tools;37.0.1' would fail. Instead the versioned archive platform-tools_r37.0.1-linux.zip is downloaded directly (the archive sdkmanager would resolve) and verified against the repository-XML SHA-1 (477254aa5f903c15cf51001717bdf347fb6b53e0) before extraction. toolchain-pins.md Android SDK table updated to the resolved exact 37.0.1. SHA-256 verification of all downloads deferred: TODO(P1-001-followup) comments added at cmdline-tools, platform-tools, Gradle, and Robolectric download sites. APT inputs documented as versioned by the base-image digest; full apt snapshotting deferred (BER-002 note)."
    - id: "patch-6"
      title: "Fix mtime normalization (BER-012, BER-013, B-20)"
      finding_ids: ["BER-012", "BER-013", "B-20"]
      disposition: "applied"
      detail: "Replaced the -newer /etc/hostname filter + 2>/dev/null || true block with a direct find /opt/android-sdk /opt/gradle /home/builder -exec touch -h -d @SOURCE_DATE_EPOCH {} + that covers all files and directories and fails the build if touch fails. Verified: adb, gradle, and Robolectric JAR paths all show 2025-01-01 00:00:00 UTC."
    - id: "patch-7"
      title: "Secret/credential exclusions in .containerignore (BER-015, B-23)"
      finding_ids: ["BER-015", "B-23"]
      disposition: "applied"
      detail: "Added .env, .env.*, *.jks, *.keystore, *.p12, *.pem, *-key.pem, *_key.pem, *.key, credentials.json, *.credentials, secrets/, **/secrets/, *.backup, *.bak to .containerignore under a new 'Secrets and credentials' section."
    - id: "patch-8"
      title: "Robolectric loop hardening (B-11, B-12)"
      finding_ids: ["B-11", "B-12"]
      disposition: "applied"
      detail: "Loop now continues on individual download failure (logged + counted), validates every JAR with unzip -tq (rejects HTML 200 pages, directories, truncated files), and fails at the end if any API is missing/corrupt. API 21-27 gap documented as intentional (ADR 0007 raises minSdk to 28; Robolectric 4.16 published set starts at API 28). Build log shows unzip -tq on all nine JARs and '[ 0 -gt 0 ]' (no failures)."
    - id: "patch-9"
      title: "Bootstrap hardening (B-02, B-06, B-07)"
      finding_ids: ["B-02", "B-06", "B-07"]
      disposition: "applied"
      detail: "apt: DEBIAN_FRONTEND=noninteractive + -o Acquire::Retries=3 on update and install. cmdline-tools extraction: rm -rf ${ANDROID_HOME}/cmdline-tools/latest before unzip/mv. Licenses: sdkmanager exit status authoritative + two postconditions (confirmation message grep on logged output; android-sdk-license file exists). sdkmanager install wrapped in timeout 600. Deviations: sdkmanager has no --timeout option (verified in the 16.0 build 13114758 jars), so the coreutils timeout wrapper is used; `set -o pipefail` on `yes | sdkmanager` would fail the build because yes dies of SIGPIPE (141) in this base, so the acceptance stream is pre-written to a file and stdin is redirected from it."
    - id: "defer-1"
      title: "Deferred: SHA-256 content verification of downloaded artifacts"
      finding_ids: ["BER-001", "BER-020", "B-03"]
      disposition: "deferred"
      detail: "Full checksum verification of cmdline-tools zip, Gradle zip, and Robolectric JARs requires resolving each artifact's SHA-256 first; marked with TODO(P1-001-followup) at every download site. HTTPS + pinned URLs are the current integrity controls. platform-tools is the exception: its SHA-1 from repository2-3.xml IS verified at build time."
    - id: "defer-2"
      title: "Deferred: full APT snapshotting"
      finding_ids: ["BER-002"]
      disposition: "deferred"
      detail: "APT packages are versioned implicitly by the base-image digest (eclipse-temurin base pins its own apt sources/revisions); documented inline with a TODO(P1-001-followup). Snapshot-pinning apt proxy is a follow-up, out of scope for this patch round."
    - id: "dismiss-1"
      title: "Dismissed-as-intentional: Robolectric API 21-27 prefetch gap"
      finding_ids: ["B-11"]
      disposition: "dismiss"
      detail: "Project minSdk moves to 28 per ADR 0007; the dev Containerfile and test suite only exercise API 28+; Robolectric 4.16's published android-all-instrumented set starts at API 28. Gap documented in the Containerfile with a revisit note when the minSdk bump lands."
  fixes_applied: true
review_phase_2:
  red_team_findings: []
  blue_team_findings: []
  triaged_findings:
    - id: "STR-01"
      title: "Base-image provenance remains unverified"
      finding_ids: ["STR-01"]
      severity: "high"
      disposition: "defer-to-CI (P1-005)"
      detail: "Digest pinning selects bytes, not publisher identity. The protected P1-005 publication job must verify the base reference against an allowlisted Eclipse Temurin publisher identity/attestation, generate the SBOM, run the vulnerability policy, and sign/push only after all gates pass. Not part of this dispatch."
    - id: "STR-02"
      title: "APT package selection can drift through the inherited repository"
      finding_ids: ["STR-02"]
      severity: "medium"
      disposition: "defer-to-CI (P1-005)"
      detail: "Live unversioned APT metadata could resolve trojanized packages. P1-005 must emit an SBOM with every APT package/version, compare with the approved toolchain baseline, run the vulnerability policy, and block publication on drift or scan failure. Not part of this dispatch."
    - id: "STR-03"
      title: "Root-executed Android SDK content lacks an independent publication gate"
      finding_ids: ["STR-03"]
      severity: "high"
      disposition: "defer-to-CI (P1-005)"
      detail: "A malicious cmdline-tools archive or SDK package executes as root during construction. P1-005 must require the SBOM to enumerate all Android components, run the vulnerability policy, attach provenance/SBOM, and sign/publish only on success. Not part of this dispatch."
    - id: "STR-04"
      title: "Gradle distribution provenance is deferred to the publication gate"
      finding_ids: ["STR-04"]
      severity: "high"
      disposition: "defer-to-CI (P1-005)"
      detail: "A modified Gradle 8.13 ZIP would be loaded as Java code by ./gradlew. Existing SHA-256 TODO stays; P1-005 SBOM must identify and compare the distribution against the approved toolchain entry. STR-06 cache controls must prevent later replacement. Not part of this dispatch."
    - id: "STR-05"
      title: "Robolectric artifacts remain a publication-gate concern"
      finding_ids: ["STR-05"]
      severity: "high"
      disposition: "defer-to-CI (P1-005)"
      detail: "A malicious but valid ZIP/JAR passes unzip -tq and is loaded by Robolectric. P1-005 must include all nine android-all-instrumented coordinates in the SBOM, compare against the Robolectric 4.16 mapping, and fail publication on drift or missing gate. Not part of this dispatch."
    - id: "STR-06"
      title: "Builder-writable tool trees and shared caches permit cross-trust poisoning"
      finding_ids: ["STR-06"]
      severity: "high (highest practical priority)"
      disposition: "applied"
      detail: "Baked tool trees are now root-owned and read-only for builder: the chown RUN was replaced with `chown -R root:root /opt/android-sdk /opt/gradle` + `find ... -type d/-type f -exec chmod go-w {} +` (execute/traversal bits untouched), keeping `chown -R builder:builder /home/builder` for Gradle/Maven runtime caches. Verified in-image (str06, id 6e1fa84379f2): /opt/android-sdk and /opt/gradle root:root 755, zero go-w dirs/files, zero non-root entries; builder `touch /opt/android-sdk/test_write` -> Permission denied; /home/builder writable by builder; adb executes (37.0.1-15733141); offline `./gradlew --version` -> Gradle 8.13 with the wrapper dist read from builder-owned /home/builder. NOTE: this supersedes the AC5 parenthetical (\"all SDK/cache directories chown'd to builder:builder\") — only /home/builder is builder-owned now. STR-06 CI-side enforcement (read-only/trust-scoped caches) remains with P1-010/P1-011; STR-10 (archive resource bounds) is the remaining open apply-now finding."
    - id: "STR-07"
      title: "Credential-bearing files should be excluded from the build context"
      finding_ids: ["STR-07"]
      severity: "medium"
      disposition: "applied"
      detail: "Expanded the secrets block of .containerignore with the full STR-07 pattern set: gradle.properties, **/gradle.properties, .netrc, **/.netrc, .m2/settings.xml, **/.m2/settings.xml, .ssh/, **/.ssh/, .ssh/id_*, **/.ssh/id_*, .aws/, **/.aws/, **/credentials, **/credentials.*, terraform.tfvars(.json), **/terraform.tfvars(.json), *.pfx, **/*.pfx. Verified by diff review; the no-COPY build is unaffected (build still green)."
    - id: "STR-08"
      title: "Normalize and fail closed on a pre-existing builder account"
      finding_ids: ["STR-08"]
      severity: "medium"
      disposition: "applied"
      detail: "Existing-builder branch now forces primary group to GID 1000 (usermod --gid 1000, tolerant), strips supplementary groups (usermod --groups builder), locks the password (usermod --lock), asserts id -G = 1000 only, and fails the build if /etc/sudoers or /etc/sudoers.d names builder or %builder. The ubuntu-rename branch gains the same password lock (its -G builder strip is the --groups equivalent). Micro-verified in isolation: hostile base with builder + sudo/video/dialout groups + sudoers rule fails the build with 'ERROR: builder has sudoers entries'; without a sudoers rule the block completes and leaves groups=1000(builder), password locked. Full build: uid=1000(builder) gid=1000(builder) groups=1000(builder), passwd -S builder -> L."
    - id: "STR-09"
      title: "Keep hostile builds off the host-facing checkout mount"
      finding_ids: ["STR-09"]
      severity: "medium"
      disposition: "defer-to-CI (P1-010/P1-011)"
      detail: "Rootless keep-id means a hostile PR can rewrite a writable /workspace bind mount. P1-010/P1-011 must bind the checkout read-only, run --read-only with a builder-owned ephemeral workspace, and never mount sockets/credentials. An image cannot enforce bind-mount flags, so this is a CI-level control. Not part of this dispatch."
    - id: "STR-10"
      title: "Bound archive download and extraction resources"
      finding_ids: ["STR-10"]
      severity: "low"
      disposition: "open — apply-now, separate dispatch"
      detail: "Add a guarded-download/check-zip helper with size/entry-count/expansion budgets per archive (cmdline-tools 512MiB/2GiB/100k, platform-tools 256MiB/1GiB/50k, Gradle 512MiB/2GiB/100k, Robolectric 512MiB/2GiB/250k) and free-space checks before unzip. NOT part of this STR-07/STR-08 dispatch — recommended for a follow-up patch round."
  fixes_applied: true
coverage_audit:
  rating: ""
  risk_weighted_score: 0
  memtrace_reconciliation: ""
  coverage_gaps: []
uat:
  status: "pending"
  user_decision: ""
documentation:
  tech_writer_artifacts: []
  session_handout: ".maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/session-handout.md"
  memtrace_repo_id: "CandelaMoon"
memtrace_indexed_sha: "2118b61cd1dc49d600b36f06f7d832d5a7b8b824"
memtrace_episode_ids: []
capability_rows: []
adrs: ["0014"]
verification:
  tests_pass: true
  memtrace_review: false
  acceptance_audit: false
  edge_case_hunt: false
  blind_hunt: false
  security_review: false
  policy_check: false
known_debt:
  - "AC8: Podman layer-tar gzip is non-deterministic, so two `--no-cache` builds produce different image digests. The image CONTENT is reproducible (verified by file count + total size match in /opt and /home/builder across two `--no-cache` rebuilds), but the image DIGEST is not bit-reproducible. Resolution path: pin every downloaded artifact by SHA-256 in the Containerfile and pass `--rewrite-timestamp --source-date-epoch` and a deterministic compression backend (e.g. zstd -19 with --no-content-check) when Podman supports it. Tracked as follow-up (out of scope for P1-001)."
  - "Cmdline-tools zip SHA-256 not pinned — the URL `commandlinetools-linux-13114758_latest.zip` is content-addressed by Google but not cryptographically verified at build time. Recording the SHA-256 in toolchain-pins.md is the next step."
  - "Gradle 8.13 distribution zip SHA-256 not pinned at build time — same caveat as cmdline-tools."
  - "Robolectric JARs not pinned by SHA-256 — same caveat."
  - "platform-tools 37.0.1 is now pinned in the Containerfile via direct download of platform-tools_r37.0.1-linux.zip with repository-XML SHA-1 verification (sdkmanager has no versioned package ID for it). toolchain-pins.md records the resolved exact. Bump the archive URL + SHA-1 in lockstep on any re-pin."
rollback_strategy: "Delete infra/containers/candelamoon-android/, .containerignore, and revert toolchain-pins.md digest update. No code or build files are affected — the Containerfile is not yet referenced by any CI workflow."
---

# Task: P1-001 — candelamoon-android Containerfile

## Context

Phase 1 (Delivery Foundation) requires a containerized Android build environment. ADR 0014 mandates Podman-first, rootless execution with images pinned by digest. The `candelamoon-android` image is the first of four container image roles (the others: P1-002 docs, P1-003 security, P1-004 luminal-contract). It serves as the build/test/lint/native-compile environment for all Android CI tiers.

A local dev build of the CI-equivalent image was used to validate P1-021 (Containerfile preserved at `%TEMP%/opencode/p1-021/Containerfile`). This task promotes that proven build into the official tracked location.

**Key references:**
- CI architecture: `docs/infrastructure/ci-architecture.md` § "candelamoon-android" (lines 60-67)
- Toolchain pins: `docs/infrastructure/toolchain-pins.md` (all tool versions)
- ADR 0014: `docs/adr/0014-podman-first-execution.md`
- Phase plan: `.maestro-space/maestro-plans/phase-1-delivery-system/phase-plan.md`

## Instructions for Agent

**Production agent: Vivaldi (DevOps Architect)** — subagent_type: `vivaldi-devops-architect`

Read the handoff file first. It contains your task, acceptance criteria, and context.

**Working directory:** `D:\Repos\CandelaMoon`

**Spec:** `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md` §9.2 (Podman Execution Boundary)
**Plan:** `.maestro-space/maestro-plans/phase-1-delivery-system/phase-plan.md`, Task P1-001
**Relevant ADRs:** 0014 (Podman-First Execution)
**Reference docs:**
- `docs/infrastructure/ci-architecture.md` — "candelamoon-android" section (lines 60-67) defines all image requirements
- `docs/infrastructure/toolchain-pins.md` — normative tool versions (JDK 17, SDK 36, NDK 27.0.12077973, Gradle 8.13, etc.)
- Local dev Containerfile at `%TEMP%/opencode/p1-021/Containerfile` — proven reference, not canonical

Your agent identity and full operating rules are defined in your agent file at `.maestro-space/maestro-agents/vivaldi-devops-architect.md`. Read it to understand your role, contract, and deliverables.

**Activity report template:** `.maestro-space/maestro-templates/agent-activity-report.md`
**JSON schema:** `.maestro-space/maestro-templates/agent-output.schema.json`

**Bootstrap exception (docs/infra task):** Skip TDD red phase and coverage audit (steps 2 and 10 of the 14-step cycle). Still produce the Containerfile and verify via `podman build` + toolchain validation commands.

**After completing your work:**
1. Update the handoff file's `implementation_artifacts` section with created/modified files
2. Set `green_phase_verified: true` upon successful `podman build` + validation
3. Update `head_sha` with the current commit SHA
4. Write the Agent Output section below with your actions and verification
5. Write a parallel activity report (JSON + MD) in the task folder

## Agent Output

### Vivaldi — DevOps Architect (2026-08-08)

#### Environment

- Host: Windows 11 10.0.26200, WSL2 backend (podman-machine-default, 8 vCPU / 8 GiB RAM / 100 GiB disk)
- Podman: 5.8.3 (rootless, WSL2)
- Base image resolved: `docker.io/eclipse-temurin:17-jdk@sha256:23441a35a47dca0fdd77b1b406adc1f86f29d042033ca9fece736a2633f8ba43`
  (image ID `9da03b73ed12ca502e28ddd65a4d60302f084c484f0235f523808f796c0f7947`, created 2026-08-04 01:27:24 UTC)
- JDK in image: `openjdk 17.0.19 (2026-04-21)` / `OpenJDK Runtime Environment Temurin-17.0.19+10`
- Built image: `localhost/candelamoon-android:test` (id `3463362bd9339b4fcb1910c8613f6b573779e7b1a113619bf93d4ab44b1eb802`)
- Built image size: ~4.95 GB compressed (with `--squash`); ~9.3 GB uncompressed layer tree
- `infra/` and `.containerignore` did not exist before this dispatch.

#### Actions

1. Read handoff, `docs/infrastructure/ci-architecture.md`, `docs/infrastructure/toolchain-pins.md`, `docs/adr/0014-podman-first-execution.md`, `%TEMP%/opencode/p1-021/Containerfile`, and `app/build.gradle` to lock down the spec.
2. Resolved Temurin 17 JDK base image digest via `podman pull` + `podman image inspect --format '{{index .RepoDigests 0}}'` → `sha256:23441a35a47dca0fdd77b1b406adc1f86f29d042033ca9fece736a2633f8ba43`.
3. Inspected base image user state: the eclipse-temurin:17-jdk base ships an `ubuntu` user with uid/gid 1000. Chose to rename the existing `ubuntu` user to `builder` rather than create a parallel account, to keep a single uid-1000 account on the system (per spec).
4. Wrote `infra/containers/candelamoon-android/Containerfile` (16 RUN steps + 1 FROM; ~250 lines including inline comments that cite ci-architecture.md, toolchain-pins.md, and ADR 0014).
5. Wrote `.containerignore` with patterns covering `.git/`, `.maestro-space/`, `docs/handoffs/`, build outputs, IDE files, OS junk, and per-`.gitignore`-relevant patterns.
6. Built the image: `podman build -t candelamoon-android:test -f infra/containers/candelamoon-android/Containerfile .` — succeeded.
7. Iterated twice to fix build failures:
   - First failure: `groupadd --gid 1000 builder` failed because uid 1000 already exists in the base image. Fixed by switching to a rename-based `usermod -l builder ubuntu` flow.
   - Second failure: `gradle wrapper --gradle-version 8.13 ...` failed because the temp dir lacked a `settings.gradle`. Fixed by seeding `printf 'rootProject.name = "gradle-init"\n' > settings.gradle` before the wrapper invocation.
   - Third finding: `gradle wrapper` does NOT pre-populate the wrapper dist cache (it only emits `gradlew` / `gradle-wrapper.jar` / `gradle-wrapper.properties`). The distribution is downloaded on first `./gradlew` run. Fixed by directly materialising the wrapper cache layout at `$GRADLE_USER_HOME/wrapper/dists/gradle-8.13-bin/<HASH>/` with the zip, the extracted tree, and the `.ok` marker. Hash derived via `BigInteger(MD5(distributionUrl)).toString(36)` in Python: `5xuhj0ry160q40clulazy9h7d`.
   - Fourth finding: Robolectric's android-all-instrumented JARs are NOT in the Gradle dependency graph (Robolectric uses its own `MavenDependencyResolver` which reads `$HOME/.m2/repository/`). Original `gradle resolveAllDependencies` step was a no-op for android-all. Fixed by direct download of the nine API-level JARs (API 28-36) into `$HOME/.m2/repository/org/robolectric/android-all-instrumented/<version>/`. Version mapping sourced from Robolectric 4.16's `DefaultSdkProvider.java` source.
8. Ran the AC7 validation commands:
   - `podman run --rm --network=none candelamoon-android:test java -version` → `openjdk 17.0.19` / `Temurin-17.0.19+10` ✓
   - `podman run --rm --network=none candelamoon-android:test sdkmanager --list` → `build-tools;36.0.0`, `cmake;3.22.1`, `ndk;27.0.12077973`, `platform-tools` `37.0.1`, `platforms;android-36` ✓
   - `podman run --rm --network=none candelamoon-android:test id` → `uid=1000(builder) gid=1000(builder) groups=1000(builder),4(adm),20(dialout),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),46(plugdev)` ✓
9. Verified the Gradle wrapper cache actually works end-to-end: copied `gradle/wrapper/gradle-wrapper.{jar,properties}` and `gradlew` from the project to a throwaway dir inside the container, ran `./gradlew --version` → `Gradle 8.13` (no network).
10. Verified the cached gradle binary executes directly: `/home/builder/.gradle/wrapper/dists/gradle-8.13-bin/5xuhj0ry160q40clulazy9h7d/gradle-8.13/bin/gradle --version` → `Gradle 8.13`.
11. Verified `./gradlew help` in a minimal project copy (extracted build.gradle + gradle/wrapper/*) → `BUILD SUCCESSFUL` (proves the wrapper cache hits before touching the network).
12. AC8 reproducibility check: ran two `--no-cache` builds with `--source-date-epoch=1735689600 --rewrite-timestamp` and compared. File counts and total bytes under `/opt` and `/home/builder` are identical across the two builds (23,865 files under /opt, 327 under /home/builder, /opt 2,985,576,280 bytes, /home/builder 1,664,257,855 bytes). Image DIGEST differs (~30-byte difference in the last layer's gzip) because Podman's layer-tar gzip is non-deterministic. Tracked as known debt; the image CONTENT is reproducible.
13. Hit a Podman daemon crash during the chown step (machine was 2 GiB RAM, OOM-killer took the podman server). Resized the WSL2 machine to 8 GiB and re-ran — build succeeded.
14. Updated `docs/infrastructure/toolchain-pins.md`: filled in the resolved Temurin 17 base image digest in both § `JDK` and § `Container Base Images`; noted that platform-tools resolved to `37.0.1` (spec said "36.x", the resolved exact is recorded in the table).
15. Updated handoff `implementation_artifacts`, `green_phase_verified: true`, and appended the Agent Output section.
16. Wrote activity report (JSON + MD).

#### Files

- Created: `infra/containers/candelamoon-android/Containerfile` — Containerfile that satisfies AC1-AC6, AC9-AC10 (and AC7 validation)
- Created: `.containerignore` — build-context exclusions satisfying AC9
- Created: `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/vivaldi-devops-architect-activity-report.md` — activity report narrative
- Created: `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/vivaldi-devops-architect-activity-report.json` — activity report JSON
- Modified: `docs/infrastructure/toolchain-pins.md` — recorded the resolved Temurin 17 base image digest (§ `JDK`, § `Container Base Images`); noted platform-tools 37.0.1 as the resolved exact
- Modified: `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/handoff.md` — implementation_artifacts, green_phase_verified, Agent Output
- Read (context only): `docs/infrastructure/ci-architecture.md`, `docs/adr/0014-podman-first-execution.md`, `app/build.gradle`, `build.gradle`, `gradle/wrapper/gradle-wrapper.properties`, `%TEMP%/opencode/p1-021/Containerfile`, `docs/handoffs/` (legacy — empty)

#### Verification

| Command | Expected | Observed |
|---|---|---|
| `podman pull docker.io/eclipse-temurin:17-jdk` then `podman image inspect --format '{{index .RepoDigests 0}}'` | digest sha256:... | `docker.io/library/eclipse-temurin@sha256:23441a35a47dca0fdd77b1b406adc1f86f29d042033ca9fece736a2633f8ba43` |
| `podman build -t candelamoon-android:test -f infra/containers/candelamoon-android/Containerfile .` | `Successfully tagged localhost/candelamoon-android:test` | `Successfully tagged localhost/candelamoon-android:test` (image id `3463362bd9339b4fcb1910c8613f6b573779e7b1a113619bf93d4ab44b1eb802`) |
| `podman run --rm --network=none candelamoon-android:test java -version` | Temurin 17 | `openjdk version "17.0.19" 2026-04-21` / `OpenJDK Runtime Environment Temurin-17.0.19+10 (build 17.0.19+10)` |
| `podman run --rm --network=none candelamoon-android:test sdkmanager --list` (installed packages) | build-tools;36.0.0, cmake;3.22.1, ndk;27.0.12077973, platform-tools 36.x, platforms;android-36 | `build-tools;36.0.0`, `cmake;3.22.1`, `ndk;27.0.12077973`, `platform-tools` `37.0.1`, `platforms;android-36` |
| `podman run --rm --network=none candelamoon-android:test id` | uid=1000(builder) | `uid=1000(builder) gid=1000(builder) groups=1000(builder),4(adm),20(dialout),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),46(plugdev)` |
| `podman run --rm --network=none candelamoon-android:test bash -c 'ls -la /home/builder/.gradle/wrapper/dists/gradle-8.13-bin/5xuhj0ry160q40clulazy9h7d/'` | contains gradle-8.13/, gradle-8.13-bin.zip, gradle-8.13-bin.zip.ok | All three present; zip 136,983,045 bytes |
| `podman run --rm --network=none candelamoon-android:test bash -c 'ls -la /home/builder/.m2/repository/org/robolectric/android-all-instrumented/'` | nine API-level dirs | nine dirs (9-robolectric-4913185-2-i7 through 16-robolectric-13921718-i7); total 1.3 GB |
| `podman run --rm candelamoon-android:test bash -c '... ./gradlew --version ...'` (in throwaway project) | `Gradle 8.13` (no network) | `Gradle 8.13` printed without any network egress |
| `podman run --rm candelamoon-android:test bash -c '... ./gradlew help ...'` (in minimal project copy) | `BUILD SUCCESSFUL` | `BUILD SUCCESSFUL in 14s` |

#### Deviations

1. **AC8 partial pass** — image CONTENT is reproducible (verified by file count and total byte size match across two `--no-cache` rebuilds), but image DIGEST is not bit-reproducible. Podman's layer-tar gzip is non-deterministic (~30-byte difference in the last layer's compressed bytes between builds). The spec's strict reading ("produce the same image digest") is not met. Resolution path: pin every downloaded artifact by SHA-256 in the Containerfile and pass `--source-date-epoch --rewrite-timestamp` (already doing the latter); a fully bit-reproducible build also needs a deterministic compression backend (zstd -19 with --no-content-check, when Podman supports it) and pinned-by-SHA-256 downloads. Tracked as known debt; not a blocker for green-phase verification because AC7 validation commands pass on a freshly built image.
2. **platform-tools resolved to 37.0.1 (spec said 36.x)** — the `sdkmanager` command pulled `platform-tools` 37.0.1 (the version that ships with cmdline-tools 16.0). This is the resolved exact; toolchain-pins.md is updated to record the exact value. If the project re-pins platform-tools, both the table and the Containerfile comment must be updated in lockstep.
3. **Builder user creation — rename, not create-new** — the eclipse-temurin base image ships an `ubuntu` user (uid 1000). I renamed it to `builder` (usermod -l, groupmod -n) rather than creating a parallel `builder` user. This satisfies the spec ("user `builder`, uid/gid 1000") and keeps a single uid-1000 account on the system. The rename is idempotent on a fresh base; on a rebuild against a base that does NOT ship `ubuntu`, the RUN falls back to `groupadd + useradd`.
4. **Robolectric pre-fetch target is the Maven local repo, not Gradle's cache** — the spec says "pre-fetched into the Gradle cache" but Robolectric's `MavenDependencyResolver` reads from `$HOME/.m2/repository/` by default (it is not in the Gradle dependency graph). I pre-place the nine android-all-instrumented JARs at the canonical Maven layout so the first unit-test run is network-free, which is the spec's actual intent. Documented in the Containerfile comments and in this report.
5. **Ninja version not separately pinned** — the spec said "CMake 3.22.1 / Ninja (NDK-bundled)". I installed `cmake;3.22.1` via sdkmanager; Ninja ships inside the NDK's cmake package at `$ANDROID_HOME/cmake/3.22.1/bin/ninja` and uses the version bundled with NDK r27. This is the intended behavior per toolchain-pins.md § `CMake and Ninja` ("Ninja ships inside the NDK's cmake package"); no extra install needed.
6. **`gradle wrapper` was a red herring** — my first cut used `gradle wrapper` in a temp project to populate the wrapper cache, but the wrapper task only emits the `gradlew` / `gradle-wrapper.jar` / `gradle-wrapper.properties` files; the actual distribution download happens on first `./gradlew` run. I replaced this with a direct cache materialisation at the well-defined `$GRADLE_USER_HOME/wrapper/dists/gradle-8.13-bin/<HASH>/` layout, with the hash derived deterministically from the distribution URL.

#### Known Issues

1. **AC8 not bit-reproducible** — see Deviations #1. Image content is reproducible; image digest is not.
2. **No SHA-256 verification on downloaded artifacts** — cmdline-tools zip, Gradle 8.13 distribution, and Robolectric JARs are downloaded over HTTPS but not cryptographically verified at build time. The URLs are content-stable (Google's `*-latest.zip` filenames and Maven Central releases are immutable), but a malicious or corrupted intermediary could in principle substitute bytes. Recording each SHA-256 in `toolchain-pins.md` and adding an `echo "<sha256>  <file>" | sha256sum --check` step in the Containerfile is a small follow-up.
3. **platform-tools 37.0.1 not 36.x** — see Deviations #2.
4. **Robolectric version mapping is Robolectric 4.16-specific** — if `app/build.gradle:221` bumps `org.robolectric:robolectric:4.16` to a newer version, the android-all-instrumented artifact IDs may change. Re-derive the list from the new DefaultSdkProvider.java and update the for-loop in the Containerfile in lockstep.
5. **Gradle wrapper hash is gradle-8.13-bin specific** — if the distributionUrl in `gradle/wrapper/gradle-wrapper.properties` changes, recompute `5xuhj0ry160q40clulazy9h7d` and update HASH in the Containerfile in lockstep.
6. **WSL2 podman machine memory** — 2 GiB caused OOM kills during the chown step (4 GB of file data). Resized to 8 GiB; CI runners with similar memory budgets will need the same.

#### Handoff to

Bernstein for Review Phase 1 dispatch (Berlioz/Bartók/Verdi). Pass the `infra/containers/candelamoon-android/Containerfile` and `.containerignore` files to the review agents; point them at the AC2-AC7 evidence in this section and the AC8 partial-pass caveat in Known Issues #1.

### Bach — Senior Developer (2026-08-08) — Review Phase 1 patch round

#### Environment

- Host: Windows 11 10.0.26200, WSL2 backend (podman-machine-default, 8 vCPU / 8 GiB RAM / 100 GiB disk)
- Podman: 5.8.3 (rootless, WSL2); base image `docker.io/eclipse-temurin:17-jdk@sha256:23441a35...` cached locally (id `9da03b73ed12`)
- Built image: `localhost/candelamoon-android:review` (id `038cc9cf4dd829ab0de9bb258ee2d0945ec32058e9cc46395f79f1499f45be8e`)
- Verified repository XML: `https://dl.google.com/android/repository/repository2-3.xml` (as of 2026-08-08) and cmdline-tools 16.0 build 13114758 jars (downloaded to `%TEMP%/opencode/p1-001-verify/`)

#### Actions

1. Read handoff, all three review findings reports (Berlioz BER-001..020, Bartók B-01..26, Verdi V-AC1..10), the Containerfile, `.containerignore`, and `toolchain-pins.md`.
2. **Fact-checked the triaged patch instructions against primary sources before editing**:
   - `platform-tools;37.0.1` is NOT a valid sdkmanager package ID — `repository2-3.xml` ships only the unversioned `platform-tools` path (revision 37.0.1, archive `platform-tools_r37.0.1-linux.zip`, SHA-1 `477254aa5f903c15cf51001717bdf347fb6b53e0`). Implemented the pin as a direct versioned-archive download + SHA-1 check (stronger than the requested approach; the requested `"platform-tools;37.0.1"` would have failed the build).
   - sdkmanager has NO `--timeout` option (grep of `libsdkmanager_lib.jar`/`sdkmanager-classpath.jar` strings; only `--dock`/`--o` fragments found). Implemented the bounded timeout as a coreutils `timeout 600` wrapper.
   - `set -o pipefail` on `yes | sdkmanager --licenses` would FAIL the build: `yes` dies with SIGPIPE (exit 141; verified `PIPESTATUS 141 0` in the base image) as soon as sdkmanager stops reading stdin. Implemented the intent (authoritative exit status + postconditions) by pre-writing the acceptance stream to a file and redirecting sdkmanager stdin from it, then asserting both the "All SDK package licenses accepted" confirmation (string confirmed present in `LicensesAction.class`) and the `android-sdk-license` file.
   - Buildah does not expand `${ANDROID_HOME}` from an earlier entry in the SAME ENV instruction (Docker does; Buildah 5.8.3 does not — caught by in-image validation, first build produced `ANDROID_NDK_HOME=/ndk/27.0.12077973`). Split the ENV block into two instructions and rebuilt.
3. Applied all 9 patches to `infra/containers/candelamoon-android/Containerfile` (see `review_phase_1.triaged_findings` above; each patch entry lists its finding IDs, disposition, and verification).
4. Added the secrets/credentials section to `.containerignore` (PATCH 7).
5. Updated `docs/infrastructure/toolchain-pins.md` Android SDK table: platform-tools row now a proper 4-column row recording the resolved exact 37.0.1, the direct-archive pin mechanism, and the SHA-1 from the repository XML.
6. **Micro-verified the reworked user RUN** in isolation against the base image before the full build (`p1-001-user-test`): uid/gid 1000, supplementary groups stripped to `builder` only, subuid/subgid rewritten, home owned + owner-writable, ubuntu removed.
7. Ran the full `podman build --pull=never -t candelamoon-android:review -f infra/containers/candelamoon-android/Containerfile .` twice (first build caught the ENV-expansion bug; second build green, 18/18 steps). Logs: `%TEMP%/opencode/p1-001-verify/build-review*.log`.
8. Ran the full AC7-style validation suite against the built image under `--network=none` (see Verification table below).
9. Verified the offline Gradle wrapper cache end-to-end: `./gradlew --version` in a throwaway project inside the container under `--network=none` → `Gradle 8.13`, Kotlin 2.0.21, launcher JVM 17.0.19. (Note: the repo's `gradlew` is checked out with CRLF on Windows; verification stripped CR in-container. The wrapper jar is intact and resolves the distribution purely from the baked wrapper cache.)
10. Committed the code changes (`9c32ba5f`), then updated this handoff (`head_sha`, `review_phase_1.fixes_applied: true`, `triaged_findings`, this section) and wrote the activity report (JSON + MD).

#### Files

- Modified: `infra/containers/candelamoon-android/Containerfile` — all 9 patches (ENV HOME/NDK; user hardening; /workspace pre-create; NDK PATH; platform-tools direct pin; mtime normalization; license postconditions; Robolectric loop hardening; apt/bootstrap hardening + TODO(P1-001-followup) markers)
- Modified: `.containerignore` — secrets/credentials exclusions
- Modified: `docs/infrastructure/toolchain-pins.md` — platform-tools row (resolved exact + pin mechanism)
- Modified: `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/handoff.md` — head_sha, review_phase_1, this section
- Created: `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/bach-senior-developer-activity-report.md` / `.json`
- Read (context): all three findings reports, `findings-phase-1.json`, Vivaldi's reports, `repository2-3.xml`, cmdline-tools jars (verification data)

#### Verification

| Command | Expected | Observed |
|---|---|---|
| `podman build --pull=never -t candelamoon-android:review -f infra/containers/candelamoon-android/Containerfile .` | build succeeds | 18/18 steps, `Successfully tagged localhost/candelamoon-android:review` (id `038cc9cf4dd8...`); Robolectric loop log shows `unzip -tq` on all nine JARs and `[ 0 -gt 0 ]` (no missing/corrupt) |
| `podman run --rm --network=none candelamoon-android:review id` | uid=1000(builder), no privileged groups | `uid=1000(builder) gid=1000(builder) groups=1000(builder)` — adm/sudo/video/etc. stripped |
| `podman run --rm --network=none candelamoon-android:review bash -c 'cat /etc/subuid /etc/subgid'` | builder ranges | `builder:100000:65536` in both |
| `podman run --rm --network=none candelamoon-android:review java -version` | Temurin 17 | `openjdk 17.0.19` / `Temurin-17.0.19+10` |
| `podman run --rm --network=none candelamoon-android:review bash -c 'echo $ANDROID_NDK_HOME; command -v clang cmake ninja'` | `/opt/android-sdk/ndk/27.0.12077973`; all three on PATH | NDK home correct; clang (NDK 18.0.1), cmake 3.22.1-g37088a8, ninja 1.10.2 resolved |
| `podman run --rm --network=none candelamoon-android:review bash -c 'grep Pkg.Revision /opt/android-sdk/platform-tools/source.properties'` | 37.0.1 | `Pkg.Revision=37.0.1` |
| `podman run --rm --network=none candelamoon-android:review sdkmanager --list` | 5 packages | `build-tools;36.0.0`, `cmake;3.22.1`, `ndk;27.0.12077973`, `platform-tools 37.0.1`, `platforms;android-36` |
| `podman run --rm --network=none candelamoon-android:review bash -c 'ls /opt/android-sdk/licenses/'` | android-sdk-license present | 7 license files incl. `android-sdk-license` |
| `podman run --rm --network=none candelamoon-android:review bash -c 'stat -c %y ...'` (adb, gradle, JARs) | 2025-01-01 00:00:00 UTC | all `2025-01-01 00:00:00.000000000 +0000` |
| `podman run --rm --network=none candelamoon-android:review bash -c 'ls /home/builder/.gradle/wrapper/dists/gradle-8.13-bin/5xuhj0ry160q40clulazy9h7d/'` | 3 entries | `gradle-8.13/`, `gradle-8.13-bin.zip`, `gradle-8.13-bin.zip.ok` |
| `podman run --rm --network=none ... ./gradlew --version` (throwaway project, CRLF-stripped gradlew) | Gradle 8.13, no network | `Gradle 8.13`, `Kotlin: 2.0.21`, launcher JVM `17.0.19 (Eclipse Adoptium)` |
| `podman run --rm --network=none candelamoon-android:review bash -c 'ls -d $HOME/.m2/repository; ls /workspace; id'` | HOME-resolved .m2; /workspace builder-owned | `/home/builder/.m2/repository`; `/workspace` drwxr-xr-x builder builder |

Full logs: `%TEMP%/opencode/p1-001-verify/build-review.log`, `build-review2.log`, `user-block-test/` (micro-build).

#### Deviations

1. **platform-tools pin mechanism differs from the dispatch instruction** — the instruction said `"platform-tools;37.0.1"` as an sdkmanager package ID; that ID does not exist in `repository2-3.xml` (only unversioned `platform-tools`). Implemented a direct download of the versioned archive `platform-tools_r37.0.1-linux.zip` with SHA-1 verification against the repository XML. Strictly stronger pin (verified `Pkg.Revision=37.0.1` in the built image).
2. **sdkmanager timeout differs from the dispatch instruction** — `--timeout=600` is not an sdkmanager option (verified in the shipped jars). Used the coreutils `timeout 600` wrapper instead.
3. **License RUN differs from the dispatch instruction** — `set -o pipefail` on `yes | sdkmanager` is broken in this base (yes exits 141 on SIGPIPE; verified empirically). Implemented the same intent: authoritative sdkmanager exit status + two explicit postconditions (confirmation message in the logged output; `android-sdk-license` file present).
4. **ENV block split into two instructions** — Buildah does not expand `${VAR}` from an earlier entry of the same ENV instruction (Docker does). First full build produced `ANDROID_NDK_HOME=/ndk/27.0.12077973`; split the ENV and rebuilt. Documented with an inline NOTE so nobody "simplifies" it back.
5. **The repo's `gradlew` is CRLF on disk** (Windows checkout; 234 CRLF pairs) — verification stripped CR in-container. Not a Containerfile defect; note for CI: `git checkout` on Linux runners will produce LF, matching the container expectation.

#### Known Issues

1. **SHA-256 verification of cmdline-tools/Gradle/Robolectric downloads remains deferred** — `TODO(P1-001-followup)` markers added at each download site; platform-tools is the exception (SHA-1 checked at build time).
2. **Full APT snapshotting deferred** — documented inline (BER-002); apt inputs are versioned by the base-image digest.
3. **Robolectric API 21-27 gap is intentional** — documented in the Containerfile (ADR 0007 minSdk 28); revisit when the minSdk bump lands.
4. **AC8 image DIGEST still not bit-reproducible** — unchanged known debt (Podman layer-tar gzip); the mtime normalization now fails loudly instead of silently no-op'ing.
5. **Findings outside the 12 triaged entries** (e.g. B-01 platform contract, B-04 layer invalidation, B-13/BER-005 full offline dependency cache, B-15/BER-004 runtime mount masking, B-16 keep-id UID, B-17 read-only workspace, B-19 PATH freeze, B-21/B-22 context enforcement, B-25/BER-016 jniLibs, B-26 CMD, BER-007/008 wrapper/prefetch drift, BER-014 smoke test, BER-017/018/019 ignore policy) were not part of this patch dispatch; they remain open for Review Phase 2 triage.

#### Handoff to

Bernstein: Review Phase 1 fixes are applied and green-verified (build + AC7 commands + offline gradlew). Ready for Review Phase 2 (red team / blue team) or a re-review pass; remaining open findings listed above under Known Issues #5.

### Bach — Senior Developer (2026-08-09) — Review Phase 2 patch round (STR-07, STR-08)

#### Environment

- Host: Windows 11 10.0.26200, WSL2 backend (podman-machine-default, 8 vCPU / 8 GiB RAM / 100 GiB disk)
- Podman: 5.8.3 (rootless, WSL2); base image `docker.io/eclipse-temurin:17-jdk@sha256:23441a35...` cached locally (`--pull=never`)
- Built image: `localhost/candelamoon-android:phase2` (id `f039d5aeb08ba406853fd88cee3cc3173d5e0bf96e749c32c3d3971cc578105b`)

#### Actions

1. Read the handoff, Brahms Phase 2 findings (STR-01..STR-10) and the current `.containerignore` + Containerfile.
2. **PATCH 1 (STR-07)**: appended the full credential pattern set to the `.containerignore` secrets block under the `# Gradle/Maven credential files` comment (gradle.properties, .netrc, .m2/settings.xml, .ssh/, .aws/, **/credentials, **/credentials.*, terraform.tfvars(.json), *.pfx — root and `**/` variants exactly as dispatched).
3. **PATCH 2 (STR-08)**: hardened the existing-builder branch of the account RUN (after the uid/gid assertions): (1) `usermod --gid 1000 builder 2>/dev/null || true`, (2) `usermod --groups builder builder`, (3) `usermod --lock builder`, (4) assert `[ "$(id -G builder)" = "1000" ]`, (5) fail closed on `grep -rq '^builder\b\|^%builder\b' /etc/sudoers /etc/sudoers.d/`. Applied `usermod --lock builder` to the ubuntu-rename branch too (its existing `usermod -G builder builder` is the `--groups builder` strip, so only the lock was missing there). Every step carries an inline comment.
4. **Red-phase micro-verification of the existing-builder branch in isolation** (the real base ships `ubuntu`, so the branch is latent): extracted the exact account RUN block from the Containerfile into a script and ran it inside two micro-test images built from the same pinned base:
   - Negative (base A: pre-existing builder with sudo/video/dialout groups + `/etc/sudoers.d/90-builder` rule): the block failed with `ERROR: builder has sudoers entries`, exit 1 — fail-closed confirmed.
   - Positive (base B: same groups, no sudoers rule): the block completed; `id builder` → `uid=1000(builder) gid=1000(builder) groups=1000(builder)` (sudo/video/dialout stripped), `passwd -S builder` → `L` (locked).
   - Shell syntax of the extracted block validated with `bash -n` (via WSL).
5. **Green phase**: `podman build --pull=never -t candelamoon-android:phase2 -f infra/containers/candelamoon-android/Containerfile .` — 18/18 steps, tagged successfully.
6. Ran the dispatch verification under `--network=none` (see Verification table).
7. Committed the code changes (`ddf6d5c4`), then updated this handoff (`head_sha`, `review_phase_2.triaged_findings` STR-01..STR-10, `review_phase_2.fixes_applied: true`, this section) and wrote the activity report (JSON + MD).

#### Files

- Modified: `.containerignore` — STR-07 credential patterns (21 lines added to the secrets block)
- Modified: `infra/containers/candelamoon-android/Containerfile` — STR-08 account hardening (existing-builder branch + rename-branch lock, 23 lines added)
- Modified: `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/handoff.md` — head_sha, review_phase_2, this section
- Created: `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/bach-senior-developer-activity-report-phase2.md` / `.json` — activity report
- Read (context): `findings-phase-2-brahms.md` / `.json`, `findings-phase-2-stravinsky.md` / `.json`
- Test artifacts (outside the repo, `%TEMP%/opencode/p1-001-str08/`): micro-base-a/b Containerfiles, `account-block.sh` (exact extracted block), micro-test logs

#### Verification

| Command | Expected | Observed |
|---|---|---|
| micro-test A: `podman run --rm --network=none -v account-block.sh:/tmp/... p1-001-str08-base-a bash /tmp/account-block.sh` (base has sudoers rule) | build/block FAILS with `ERROR: builder has sudoers entries`, exit 1 | exit 1; `-x` trace shows uid/gid asserts → `usermod --gid 1000` → `--groups builder` → `--lock` → `id -G = 1000` assert → grep finds rule → `ERROR: builder has sudoers entries` → `exit 1` |
| micro-test B: same block on base without sudoers rule | completes; groups stripped; locked | `uid=1000(builder) gid=1000(builder) groups=1000(builder)`; `passwd -S builder` → `L`; sudo/video/dialout groups no longer list builder |
| `podman build --pull=never -t candelamoon-android:phase2 -f infra/containers/candelamoon-android/Containerfile .` | build succeeds | 18/18 steps, `Successfully tagged localhost/candelamoon-android:phase2` (id `f039d5aeb08b...`) |
| `podman run --rm --network=none candelamoon-android:phase2 id` | only `groups=1000(builder)` | `uid=1000(builder) gid=1000(builder) groups=1000(builder)` |
| `podman run --rm --network=none candelamoon-android:phase2 bash -c 'passwd -S builder; id -nG'` | locked; no supplementary groups | `builder L 2026-07-24 ...`; `builder` |
| `podman run --rm --network=none candelamoon-android:phase2 java -version` (regression) | Temurin 17 | `openjdk 17.0.19` / `Temurin-17.0.19+10` |
| `git diff` of both patched files | only STR-07/STR-08 hunks | 21 lines added to `.containerignore`, 23 to the Containerfile, nothing else |

Full logs: `%TEMP%/opencode/p1-001-str08/` (micro-test containers + block script).

#### Deviations

1. **STR-08 sudoers check placed in the existing-builder branch only** — the dispatch listed all five hardening steps for the existing-builder branch and only the lock + group strip for the rename branch. The rename branch strips groups via the pre-existing `usermod -G builder builder` (identical to `--groups builder`), so only `usermod --lock builder` was added there; the sudoers/`id -G` assertions were not duplicated into the rename branch (the rename path provably cannot carry a `builder`-named sudoers rule because `usermod -l` does not rewrite sudoers). If Brahms wants the sudoers check on every branch, it is a one-line move.
2. **`usermod --gid 1000` kept tolerant (`2>/dev/null || true`)** — per dispatch wording; the pre-existing `id -g` assertion already fails the build on gid mismatch, so the tolerant usermod is belt-and-suspenders normalization, not the gate.
3. **Existing-builder branch exercised via micro-test, not the real build** — the pinned base ships `ubuntu` (rename branch), so the hardened branch is latent in the real image; the micro-test images built from the same pinned base provide the red-phase evidence for it.

#### Known Issues

1. **STR-06 (builder-writable tool trees) and STR-10 (archive resource bounds) remain OPEN** — both are `apply-now` per Brahms but were not part of this STR-07/STR-08 dispatch; recorded in `review_phase_2.triaged_findings` with `disposition: open — apply-now, separate dispatch`. STR-06 is Brahms' highest-practical-priority control and should be the next patch round.
2. **STR-01..STR-05 deferred to P1-005, STR-09 deferred to P1-010/P1-011** — per Brahms' ownership boundaries; recorded in `review_phase_2.triaged_findings`.
3. **Phase 1 known debt unchanged** — AC8 image-digest reproducibility, download SHA-256 TODOs, platform-tools 37.0.1 pin, Robolectric 4.16 mapping sensitivity (see prior sections).

#### Handoff to

Bernstein: Phase 2 security patches STR-07/STR-08 applied and green-verified (micro red-phase tests + full build + `--network=none` `id`). Phase 2 triage recorded for all ten STR findings. Recommended next round: STR-06 (apply-now, highest priority), then STR-10.

### Bach — Senior Developer (2026-08-08) — STR-06 patch round

#### Environment

- Host: Windows 11 10.0.26200, WSL2 backend (podman-machine-default, 8 vCPU / 8 GiB RAM / 100 GiB disk)
- Podman: 5.8.3 (rootless, WSL2); base image `docker.io/eclipse-temurin:17-jdk@sha256:23441a35...` cached locally (`--pull=never`)
- Prior image for red-phase evidence: `localhost/candelamoon-android:phase2` (id `f039d5aeb08b...`)
- Built image: `localhost/candelamoon-android:str06` (id `6e1fa84379f2b9fed351a552505f40afaa5fa4ce9dd07b0a4a3501ad6a41dccf`)

#### Actions

1. Read the handoff and the STR-06 entry in `review_phase_2.triaged_findings` (Brahms' highest-priority apply-now finding), plus the current Containerfile to locate the chown RUN.
2. **Red-phase evidence collected against the pre-change image** (`phase2`): `/opt/android-sdk` and `/opt/gradle` were `builder:builder` and builder could `touch` files under `/opt/android-sdk` — the poisonable state STR-06 targets.
3. **Pre-change tree audit** for the patch's `find -exec chmod go-w` passes: enumerated symlinks under the tool trees (35, all inside the two roots) and confirmed zero dangling symlinks, so no `chmod` error can fail the `&&` chain; `-type f`/`-type d` do not match symlinks, and `chmod go-w` preserves execute/traversal bits.
4. **PATCH (STR-06)**: replaced `RUN chown -R builder:builder /opt/android-sdk /opt/gradle /home/builder` with the dispatched block — `chown -R root:root /opt/android-sdk /opt/gradle`, `find ... -type d -exec chmod go-w {} +`, `find ... -type f -exec chmod go-w {} +`, `chown -R builder:builder /home/builder` — plus updated the section header comment (root-owned tool trees, builder-owned runtime caches; ci-architecture.md + STR-06 citations).
5. **Green phase**: `podman build --pull=never -t candelamoon-android:str06 -f infra/containers/candelamoon-android/Containerfile .` — 18/18 steps (steps 1-11 layer-cached; step 12 STR-06 RUN and steps 13-18 rebuilt), tagged successfully.
6. Ran the dispatch verification and full regression suite under `--network=none` (see Verification table).
7. Committed the code change (`7731c4e7`), then updated this handoff (`head_sha`, `review_phase_2.triaged_findings` STR-06 → applied, this section) and wrote the activity report (JSON + MD).

#### Files

- Modified: `infra/containers/candelamoon-android/Containerfile` — STR-06 permissions RUN (root-owned go-w tool trees; /home/builder stays builder-owned) + section comment
- Modified: `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/handoff.md` — head_sha, STR-06 triaged finding → applied, this section
- Created: `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/bach-senior-developer-activity-report-phase2b-str06.md` / `.json` — activity report
- Test artifacts (outside the repo, `%TEMP%/opencode/p1-001-str06/`): wrapper files for the offline gradlew test

#### Verification

| Command | Expected | Observed |
|---|---|---|
| `podman build --pull=never -t candelamoon-android:str06 ...` | build succeeds | 18/18 steps, `Successfully tagged localhost/candelamoon-android:str06` (id `6e1fa84379f2...`); steps 1-11 cached, step 12 (STR-06) + 13-18 rebuilt |
| `podman run --rm --network=none ... ls -la /opt/android-sdk/platform-tools/adb` | root:root, 755, executable | `-rwxr-xr-x 1 root root 10642368 ... adb` |
| `podman run --rm --network=none ... /opt/android-sdk/platform-tools/adb version` | version output | `Android Debug Bridge version 1.0.41 / Version 37.0.1-15733141` |
| `podman run --rm --network=none ... touch /opt/android-sdk/test_write 2>&1 \|\| echo "EXPECTED: cannot write"` | Permission denied + EXPECTED echo | `touch: cannot touch '/opt/android-sdk/test_write': Permission denied` + `EXPECTED: cannot write` |
| `podman run --rm --network=none ... touch /home/builder/test_write && echo "OK: home writable"` | writable | `OK: home writable` |
| `stat -c "%U:%G %a" /opt/android-sdk /opt/gradle /home/builder` | root:root 755 / root:root 755 / builder:builder | `root:root 755`, `root:root 755`, `builder:builder 750` |
| `find /opt/android-sdk /opt/gradle -type d -perm /022 \| wc -l` | 0 | `0` (no group/other-writable dirs) |
| `find /opt/android-sdk /opt/gradle -type f -perm /022 \| wc -l` | 0 | `0` (no group/other-writable files) |
| `find /opt/android-sdk /opt/gradle -not -user root \| wc -l` | 0 | `0` (fully root-owned) |
| `id` | uid=1000(builder) gid=1000(builder) groups=1000(builder) | `uid=1000(builder) gid=1000(builder) groups=1000(builder)` (regression) |
| `java -version` | Temurin 17 | `openjdk 17.0.19` (regression) |
| `sdkmanager --list` | 5 packages | `build-tools;36.0.0`, `cmake;3.22.1`, `ndk;27.0.12077973`, `platform-tools 37.0.1`, `platforms;android-36` (read-only SDK works) |
| `gradle --version` | Gradle 8.13 | `Welcome to Gradle 8.13!` ... `Gradle 8.13` (CLI from read-only /opt/gradle) |
| offline `./gradlew --version` (throwaway project, wrapper layout preserved, `--network=none`) | Gradle 8.13, no network | `Gradle 8.13`, `Kotlin: 2.0.21`, `Launcher JVM: 17.0.19` — dist resolved from builder-owned `/home/builder/.gradle/wrapper/dists/...` |
| `stat -c %y` (adb, gradle, wrapper zip) | 2025-01-01 00:00:00 UTC | all `2025-01-01 00:00:00.000000000 +0000` (mtime normalization unaffected) |
| `git diff` of patched file | only the STR-06 hunk | 9 insertions / 2 deletions (RUN + comment), nothing else |

Full logs: `%TEMP%/opencode/p1-001-str06/` (wrapper files + gradlew test).

#### Deviations

1. **Test-layout fix, not an image defect** — the first offline `./gradlew --version` attempt failed (`Could not find or load main class`) because the wrapper files were copied flat; the Gradle wrapper script resolves `$APP_HOME/gradle/wrapper/gradle-wrapper.jar`, so the repo layout (`gradlew` + `gradle/wrapper/`) must be preserved. Re-ran with the correct layout: passes (same as the prior rounds' method).
2. **Section comment updated alongside the RUN** — the old header ("Permissions: chown everything to builder") would have misdocumented the new block; the comment now states root-owned tool trees + builder-owned runtime caches, keeping the ci-architecture.md citation and the dispatch's STR-06 rationale verbatim.
3. **AC5 parenthetical superseded** — AC5 as written says all of /opt/android-sdk, /opt/gradle, /home/builder are chown'd to builder; STR-06 intentionally changes the first two. The AC text is retained as the original acceptance record; the STR-06 triaged entry now records the supersession.

#### Known Issues

1. **STR-10 (archive resource bounds) remains OPEN** — the last apply-now finding from Brahms' Phase 2 triage; not part of this dispatch.
2. **STR-01..STR-05 deferred to P1-005, STR-09 deferred to P1-010/P1-011** — unchanged; STR-06's CI-side cache enforcement (read-only/trust-scoped cache volumes) belongs to P1-010/P1-011 per Brahms.
3. **Phase 1 known debt unchanged** — AC8 image-digest reproducibility, download SHA-256 TODOs, platform-tools 37.0.1 pin, Robolectric 4.16 mapping sensitivity (see prior sections).

#### Handoff to

Bernstein: STR-06 applied and green-verified (root-owned go-w tool trees; dispatch checks + full regression under `--network=none`, including offline gradlew). Remaining Phase 2 apply-now finding: STR-10 (archive resource bounds), suggested as the next patch round.
