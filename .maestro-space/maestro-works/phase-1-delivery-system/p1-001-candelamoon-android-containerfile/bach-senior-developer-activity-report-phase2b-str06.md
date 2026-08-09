# Bach — Senior Developer — Activity Report (STR-06 patch round)

- **Task**: P1-001 — candelamoon-android Containerfile
- **Dispatch**: Apply security patch **STR-06** only — root-own baked tool trees
- **Branch**: `moonlight-noir` · **Base SHA**: `0262b0a` · **Head SHA**: `7731c4e7640ca6e09af80de8d62b661cd5f2510b`
- **Date**: 2026-08-08 (local) / 2026-08-09 UTC

## 1. What was done

### PATCH — STR-06: root-owned, read-only baked tool trees (high, highest practical priority)

Replaced the single permissions RUN in
`infra/containers/candelamoon-android/Containerfile`:

```dockerfile
# before (poisonable):
RUN chown -R builder:builder /opt/android-sdk /opt/gradle /home/builder

# after (STR-06):
# Per STR-06: baked tool trees are root-owned and read-only for builder.
# This prevents a compromised PR build from overwriting SDK, NDK, or Gradle
# binaries that could then execute in a trusted CI job via cache reuse.
# /home/builder stays builder-owned for Gradle/Maven runtime caches.
RUN chown -R root:root /opt/android-sdk /opt/gradle \
    && find /opt/android-sdk /opt/gradle -type d -exec chmod go-w {} + \
    && find /opt/android-sdk /opt/gradle -type f -exec chmod go-w {} + \
    && chown -R builder:builder /home/builder
```

The section header comment was updated in lockstep (the old "chown everything
to builder" would have misdocumented the block): root-owned tool trees,
builder-owned runtime caches, ci-architecture.md citation kept, STR-06
rationale verbatim from the dispatch.

Pre-change tree audit: 35 symlinks exist under the tool trees, all resolving
in-tree, zero dangling — so `find -exec chmod go-w` cannot error out the
`&&` chain (`-type f`/`-type d` do not match symlinks; `chmod go-w` preserves
execute/traversal bits).

## 2. Red phase (fail-first evidence)

Against the pre-change image `localhost/candelamoon-android:phase2`
(id `f039d5aeb08b…`), before the patch:

| Check | Observed (red) |
|---|---|
| `stat -c "%U:%G" /opt/android-sdk /opt/gradle` | `builder:builder` (both) |
| `touch /opt/android-sdk/red-phase-probe` (as builder, the runtime user) | succeeds — tool tree writable by the untrusted build user |

This is the exact STR-06 poisonable state: a compromised PR build could
overwrite SDK/NDK/Gradle binaries that a trusted job would then execute via
cache reuse.

## 3. Green phase (build + runtime evidence)

| Command | Result |
|---|---|
| `podman build --pull=never -t candelamoon-android:str06 -f infra/containers/candelamoon-android/Containerfile .` | 18/18 steps, `Successfully tagged localhost/candelamoon-android:str06` (id `6e1fa84379f2…`); steps 1-11 layer-cached, step 12 (STR-06 RUN) + 13-18 rebuilt |
| `ls -la /opt/android-sdk/platform-tools/adb` | `-rwxr-xr-x 1 root root 10642368 … adb` |
| `/opt/android-sdk/platform-tools/adb version` | `Android Debug Bridge version 1.0.41 / Version 37.0.1-15733141` |
| `touch /opt/android-sdk/test_write 2>&1 \|\| echo "EXPECTED: cannot write"` | `Permission denied` + `EXPECTED: cannot write` |
| `touch /home/builder/test_write && echo "OK: home writable" && rm …` | `OK: home writable` |
| `stat -c "%U:%G %a" /opt/android-sdk /opt/gradle /home/builder` | `root:root 755` / `root:root 755` / `builder:builder 750` |
| `find /opt/android-sdk /opt/gradle -type d -perm /022 \| wc -l` | `0` (no group/other-writable dirs) |
| `find /opt/android-sdk /opt/gradle -type f -perm /022 \| wc -l` | `0` (no group/other-writable files) |
| `find /opt/android-sdk /opt/gradle -not -user root \| wc -l` | `0` (fully root-owned) |
| `id` (regression) | `uid=1000(builder) gid=1000(builder) groups=1000(builder)` |
| `java -version` (regression) | `openjdk 17.0.19` / Temurin-17.0.19+10 |
| `sdkmanager --list` (regression) | `build-tools;36.0.0`, `cmake;3.22.1`, `ndk;27.0.12077973`, `platform-tools 37.0.1`, `platforms;android-36` |
| `gradle --version` (regression, read-only /opt/gradle) | `Gradle 8.13` |
| offline `./gradlew --version`, `--network=none` (throwaway project, wrapper layout preserved) | `Gradle 8.13`, `Kotlin: 2.0.21`, `Launcher JVM: 17.0.19` — dist resolved from builder-owned `/home/builder/.gradle/wrapper/dists/…` |
| `stat -c %y` adb / gradle / wrapper zip (mtime normalization) | all `2025-01-01 00:00:00.000000000 +0000` |
| `git diff` scope | only the STR-06 hunk: 9 insertions / 2 deletions |

## 4. Files

- Modified: `infra/containers/candelamoon-android/Containerfile` (STR-06 RUN + section comment)
- Modified: `handoff.md` (`head_sha` → `7731c4e7`, STR-06 triaged finding → `applied`, Agent Output section)
- Created: this report (`.json` + `.md`)
- Test artifacts (outside repo): `%TEMP%/opencode/p1-001-str06/` — wrapper files for the offline gradlew test

## 5. Deviations

1. **Section comment updated alongside the RUN** — the old "Permissions: chown everything to builder" header would have misdocumented the new block; the comment now states root-owned tool trees + builder-owned runtime caches, keeping the ci-architecture.md citation and the dispatch's STR-06 rationale verbatim.
2. **First offline `./gradlew` attempt failed due to test layout, not the image** — the wrapper script resolves `$APP_HOME/gradle/wrapper/gradle-wrapper.jar`, so flat-copied wrapper files produce `Could not find or load main class`. Re-ran with the repo layout preserved (`gradlew` + `gradle/wrapper/`): passes, same as the prior rounds' method.
3. **AC5 parenthetical superseded** — AC5 as written says all of /opt/android-sdk, /opt/gradle, /home/builder are chown'd to builder; STR-06 intentionally changes the first two. AC text retained as the original acceptance record; the STR-06 triaged entry records the supersession.

## 6. Phase 2 triage summary (handoff `review_phase_2.triaged_findings`)

- **Applied**: STR-06 (this round) — joins STR-07, STR-08
- **Deferred**: STR-01..STR-05 → P1-005 protected publication gate; STR-09 → P1-010/P1-011 mount/trust segregation; STR-06 CI-side cache enforcement → P1-010/P1-011
- **Open (apply-now, separate dispatch)**: STR-10 (archive/resource bounds)

## 7. Handoff to Bernstein

STR-06 applied and green-verified (root-owned go-w tool trees; dispatch checks
+ full regression under `--network=none`, including offline gradlew). Remaining
Phase 2 apply-now finding: STR-10 (archive resource bounds), suggested as the
next patch round.
