# Activity Report — Bach (Senior Developer)

- **Agent**: Bach (Senior Developer) (`bach-senior-developer`)
- **Task**: P1-001 — Apply Phase 1 review patches to the candelamoon-android Containerfile
- **Branch**: `moonlight-noir`
- **Base SHA**: `2118b61cd1dc49d600b36f06f7d832d5a7b8b824`
- **Head SHA**: `9c32ba5f510cc3fae63e8c3792352cfaf0b5d3fd` (after this dispatch)
- **Date**: 2026-08-08
- **Dispatched by**: Bernstein (orchestrator)
- **task_id**: P1-001

---

## Environment

- Host: Windows 11 10.0.26200, WSL2 backend (podman-machine-default, 8 vCPU / 8 GiB RAM / 100 GiB disk)
- Podman: 5.8.3 (rootless, WSL2); base image `docker.io/eclipse-temurin:17-jdk@sha256:23441a35...` cached locally (id `9da03b73ed12`)
- Built image: `localhost/candelamoon-android:review` (id `038cc9cf4dd829ab0de9bb258ee2d0945ec32058e9cc46395f79f1499f45be8e`)
- Verification data: `repository2-3.xml` and cmdline-tools 16.0 build 13114758 jars downloaded to `%TEMP%/opencode/p1-001-verify/`

## Actions

1. Read the handoff, all three Review Phase 1 findings reports (Berlioz BER-001..020, Bartók B-01..26, Verdi V-AC1..10), the Containerfile, `.containerignore`, and `toolchain-pins.md`.
2. **Fact-checked the triaged patch instructions against primary sources** before touching the files (each check changed the implementation, see Deviations):
   - `platform-tools;37.0.1` is not a valid sdkmanager package ID — `repository2-3.xml` ships only the unversioned `platform-tools` path (revision 37.0.1, archive `platform-tools_r37.0.1-linux.zip`, SHA-1 `477254aa5f903c15cf51001717bdf347fb6b53e0`).
   - sdkmanager has no `--timeout` option (string scan of the shipped jars).
   - `yes` exits 141 (SIGPIPE) in the base image, so `set -o pipefail` on `yes | sdkmanager --licenses` would fail a successful acceptance (`PIPESTATUS 141 0` verified in-container).
   - The "All SDK package licenses accepted" confirmation string exists in `LicensesAction.class` (cmdline-tools 16.0 build 13114758).
   - Buildah 5.8.3 does not expand `${VAR}` from an earlier entry of the same ENV instruction (Docker does).
3. Applied **PATCH 1** — `ENV HOME=/home/builder` (BER-006, B-14).
4. Applied **PATCH 2** — reworked builder user RUN: uid/gid 1000 postcondition asserts on every branch, existing-builder identity validation, `usermod -G builder` supplementary-group strip, `/etc/subuid`+`/etc/subgid` rewrite, home ownership (stat) + owner-write (find) validation without su/PAM (BER-009, BER-010, B-08, B-09, B-10).
5. Applied **PATCH 3** — `RUN mkdir -p /workspace && chown builder:builder /workspace` before `USER builder` (BER-011).
6. Applied **PATCH 4** — `ANDROID_NDK_HOME` (own ENV instruction after `ANDROID_HOME`) + NDK LLVM toolchain and `cmake/3.22.1/bin` on PATH (B-18).
7. Applied **PATCH 5** — platform-tools 37.0.1 pinned by direct versioned-archive download with SHA-1 verification; `TODO(P1-001-followup)` SHA-256 markers at every download site; apt base-digest note; `toolchain-pins.md` Android SDK table updated (BER-001, BER-003, BER-020, B-03).
8. Applied **PATCH 6** — mtime normalization rewritten: direct `find ... -exec touch -h -d "@${SOURCE_DATE_EPOCH}" {} +`, no `/etc/hostname` filter, no error suppression (BER-012, BER-013, B-20).
9. Applied **PATCH 7** — secrets/credentials patterns added to `.containerignore` (BER-015, B-23).
10. Applied **PATCH 8** — Robolectric loop: continue-on-error download with per-item logging, `unzip -tq` validation of every JAR, fail-at-end if any missing/corrupt; API 21-27 gap documented as intentional (B-11, B-12).
11. Applied **PATCH 9** — apt `DEBIAN_FRONTEND=noninteractive` + `Acquire::Retries=3`; `rm -rf` stale `cmdline-tools/latest` before extraction; license postconditions (confirmation grep + license file); `timeout 600` wrapper (B-02, B-06, B-07).
12. Micro-verified the reworked user RUN in isolation (`p1-001-user-test` image) before the full build: uid/gid 1000, `groups=1000(builder)` only, subuid/subgid `builder:100000:65536`, `/home/builder` owner-writable, `ubuntu` removed.
13. Ran two full `podman build` runs. The first caught the Buildah ENV-expansion bug (`ANDROID_NDK_HOME=/ndk/27.0.12077973`); fixed by splitting the ENV block; the second build was green (18/18 steps). Logs: `%TEMP%/opencode/p1-001-verify/build-review{,-2}.log`.
14. Ran the full AC7-style validation suite under `--network=none` (see Verification).
15. Verified the offline Gradle wrapper cache end-to-end: `./gradlew --version` in a throwaway project under `--network=none` → `Gradle 8.13` / `Kotlin 2.0.21` / launcher JVM `17.0.19 (Eclipse Adoptium)` (repo `gradlew` is CRLF on disk; CR-stripped in-container for the test).
16. Committed the code changes (`9c32ba5f`), updated the handoff (`head_sha`, `review_phase_1.fixes_applied: true`, `triaged_findings` with the 9 patches + 3 defer/dismiss categories, Agent Output section), and wrote this report (JSON + MD).

## Files

- **Modified**: `infra/containers/candelamoon-android/Containerfile` — all 9 patches + `TODO(P1-001-followup)` markers
- **Modified**: `.containerignore` — secrets/credentials exclusions
- **Modified**: `docs/infrastructure/toolchain-pins.md` — platform-tools row (resolved exact + pin mechanism)
- **Modified**: `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/handoff.md` — head_sha, review_phase_1, Bach Agent Output
- **Created**: `bach-senior-developer-activity-report.md` / `.json` (this report)
- **Read** (context): all three findings reports, `findings-phase-1.json`, Vivaldi's reports, `repository2-3.xml`, cmdline-tools jars

## Verification

| Command | Expected | Observed |
|---|---|---|
| `podman build --pull=never -t candelamoon-android:review -f infra/containers/candelamoon-android/Containerfile .` | build succeeds | 18/18 steps; Robolectric loop `unzip -tq` on all nine JARs, `[ 0 -gt 0 ]` (no missing/corrupt) |
| `podman run --rm --network=none candelamoon-android:review id` | uid=1000(builder), no privileged groups | `uid=1000(builder) gid=1000(builder) groups=1000(builder)` — adm/sudo/video/etc. stripped |
| `podman run --rm --network=none candelamoon-android:review bash -c 'cat /etc/subuid /etc/subgid'` | builder ranges | `builder:100000:65536` in both files |
| `podman run --rm --network=none candelamoon-android:review java -version` | Temurin 17 | `openjdk 17.0.19` / `Temurin-17.0.19+10` |
| `echo $ANDROID_NDK_HOME; command -v clang cmake ninja` | NDK home; tools on PATH | `/opt/android-sdk/ndk/27.0.12077973`; clang (NDK 18.0.1), cmake 3.22.1-g37088a8, ninja 1.10.2 |
| `grep Pkg.Revision /opt/android-sdk/platform-tools/source.properties` | 37.0.1 | `Pkg.Revision=37.0.1` |
| `sdkmanager --list` (installed) | 5 packages | build-tools;36.0.0, cmake;3.22.1, ndk;27.0.12077973, platform-tools 37.0.1, platforms;android-36 |
| `ls /opt/android-sdk/licenses/` | android-sdk-license present | 7 license files incl. `android-sdk-license` |
| `stat -c %y` on adb / gradle / JARs | 2025-01-01 00:00:00 UTC | `2025-01-01 00:00:00.000000000 +0000` on all sampled paths |
| wrapper dist `ls` | 3 entries | `gradle-8.13/`, `gradle-8.13-bin.zip`, `gradle-8.13-bin.zip.ok` |
| `./gradlew --version` (throwaway project, `--network=none`) | Gradle 8.13, no network | `Gradle 8.13`, `Kotlin: 2.0.21`, launcher JVM `17.0.19 (Eclipse Adoptium)` |
| `ls -d $HOME/.m2/repository; ls -ld /workspace` | HOME-resolved .m2; builder-owned /workspace | `/home/builder/.m2/repository`; `/workspace` drwxr-xr-x builder builder |

Full logs: `%TEMP%/opencode/p1-001-verify/build-review.log`, `build-review2.log`, `user-block-test/` (micro-build).

## Deviations

1. **platform-tools pin mechanism** — the dispatch said `"platform-tools;37.0.1"` as an sdkmanager package ID; that ID does not exist in `repository2-3.xml`. Implemented a direct download of the versioned archive `platform-tools_r37.0.1-linux.zip` with SHA-1 verification against the repository XML — a strictly stronger pin (in-image `Pkg.Revision=37.0.1`).
2. **sdkmanager timeout** — `--timeout=600` is not an sdkmanager option (verified in the shipped jars); used the coreutils `timeout 600` wrapper.
3. **License RUN** — `set -o pipefail` on `yes | sdkmanager` is broken in this base (`yes` exits 141 on SIGPIPE). Implemented the same intent: acceptance stream pre-written to a file and redirected to sdkmanager stdin, sdkmanager's exit status authoritative, plus two postconditions (confirmation message in the logged output; `android-sdk-license` file present).
4. **ENV block split into two instructions** — Buildah does not expand `${VAR}` from an earlier entry of the same ENV instruction. First full build produced `ANDROID_NDK_HOME=/ndk/27.0.12077973`; split the ENV and rebuilt. Inline NOTE added so nobody re-merges it.
5. **Repo `gradlew` is CRLF on disk** (Windows checkout) — verification CR-stripped it in-container. Not a Containerfile defect; Linux CI checkouts produce LF.

## Known Issues

1. **SHA-256 verification of cmdline-tools/Gradle/Robolectric downloads deferred** — `TODO(P1-001-followup)` markers at each download site; platform-tools is the exception (SHA-1 verified at build time).
2. **Full APT snapshotting deferred** (BER-002) — apt inputs are versioned by the base-image digest, documented inline.
3. **Robolectric API 21-27 gap intentional** (ADR 0007 minSdk 28) — documented in the Containerfile; revisit when the minSdk bump lands.
4. **AC8 image DIGEST still not bit-reproducible** — unchanged known debt (Podman layer-tar gzip); the mtime normalization now fails loudly instead of silently no-op'ing.
5. **Findings outside the 12 triaged entries remain open** (B-01, B-04, B-05, B-13, B-15, B-16, B-17, B-19, B-21, B-22, B-24, B-25, B-26, BER-004, BER-005, BER-007, BER-008, BER-014, BER-016, BER-017, BER-018, BER-019, V-AC6) — for Review Phase 2 triage.

## Handoff to

Bernstein: Review Phase 1 fixes applied and green-verified (build + AC7 commands + offline `./gradlew`). Ready for Review Phase 2 (red team / blue team) or a re-review pass. Open findings listed under Known Issues #5.
