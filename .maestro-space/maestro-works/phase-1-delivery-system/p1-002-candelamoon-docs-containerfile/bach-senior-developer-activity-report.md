# Activity Report — Bach (Senior Developer)

- **Agent**: Bach (`bach-senior-developer`)
- **Task**: P1-002 — candelamoon-docs Containerfile (Review Phase 2 security patch round)
- **Branch**: `phase1/p1-002-candelamoon-docs-containerfile`
- **Base SHA**: `0c80776971c86ddbfe60232cdfe9cdb4ebd42331`
- **Head SHA**: `91bd8403ad75a8d8b410ca4c48a172549f382302` (after this dispatch)
- **Date**: 2026-08-09
- **Dispatched by**: Bernstein (orchestrator)
- **task_id**: P1-002 (review phase 2 security patch round)

---

## Environment

- Host: Windows 11 (WSL2 backend; podman-machine-default, 8 vCPU / 8 GiB RAM / 100 GiB disk). Podman 5.8.3 rootless.
- Base image `docker.io/library/python:3.11-slim@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` cached locally (`--pull=never`).
- Prior image for red-phase evidence: `localhost/candelamoon-docs:review` (id `d3c7f79d9df2...`, pre-SEC-01 fix).
- Built image: `localhost/candelamoon-docs:phase2` (id `127a1439acb4a1478c9da085ade5fe2dd04466111a187b8f44a930d28e2a9b20`, 771,003,453 bytes).
- Build/verification logs: `%TEMP%/opencode/p1-002-phase2/build-phase2.log`, `build-phase2-repro.log`.

## Actions

1. Read the handoff, my agent identity file, the activity-report template + `agent-output.schema.json`, both Phase 2 findings reports (`findings-phase-2-stravinsky.md` SEC-01..SEC-07, `findings-phase-2-brahms.md` dispositions), the P1-021 handoff (findings-array format precedent), and the current `Containerfile` / `validate-design`.
2. SEC-01 (`validate-design`): added `cd /` at startup (after `set -eu`) so no check ever runs with the bind-mounted repository as its working directory; changed the jsonschema and pyyaml checks to `python3 -I -c "import ...; print(...__version__)"` (isolated mode — CWD, PYTHONPATH, and user site-packages are NOT on sys.path); documented the isolation rule in the script header and at both checks, including the P1-017 requirement (image-path imports, explicit /workspace paths).
3. SEC-02 (`Containerfile`): moved the entire "Non-root builder user" section (groupadd/useradd/usermod --lock, supplementary-group reset, uid/gid asserts, sudoers loop, /home/builder contract) ABOVE the Python pip section; rewrote the pip section as a two-phase flow: `COPY --chown=builder:builder` of requirements.lock → `USER builder` `python3 -m pip download --no-cache-dir --require-hashes --no-deps --only-binary=:all: -r /tmp/requirements.lock -d /tmp/pip-wheelhouse` with fail-closed wheelhouse assertions (non-empty, only `.whl`) → `USER root` offline `python3 -m pip install --no-cache-dir --require-hashes --no-deps --only-binary=:all: --no-index --find-links=/tmp/pip-wheelhouse -r /tmp/requirements.lock` → `rm -rf /tmp/pip-wheelhouse /tmp/requirements.lock`. Extended the section comment with the root/builder split and wheel-only policy; updated the final-USER comment to document the temporary switches.
4. Built `podman build --pull=never -t candelamoon-docs:phase2 -f infra/containers/candelamoon-docs/Containerfile .` → 23/23 steps green (20 → 23: USER builder / USER root / COPY--chown layers).
5. Verified the full AC7 suite under `--network=none`, `pip freeze` vs the locked set, wheelhouse cleanup (`/tmp` clean in the image), `/home/builder` hygiene (3 skeleton files + empty .cache/.npm, no pip cache baked), negative paths (unknown arg / extra args → exit 2), and default-CMD behavior.
6. SEC-01 proof — red-phase on the pre-fix image (`candelamoon-docs:review`): `/workspace/jsonschema.py` with `print("PWNED-JSONSCHEMA")` + spoofed `__version__ = "4.23.0"` → `OK: jsonschema PWNED-JSONSCHEMA`, exit 0 (attacker code executed AND false green). Green-phase on the new image: same hostile files (jsonschema.py + yaml.py) → exit 0 with real modules, no PWNED output anywhere.
7. Reproducibility — second `--no-cache` build (`phase2-repro`): identical per-tree file counts/bytes, identical pip freeze md5 `a6a8985a...` (same as the phase-1 review round), identical full file-list md5 `dca115fa...`, Compare-Object clean; sizes 771,003,453 vs 771,003,454 bytes (1-byte Podman gzip non-determinism, known AC8 debt). Removed `phase2-repro`.
8. Committed the code changes (`91bd8403`), updated the handoff (`head_sha`, review_phase_1 findings arrays with file paths, review_phase_2 triage: 2 applied + 4 deferred-to-CI + 1 dismissed, `fixes_applied: true`, Agent Output section) and wrote this activity report (JSON + MD).

## Files

- **Modified**:
  - `infra/containers/candelamoon-docs/Containerfile` — SEC-02 (builder block moved above pip; two-phase wheel-only download/install)
  - `infra/containers/candelamoon-docs/validate-design` — SEC-01 (`cd /`, `python3 -I`, documentation)
  - `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/handoff.md` — head_sha, review_phase_1 arrays, review_phase_2 triage, Agent Output
  - `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/bach-senior-developer-activity-report.md` / `.json` — this round
- **Read**: handoff, agent identity, both Phase 2 findings reports, P1-021 handoff (array format), agent-output schema, current Containerfile/validate-design

## Verification

| Command | Expected | Observed |
|---|---|---|
| `podman build --pull=never -t candelamoon-docs:phase2 -f infra/containers/candelamoon-docs/Containerfile .` | build succeeds | 23/23 steps, `Successfully tagged localhost/candelamoon-docs:phase2` (id `127a1439acb4...`, 771,003,453 bytes) |
| build log, download phase (USER builder) | wheels only, hash-verified | 9 wheels: `pip download --only-binary=:all:` → `Saved /tmp/pip-wheelhouse/*.whl` (incl. `PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.whl`, `rpds_py-2026.6.3-cp311-cp311-...whl`); wheelhouse asserts passed (9/9 `.whl`) |
| build log, install phase (USER root) | offline, from wheelhouse only | `Looking in links: /tmp/pip-wheelhouse`; all 9 wheels `Processing`'d; `rm -rf /tmp/pip-wheelhouse /tmp/requirements.lock` ran |
| `podman run --rm --network=none candelamoon-docs:phase2 python3 --version` | Python 3.11.x | `Python 3.11.15` |
| `... node --version` | v22.x | `v22.23.2` |
| `... npm --version` | 10.9.8 | `10.9.8` |
| `... markdownlint --version` | 0.45.0 | `0.45.0` |
| `... yamllint --version` | yamllint 1.37.1 | `yamllint 1.37.1` |
| `... markdown-link-check --version` | 3.13.7 | `3.13.7` |
| `... id` | uid=1000(builder) | `uid=1000(builder) gid=1000(builder) groups=1000(builder)` |
| `...` (default CMD) | validate-design exit 0 | `OK: all design validator tools present and runnable` (8/8 OK), exit 0 |
| `... validate-design --verbose` | real versions | 8 OK lines with versions (jsonschema line shows the known 4.x DeprecationWarning — cosmetic) |
| `... validate-design --verbsoe` | exit 2 + usage | exit 2 (`LASTEXITCODE=2`), usage on stderr |
| `... validate-design --verbose extra` | exit 2 + usage | exit 2, usage on stderr |
| `... bash -c 'curl -sS --max-time 5 https://pypi.org/'` | unreachable | `curl: (6) Could not resolve host: pypi.org` (exit 6) |
| `... pip freeze` | matches locked set | 10 entries identical to lock + base `packaging==26.3` |
| `... bash -c 'ls /tmp/'` | no wheelhouse/lock | `node-compile-cache` only; `WHEELHOUSE-GONE` / `LOCK-GONE` |
| `... bash -c 'find /home/builder'` | builder-owned, no pip cache | 3 skeleton files (.bashrc/.profile/.bash_logout) + empty `.cache/pip` + `.npm`, all builder:builder |
| SEC-01 red (old `candelamoon-docs:review`): `/workspace/jsonschema.py` spoof | attack executes + false green | `OK: jsonschema PWNED-JSONSCHEMA`, exit 0 — attacker code executed as builder |
| SEC-01 green (`phase2`): same jsonschema.py + yaml.py in /workspace, run from /workspace | exit 0, no PWNED | 8/8 OK, exit 0, real modules, no PWNED output |
| AC8: second `--no-cache` build (`phase2-repro`) | identical content | identical tree counts/bytes (`/opt/node 9446/231786503`, `/usr/local 2446/45964552`, `/home/builder 3/4553`, `/workspace 0/0`), pip freeze md5 `a6a8985a...` (same as phase-1 round), file-list md5 `dca115fa...`, Compare-Object clean; size 771,003,453 vs 771,003,454 bytes; digests differ (`b7c0d722...` vs `3a5da59a...` — Podman gzip, known debt) |

Full logs: `%TEMP%/opencode/p1-002-phase2/build-phase2.log`, `build-phase2-repro.log`

## Deviations

1. **`--no-cache-dir` added to the pip download phase** — Brahms' SEC-02 sketch omits it, but a builder-run `pip download` without it writes the HTTP/wheel cache under `/home/builder/.cache/pip`, baking build-varying content into the image and defeating AC8 (the exact reason PIP_NO_CACHE_DIR was scoped out of the runtime ENV in patch-3). The flag keeps the download phase cache-free; runtime pip cache volume behavior is unchanged.
2. **Wheelhouse created by the builder itself** (mkdir in the download RUN) instead of a root RUN + chown — one less root-owned intermediate path; the wheelhouse is builder-owned and cleaned up by the root install phase.
3. **`cd /` placed at script startup (all checks), not just before the Python checks** — Brahms' mitigation says "add `cd /` before the checks"; placing it at the top also stops non-Python tools (e.g. markdownlint config discovery) from resolving files relative to the repository. The Python checks additionally carry `-I`.
4. **`/home/builder` contents changed vs the phase-1 review image** — with builder creation moved before npm, `useradd --create-home` now finds no pre-existing `/home/builder` (npm no longer creates it first), so the Debian skeleton (.bashrc/.profile/.bash_logout, mode 700 home) is present: `/home/builder 3 files/4553 bytes` vs the phase-1 round's `4/0`. Deterministic across builds of this Containerfile (skeleton comes from the pinned base's /etc/skel); AC8 holds. The phase-1 recorded counts are superseded by the new baseline.

## Known Issues

1. **AC8 digest non-determinism unchanged** (Podman layer-tar gzip): content reproducibility verified for the SEC-02 build (identical trees, pip freeze md5 `a6a8985a...`, file-list md5 `dca115fa...`); image size differs by 1 byte (771,003,453 vs 771,003,454) and digests differ — same known debt as P1-001/phase-1.
2. **SEC-03..SEC-06 remain open at the image level by design** — all deferred-to-CI per Brahms: build-network egress enforcement, npm runtime sandboxing, runtime `--network=none` enforcement, and apt snapshot pinning. These become hard requirements of the CI job definition and the P1-005 apt snapshot work; the image-side controls (wheel-only pip, --ignore-scripts, hash locks, non-root runtime user) are in place.
3. **jsonschema `__version__` DeprecationWarning on stderr** (unchanged from phase 1) — harmless; visible only as the first line in `--verbose` output.
4. **npm audit debt unchanged** (8 vulnerabilities in the locked transitive npm tree) — P1-022 scope; the tree is locked and cannot drift.
5. **1-byte image-size difference between the two phase2 builds** (771,003,453 vs 771,003,454) — same Podman gzip non-determinism; content identical (file-list md5 equal).

## Handoff to

Bernstein: SEC-01 and SEC-02 applied and green-verified (`candelamoon-docs:phase2` id `127a1439acb4`, 23/23 steps; AC7 suite green under `--network=none`; pip freeze matches the lock; SEC-01 red→green proof captured: pre-fix image false-greens with `PWNED-JSONSCHEMA` exit 0, fixed image exits 0 with real modules; two-build reproducibility green). `review_phase_2.fixes_applied: true`; triage records 2 applied + 4 deferred-to-CI (SEC-03..SEC-06) + 1 dismissed (SEC-07 → P1-017). Next: UAT pass on `candelamoon-docs:phase2`, then merge review; carry SEC-03..SEC-06 into the CI job definition round and keep P1-017 / P1-022 tracked.
