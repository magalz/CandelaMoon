# Bach — Senior Developer — Activity Report (Review Phase 2 patch round)

- **Task**: P1-001 — candelamoon-android Containerfile
- **Dispatch**: Apply Phase 2 security patches **STR-07** and **STR-08** only
- **Branch**: `moonlight-noir` · **Head SHA**: `ddf6d5c4900cc7b17422a1b459ef83b375767325`
- **Date**: 2026-08-09 (UTC)

## 1. What was done

### PATCH 1 — STR-07: credential patterns in `.containerignore` (medium)

Appended to the existing secrets block (after `*.bak`), under the
`# Gradle/Maven credential files` comment, exactly the dispatched pattern set:

```
gradle.properties          **/gradle.properties
.netrc                     **/.netrc
.m2/settings.xml           **/.m2/settings.xml
.ssh/                      **/.ssh/
.ssh/id_*                  **/.ssh/id_*
.aws/                      **/.aws/
**/credentials             **/credentials.*
terraform.tfvars           terraform.tfvars.json
**/terraform.tfvars        **/terraform.tfvars.json
*.pfx                      **/*.pfx
```

`git diff` confirms +21 lines, nothing else touched.

### PATCH 2 — STR-08: harden the pre-existing-builder account branch (medium)

In the account `RUN`, after the existing `id -u`/`id -g` assertions (the
branch that runs when the base image already ships a `builder` account):

1. `usermod --gid 1000 builder 2>/dev/null || true` — force primary group to
   GID 1000 (self-healing, tolerant; the `id -g` assertion is the hard gate).
2. `usermod --groups builder builder` — replace the supplementary-group list
   with exactly `builder`; no adm/sudo/video/… membership survives.
3. `usermod --lock builder` — service account, no password/interactive login.
4. `[ "$(id -G builder)" = "1000" ]` — assert only GID 1000 remains.
5. `! grep -rq '^builder\b\|^%builder\b' /etc/sudoers /etc/sudoers.d/ 2>/dev/null
   || { echo "ERROR: builder has sudoers entries" >&2; exit 1; }` — fail
   closed on any user- or group-specific sudoers rule.

Consistency: the ubuntu-rename branch now also runs `usermod --lock builder`
(its existing `usermod -G builder builder` is the `--groups builder` strip).

## 2. Red phase (fail-first evidence)

The pinned base ships an `ubuntu` account, so the hardened existing-builder
branch is **latent** in the real build. To get real red-phase evidence, the
exact account `RUN` block was extracted from the Containerfile into a script
(`bash -n`-validated via WSL) and executed inside two micro-test images built
from the **same pinned base**:

| Scenario | Base state | Result |
|---|---|---|
| A (negative) | builder + sudo/video/dialout groups + `/etc/sudoers.d/90-builder` | Block **fails**: `ERROR: builder has sudoers entries`, exit 1. `-x` trace shows the ordered normalization then the sudoers gate. |
| B (positive) | builder + sudo/video/dialout groups, no sudoers rule | Block **completes** (exit 0); `id builder` → `uid=1000(builder) gid=1000(builder) groups=1000(builder)`; `passwd -S builder` → `L` (locked); sudo/video/dialout no longer list builder. |

## 3. Green phase (build + runtime evidence)

| Command | Result |
|---|---|
| `podman build --pull=never -t candelamoon-android:phase2 -f infra/containers/candelamoon-android/Containerfile .` | 18/18 steps, `Successfully tagged localhost/candelamoon-android:phase2` (id `f039d5aeb08b…`) |
| `podman run --rm --network=none candelamoon-android:phase2 id` | `uid=1000(builder) gid=1000(builder) groups=1000(builder)` — exactly `groups=1000(builder)` per dispatch |
| `podman run --rm --network=none candelamoon-android:phase2 bash -c 'passwd -S builder; id -nG'` | `builder L 2026-07-24 …`; `builder` (no supplementary groups) |
| `podman run --rm --network=none candelamoon-android:phase2 java -version` (regression) | `openjdk 17.0.19` / `Temurin-17.0.19+10` |
| `podman run --rm --network=none candelamoon-android:phase2 bash -c 'stat -c "%U:%G %a" /workspace'` | `builder:builder 755` |

## 4. Files

- Modified: `.containerignore` (STR-07, +21 lines)
- Modified: `infra/containers/candelamoon-android/Containerfile` (STR-08, +23 lines)
- Modified: `handoff.md` (head_sha, `review_phase_2.triaged_findings` STR-01..STR-10, `fixes_applied: true`, Agent Output)
- Created: this report (`.json` + `.md`)
- Test artifacts (outside repo): `%TEMP%/opencode/p1-001-str08/` — micro-base-a/b Containerfiles, `account-block.sh` (exact extracted block), micro-test runs

## 5. Deviations

1. Sudoers/`id -G` assertions live in the existing-builder branch only (per
   dispatch); the rename branch got the lock only — its `-G builder` strip is
   the `--groups builder` equivalent. Moving the sudoers gate to all branches
   is a one-line change if Brahms requests it.
2. `usermod --gid 1000 … || true` kept tolerant per dispatch; the `id -g`
   assertion remains the hard gate.
3. Existing-builder branch verified via micro-test images (the real base ships
   `ubuntu`), not via the full build.

## 6. Phase 2 triage summary (handoff `review_phase_2.triaged_findings`)

- **Applied**: STR-07 (this round), STR-08 (this round)
- **Deferred**: STR-01..STR-05 → P1-005 protected publication gate;
  STR-09 → P1-010/P1-011 mount/trust segregation
- **Open (apply-now, separate dispatch)**: STR-06 (highest-practical-priority
  per Brahms — root-own tool trees), STR-10 (archive/resource bounds)

## 7. Handoff to Bernstein

STR-07/STR-08 applied and green-verified (micro red-phase tests + full build +
`--network=none` `id`). Recommend STR-06 as the next patch round, then STR-10.
