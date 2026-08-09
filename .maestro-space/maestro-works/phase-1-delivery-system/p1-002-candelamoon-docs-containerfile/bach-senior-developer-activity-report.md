# Activity Report — Bach (Senior Developer)

- **Agent**: Bach (`bach-senior-developer`)
- **Task**: P1-002 — candelamoon-docs Containerfile (Review Phase 1 patch round)
- **Branch**: `phase1/p1-002-candelamoon-docs-containerfile`
- **Base SHA**: `e37c8c189b2505b11e36093c629fe6430839031f`
- **Head SHA**: `ff6c64d00340498c0c42d29f547b8c5bee65554b` (after this dispatch)
- **Date**: 2026-08-09
- **Dispatched by**: Bernstein (orchestrator)
- **task_id**: P1-002 (review phase 1 patch round)

---

## Environment

- Host: Windows 11 (WSL2 backend; podman-machine-default, 8 vCPU / 8 GiB RAM / 100 GiB disk). Podman 5.8.3 rootless.
- Base image `docker.io/library/python:3.11-slim@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` cached locally (`--pull=never`).
- Lock tooling: `uv 0.11.13` (`uv pip compile --generate-hashes`); host npm 11.13.0 (`npm install --package-lock-only` → lockfileVersion 3, readable by in-image npm 10.9.8).
- Built image: `localhost/candelamoon-docs:review` (id `d3c7f79d9df29fe780b197f09c2a817739c5f71a678edd0fcf1d33c3578d6b96`, 769,460,929 bytes).
- Prior image for reference: `localhost/candelamoon-docs:test` (id `b0a340483c8a...`, pre-review).
- Build/verification logs: `%TEMP%/opencode/p1-002-review/build-review.log`, `build-review2.log`, `build-review-repro.log`.

## Actions

1. Read the handoff, agent identity file, activity-report template + `agent-output.schema.json`, all three findings reports (Berlioz B-01..B-18, Bartók BAR-001..BAR-015, Verdi A-01..A-03), the P1-001 handoff (triaged_findings format precedent), and `ci-architecture.md` § candelamoon-docs / Common conventions.
2. PATCH 1: generated `infra/containers/candelamoon-docs/requirements.lock` (9 packages, `--hash=sha256:...` per artifact) via `uv pip compile --generate-hashes --python-version 3.11 --python-platform x86_64-unknown-linux-gnu requirements.txt`; confirmed the resolved set matches the recorded in-image pip freeze (10 entries incl. base-shipped `packaging==26.3`, verified present in the base image via `podman run` pip freeze). Containerfile pip step now: `pip install --no-cache-dir --require-hashes --no-deps -r /tmp/requirements.lock`. Updated requirements.txt header + toolchain-pins.md § Python.
3. PATCH 2: created `package.json` (markdownlint-cli 0.45.0, markdown-link-check 3.13.7) and generated `package-lock.json` (lockfileVersion 3, 165 packages, integrity hashes). Rewrote the npm step: COPY package.json+lock → `npm ci --ignore-scripts` in `/tmp/candelamoon-docs-npm` → copy locked tree to `/opt/node/lib/node_modules` → bin symlinks in `/opt/node/bin` (markdownlint → markdownlint-cli/markdownlint.js; markdown-link-check → markdown-link-check/markdown-link-check) → `npm cache clean --force` + `rm -rf _logs/_cacache`. Bin names confirmed via `npm view <pkg> bin`.
4. PATCH 3: removed `PIP_NO_CACHE_DIR=1` from the ENV block (runtime pip-cache volume contract); `--no-cache-dir` now only on the build pip RUN. Verified `printenv PIP_NO_CACHE_DIR` unset at runtime.
5. PATCH 4: moved `mkdir -p /workspace && chown builder:builder /workspace` BEFORE the mtime-normalization pass; added `/workspace` to the `find ... -exec touch` roots. Verified /workspace mtime = 2025-01-01 00:00:00 UTC, owner builder:builder.
6. PATCHES 5/6/7/10: rewrote `validate-design` — anchored exact-version patterns (jsonschema `^4\.23\.0$`, pyyaml `^6\.0\.2$`, yamllint `^yamllint 1\.37\.1$`, markdownlint `^0\.45\.0$`, markdown-link-check `^3\.13\.7$`, npm `^10\.9\.8$`; python3 `^Python 3\.11\.`, node `^v22\.`), real module imports for jsonschema/yaml (split into two checks so failures name the failing package), strict arg validation (unknown/extra → usage on stderr, exit 2), `timeout 30` per probe with distinct exit-124 report.
7. PATCH 8: CMD `["bash"]` → `["validate-design"]` with an `--entrypoint bash` interactive note.
8. PATCH 9: rewrote the sudoers guard as an explicit per-path loop; first build failed (`/bin/sh: syntax error expecting "done"` — multi-line loop inside a backslash-continued RUN body), collapsed to a single shell line; second build green.
9. PATCH 11: added the consolidated 5-domain build-time network allowlist comment block (pypi.org, files.pythonhosted.org, registry.npmjs.org, nodejs.org, deb.debian.org) to the Containerfile header; updated handoff AC5.
10. Built `podman build --pull=never -t candelamoon-docs:review -f infra/containers/candelamoon-docs/Containerfile .` → 20/20 steps green.
11. Verified the AC7 suite under `--network=none` plus negative paths (unknown arg → exit 2; extra args → exit 2; in-image `timeout 1 sleep 5` → 124; sudoers loop no false positive) and runtime env (PIP_NO_CACHE_DIR unset).
12. Reproducibility: second `--no-cache` build (`review2`) → identical `find` file lists, identical counts/bytes per tree, identical pip freeze (md5 `a6a8985a...`), identical image size 769,460,929 bytes; digests differ (Podman gzip non-determinism, known debt). Removed `review2`.
13. Committed code (`ff6c64d0`), updated the handoff (`head_sha`, AC5, implementation_artifacts, review_phase_1.triaged_findings 11 applied + 3 deferred + 8 dismissed, fixes_applied: true, known_debt, Agent Output), wrote this activity report (JSON + MD).

## Files

- **Created**:
  - `infra/containers/candelamoon-docs/requirements.lock` — hash-locked pip tree (9 packages)
  - `infra/containers/candelamoon-docs/package.json` — npm top-level pins (exact)
  - `infra/containers/candelamoon-docs/package-lock.json` — locked npm tree (165 packages, integrity hashes)
  - `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/bach-senior-developer-activity-report.md` / `.json`
- **Modified**:
  - `infra/containers/candelamoon-docs/Containerfile` — patches 1-4, 8, 9, 11
  - `infra/containers/candelamoon-docs/validate-design` — patches 5, 6, 7, 10
  - `infra/containers/candelamoon-docs/requirements.txt` — lock documentation
  - `docs/infrastructure/toolchain-pins.md` — § Python / § Node lock records
  - `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/handoff.md` — head_sha, AC5, review_phase_1, known_debt, Agent Output
- **Read**: handoff, agent identity, all three findings reports, P1-001 handoff, Vivaldi's reports, `agent-output.schema.json`, `ci-architecture.md`, base image inspection

## Verification

| Command | Expected | Observed |
|---|---|---|
| `podman build --pull=never -t candelamoon-docs:review -f infra/containers/candelamoon-docs/Containerfile .` | build succeeds | 20/20 steps, `Successfully tagged localhost/candelamoon-docs:review` (id `d3c7f79d9df2...`, 769,460,929 bytes) |
| `pip install --dry-run --require-hashes --no-deps -r requirements.lock` (host) | lock parses, hashes accepted | `Would install PyYAML-6.0.2 jsonschema-4.23.0 pathspec-1.1.1 rpds-py-2026.6.3 typing_extensions-4.16.0 yamllint-1.37.1` |
| `podman run --rm --network=none candelamoon-docs:review python3 --version` | Python 3.11.x | `Python 3.11.15` |
| `... node --version` | v22.x | `v22.23.2` |
| `... npm --version` | 10.9.8 | `10.9.8` |
| `... markdownlint --version` | 0.45.0 | `0.45.0` |
| `... yamllint --version` | yamllint 1.37.1 | `yamllint 1.37.1` |
| `... markdown-link-check --version` | 3.13.7 | `3.13.7` |
| `... id` | uid=1000(builder) | `uid=1000(builder) gid=1000(builder) groups=1000(builder)` |
| `...` (default CMD) | validate-design exit 0 | `OK: all design validator tools present and runnable` (8/8 OK) |
| `... validate-design --verbose` | per-tool OK | 8 OK lines with versions (jsonschema first line shows 4.x DeprecationWarning — cosmetic) |
| `... validate-design --verbsoe` | exit 2 + usage | `ERROR: unknown argument: --verbsoe` + usage, exit 2 |
| `... validate-design --verbose extra` | exit 2 + usage | `ERROR: too many arguments: --verbose extra` + usage, exit 2 |
| `... bash -c 'printenv PIP_NO_CACHE_DIR'` | unset | unset (rc 1) |
| `... bash -c 'curl -sS --max-time 5 https://pypi.org/'` | unreachable | `curl: (6) Could not resolve host: pypi.org` (exit 6) |
| `... pip freeze` | 10 entries | identical recorded set incl. base-shipped `packaging==26.3` |
| `... npm ls -g --depth=0` | expected names present | full locked tree (165 pkgs); `corepack@0.34.6`, `markdown-link-check@3.13.7`, `markdownlint-cli@0.45.0`, `npm@10.9.8` present |
| `... stat -c '%U:%G %y' /workspace` | builder + SDE | `builder:builder 2025-01-01 00:00:00.000000000 +0000` |
| `... bash -c 'timeout 1 sleep 5; echo rc=$?'` | 124 | `timeout-rc=124` |
| sudoers loop (in-image) | no false positive | `no sudoers entries for builder (good)` |
| AC8: two `--no-cache` builds | identical content | identical file lists; counts/bytes per tree identical (`/opt/node 11169/231786503`, `/usr/local 2867/45963238`, `/home/builder 4/0`, `/workspace 1/0`); pip freeze md5 `a6a8985a...`; image size 769,460,929 bytes both; digests differ (`d3c7f79d9df2` vs `602cf10611ec` — Podman gzip, known debt) |

Full logs: `%TEMP%/opencode/p1-002-review/build-review.log`, `build-review2.log`, `build-review-repro.log`

## Deviations

1. **validate-design checks split**: the triaged PATCH 6 suggested one combined import command; implemented as two separate checks (one command per check) so failures name the failing package and the `check()` helper keeps its single-pattern contract. Both do real imports and assert exact pinned versions — B-15/BAR-006 intent fully met.
2. **sudoers loop single-line form**: the triaged multi-line `for ... do ... done` cannot span lines inside a backslash-continued RUN body (first build: `/bin/sh: syntax error expecting "done"`); collapsed to one shell line, identical semantics, inline comment added.
3. **npm global wiring**: `npm install -g` cannot consume a lockfile, so PATCH 2 is implemented as `npm ci --ignore-scripts` + copy into the global layout + explicit bin symlinks. Side effect: `npm ls -g --depth=0` lists the whole 165-package locked tree instead of 4 top-level entries (global-install bookkeeping is not written); all expected names present, CLIs verified.
4. **npm exact-pinned** (`^10\.9\.8$`): not in the triaged patch list, but npm ships inside the SHA-256-pinned Node 22.23.2 tarball, so exact-pinning is deterministic and consistent with PATCH 5's intent.

## Known Issues

1. **npm audit: 8 vulnerabilities (4 moderate, 4 high) in the locked transitive npm tree** (e.g. `glob@11.0.3`, which also emits a deprecation warning during `npm ci`). Tree is locked (cannot drift) but vulnerable versions remain until pin bumps + lock regeneration — P1-022 scope.
2. **ci-architecture.md § candelamoon-docs 'Build-time network' lists only 'PyPI, npm registry'** while the Containerfile/handoff now document the 5-domain allowlist; update the normative spec doc in the same PR as the next pin change.
3. **AC8 digest non-determinism unchanged** (Podman layer-tar gzip); content reproducibility of the new locked build verified (identical file lists, counts, bytes, pip freeze, image size).
4. **jsonschema `__version__` DeprecationWarning on stderr** (per the triaged patch's explicit command choice) — harmless, anchored pattern matches the version line, visible only in `--verbose` first-line output.

## Handoff to

Bernstein: all 11 triaged patches applied and green-verified (`candelamoon-docs:review` id `d3c7f79d9df2`; AC7 suite green under `--network=none`; negative paths green; two-build reproducibility green). `review_phase_1.fixes_applied: true`; triage records 11 applied + 3 deferred (P1-005 / P1-017) + 8 dismissed. Next: UAT on `candelamoon-docs:review`, then merge review; P1-017 / P1-022 remain tracked follow-ups.
