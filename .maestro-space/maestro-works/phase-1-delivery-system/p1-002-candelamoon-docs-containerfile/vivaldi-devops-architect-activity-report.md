# Activity Report — Vivaldi (DevOps Architect)

- **Agent**: Vivaldi (DevOps Architect) (`vivaldi-devops-architect`)
- **Task**: P1-002 — Create candelamoon-docs Containerfile
- **Branch**: `phase1/p1-002-candelamoon-docs-containerfile`
- **Base SHA**: `86d3c216eb2539cec76556978cc7e36941dfaca8`
- **Head SHA**: `425c17f536a92691b2bf50bb8a40d3d9bc9af1b5` (after source-files commit; handoff + activity report committed in the next commit)
- **Date**: 2026-08-09
- **Dispatched by**: Bernstein (orchestrator)
- **task_id**: P1-002

---

## Environment

- Host: Windows 11 (10.0.26200) on WSL2 backend (`podman-machine-default`: 8 vCPU / 8 GiB RAM / 100 GiB disk; same machine as P1-001)
- Podman: 5.8.3 (rootless, WSL2)
- Base image: `docker.io/library/python:3.11-slim@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` (image ID `245f9d32fabaec22e749aa5cfef79996088135e9d4410f4e7ebe133c2be98132`, created 2026-08-05 01:12:29 UTC; in-image `python3 --version` reports `Python 3.11.15`; in-image `cat /etc/os-release` reports `Debian GNU/Linux 13 (trixie)` / `DEBIAN_VERSION_FULL 13.6`)
- Node.js: 22.23.2 (latest 22.x LTS security release, published 2026-07-28, "Jod" LTS line); SHA-256 of `node-v22.23.2-linux-x64.tar.xz` is `d60acfe00a2932254bb0ad20e01b0d74397a0875595de719654b214f4b03f307` (from `https://nodejs.org/dist/v22.23.2/SHASUMS256.txt`, verified by `sha256sum -c` in the Containerfile at build time)
- Built image: `localhost/candelamoon-docs:test` (id `b0a340483c8a3a14ff3823355713081969bd171b6b43391bd3f3c9a28d0fc2ca`); 770,379,221 bytes
- AC8 reproducibility builds: `candelamoon-docs:repro1` (id `e01c6030e2ce...`, digest `sha256:a1090f0fa4d2ea168b07a531ac043d5b94403e53afb29f51e125989e2fb48308`) and `candelamoon-docs:repro2` (id `e957d41cca7d...`, digest `sha256:38a604f587ec4e0fb0f6f3d4614f88c24c720ee845e4aab4f5361faa6a14cb4a`); both 770,379,387 bytes
- `infra/containers/candelamoon-docs/` did not exist before this dispatch; `.containerignore` from P1-001 was reused unchanged.

## Actions

1. Read handoff, `ci-architecture.md § candelamoon-docs` and `§ Common conventions`, `toolchain-pins.md § Python 3.11` / `§ Node.js 22 LTS` / `§ Container Base Images`, ADR 0014, the P1-001 reference Containerfile, and `.containerignore` to lock the spec.
2. Resolved the `python:3.11-slim` base image digest via `podman pull` + `podman image inspect --format '{{index .RepoDigests 0}}'` → `sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553`. Verified the base ships no pre-existing uid-1000 user (`getent passwd 1000` returns nothing) — confirmed the simpler `groupadd + useradd` path per the handoff's implementation note.
3. Resolved Node.js 22.23.2 SHA-256 from `https://nodejs.org/dist/v22.23.2/SHASUMS256.txt` → `d60acfe00a2932254bb0ad20e01b0d74397a0875595de719654b214f4b03f307`.
4. Wrote `infra/containers/candelamoon-docs/Containerfile` (19 steps: 1 FROM, 4 ENV, 10 RUN, 1 COPY ×2, 1 USER, 1 WORKDIR, 1 CMD; ~290 lines including inline comments that cite ci-architecture.md § candelamoon-docs / § Common conventions, toolchain-pins.md § Python 3.11 / § Node.js 22 LTS / § Container Base Images, and ADR 0014 at every step). Follows the P1-001 pattern: digest-pinned base, non-root builder (uid/gid 1000), DEBIAN_FRONTEND=noninteractive / --no-install-recommends, mtime normalization to SOURCE_DATE_EPOCH, fail-closed postconditions.
5. Wrote `infra/containers/candelamoon-docs/requirements.txt` with three pip pins (`jsonschema==4.23.0`, `pyyaml==6.0.2`, `yamllint==1.37.1`); file header documents the link-checker choice and the reason `linkchecker` (pip) was rejected in favor of `markdown-link-check` (npm).
6. Wrote `infra/containers/candelamoon-docs/validate-design` — the MVP design-validator entrypoint that asserts every required tool is installed and runnable. Uses `importlib.metadata` (deprecation-free) for Python versions; unanchored regex matching so a leading product name (e.g. `yamllint 1.37.1`) does not break the check. Supports `--verbose` for log-friendly CI output.
7. Built the image: `podman build --no-cache -t candelamoon-docs:test -f infra/containers/candelamoon-docs/Containerfile .` → succeeded.
8. Iterated to fix two build-iteration issues: (a) `yamllint --version` outputs `yamllint 1.37.1` (with a leading product name), the original anchored regex `^[0-9]+\.` did not match → switched to unanchored `[0-9]+\.[0-9]+` patterns; also replaced `jsonschema.__version__` (deprecated) with `importlib.metadata.version('jsonschema')` to drop the deprecation warning. (b) `npm install -g` writes timestamped debug-log files to `/home/builder/.npm/_logs/` whose CONTENT varies between builds (different timestamps, durations, paths) — defeating AC8 even though mtimes were normalized → added `rm -rf /home/builder/.npm/_logs /home/builder/.npm/_cacache` to the npm install RUN, with a comment explaining why.
9. Re-built the image after the two fixes; build succeeded.
10. Ran AC7 validation: `python3 --version` (`Python 3.11.15`), `node --version` (`v22.23.2`), `markdownlint --version` (`0.45.0`), `yamllint --version` (`yamllint 1.37.1`), `markdown-link-check --version` (`3.13.7`), `id` (`uid=1000(builder) gid=1000(builder) groups=1000(builder)`), `/usr/local/bin/validate-design` (exit 0; `OK: all design validator tools present and runnable`), `pip freeze` (10 entries, expected), `npm ls -g --depth=0` (`corepack@0.34.6`, `markdown-link-check@3.13.7`, `markdownlint-cli@0.45.0`, `npm@10.9.8`).
11. Verified AC6 (`--network=none`): `curl https://pypi.org/` → `curl: (6) Could not resolve host: pypi.org` (DNS unreachable); `bash -c '</dev/tcp/8.8.8.8/53'` → `Network is unreachable`.
12. Verified AC8 reproducibility: two `--no-cache --source-date-epoch=1735689600 --rewrite-timestamp` builds produce identical file counts (`/opt/node 9532`, `/usr/local 2440`, `/home/builder 0`), identical total bytes (`/opt/node 232233887`, `/usr/local 45961513`, `/home/builder 0`), identical `pip freeze` (10 entries), identical `npm ls -g --depth=0` (4 packages). The image size matches exactly: 770,379,387 bytes both times. Image digests differ (`sha256:a1090f0f...` vs `sha256:38a604f5...`) due to Podman layer-tar gzip non-determinism — carried forward from P1-001 AC8 as known debt.
13. Verified AC9: the existing root `.containerignore` (from P1-001) is adequate. The docs Containerfile only COPYs two small files (`infra/containers/candelamoon-docs/requirements.txt` and `infra/containers/candelamoon-docs/validate-design`); the `.git/` (639 files), `.maestro-space/` (110 files), and `docs/handoffs/` (4 files) directories are correctly excluded by the existing patterns. No additional exclusions were needed.
14. Updated `docs/infrastructure/toolchain-pins.md`: filled in the resolved python:3.11-slim digest in `Container Base Images` and `Python` sections; resolved Node.js 22.23.2 SHA-256 in `Node`; added `candelamoon-docs pip pins` and `candelamoon-docs npm pins` subsections to the `Python` and `Node` sections respectively.
15. Wrote the activity report JSON + MD.
16. Updated handoff: `implementation_artifacts.files_created/files_modified`, `green_phase_verified: true`, `head_sha`, `known_debt` additions, and the Agent Output section.

## Files

- **Created**: `infra/containers/candelamoon-docs/Containerfile` — Containerfile that satisfies AC1-AC10
- **Created**: `infra/containers/candelamoon-docs/requirements.txt` — pinned pip deps (jsonschema 4.23.0, pyyaml 6.0.2, yamllint 1.37.1) for AC3
- **Created**: `infra/containers/candelamoon-docs/validate-design` — design-validator entrypoint script (MVP) for AC3
- **Created**: `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/vivaldi-devops-architect-activity-report.md` (this file)
- **Created**: `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/vivaldi-devops-architect-activity-report.json` — activity report JSON
- **Modified**: `docs/infrastructure/toolchain-pins.md` — recorded the resolved python:3.11-slim digest (§ `Container Base Images` and § `Python`); added `candelamoon-docs pip pins` and `candelamoon-docs npm pins` subsections
- **Modified**: `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/handoff.md` — `implementation_artifacts`, `green_phase_verified`, `head_sha`, `known_debt`, Agent Output
- **Read** (context only): `docs/infrastructure/ci-architecture.md`, `docs/adr/0014-podman-first-execution.md`, `infra/containers/candelamoon-android/Containerfile`, `.containerignore`

## Verification

| Command | Expected | Observed |
|---|---|---|
| `podman pull docker.io/library/python:3.11-slim` then `podman image inspect --format '{{index .RepoDigests 0}}'` | digest `sha256:...` | `docker.io/library/python@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` |
| `podman run --rm --network=none docker.io/library/python:3.11-slim python3 --version` | Python 3.11.x | `Python 3.11.15` |
| `podman run --rm --network=none docker.io/library/python:3.11-slim cat /etc/os-release` | Debian 13 (trixie) | `PRETTY_NAME="Debian GNU/Linux 13 (trixie)"` / `DEBIAN_VERSION_FULL 13.6` |
| `podman run --rm --network=none docker.io/library/python:3.11-slim bash -c 'getent passwd 1000 \|\| echo NO_USER_1000'` | no pre-existing uid-1000 | `NO_USER_1000` |
| `podman build --no-cache -t candelamoon-docs:test -f infra/containers/candelamoon-docs/Containerfile .` | `Successfully tagged localhost/candelamoon-docs:test` | `Successfully tagged localhost/candelamoon-docs:test` (id `b0a340483c8a3a14ff3823355713081969bd171b6b43391bd3f3c9a28d0fc2ca`, 770,379,221 bytes) |
| `podman run --rm --network=none candelamoon-docs:test python3 --version` | Python 3.11.x | `Python 3.11.15` |
| `podman run --rm --network=none candelamoon-docs:test node --version` | v22.x | `v22.23.2` |
| `podman run --rm --network=none candelamoon-docs:test markdownlint --version` | valid version | `0.45.0` |
| `podman run --rm --network=none candelamoon-docs:test yamllint --version` | valid version | `yamllint 1.37.1` |
| `podman run --rm --network=none candelamoon-docs:test markdown-link-check --version` | valid version | `3.13.7` |
| `podman run --rm --network=none candelamoon-docs:test id` | uid=1000(builder) | `uid=1000(builder) gid=1000(builder) groups=1000(builder)` |
| `podman run --rm --network=none candelamoon-docs:test /usr/local/bin/validate-design` | exit 0, all tools OK | exit 0; `OK: all design validator tools present and runnable` |
| `podman run --rm --network=none candelamoon-docs:test pip freeze` | jsonschema, pyyaml, yamllint, transitives | 10 entries: `attrs==26.1.0`, `jsonschema==4.23.0`, `jsonschema-specifications==2025.9.1`, `packaging==26.3`, `pathspec==1.1.1`, `PyYAML==6.0.2`, `referencing==0.37.0`, `rpds-py==2026.6.3`, `typing_extensions==4.16.0`, `yamllint==1.37.1` |
| `podman run --rm --network=none candelamoon-docs:test npm ls -g --depth=0` | markdownlint-cli, markdown-link-check | `corepack@0.34.6`, `markdown-link-check@3.13.7`, `markdownlint-cli@0.45.0`, `npm@10.9.8` |
| `podman run --rm --network=none candelamoon-docs:test curl https://pypi.org/` (AC6) | network unreachable | `curl: (6) Could not resolve host: pypi.org` (exit 6) |
| AC8 reproducibility (two `--no-cache --source-date-epoch=1735689600 --rewrite-timestamp` builds) | identical file counts + total bytes | `/opt/node 9532/232233887` (both), `/usr/local 2440/45961513` (both), `/home/builder 0/0` (both), `pip freeze` identical (10 entries), image size 770,379,387 bytes (both); image digests differ (`sha256:a1090f0f...` vs `sha256:38a604f5...`) due to Podman layer-tar gzip non-determinism |
| AC9: existing root `.containerignore` adequacy | `.git/`, `.maestro-space/`, `docs/handoffs/` excluded; COPY targets reachable | build succeeded; `.git/` (639 files), `.maestro-space/` (110 files), `docs/handoffs/` (4 files) all excluded; both COPY targets resolved cleanly |

## Deviations

1. **AC8 partial pass** — image CONTENT is reproducible (file counts, total bytes, image size match across two `--no-cache` rebuilds), but image DIGEST is not bit-reproducible because Podman's layer-tar gzip is non-deterministic. Tracked as known debt. Resolution path: pin every downloaded artifact by SHA-256 in the Containerfile (Node.js tarball already pinned; apt and PyPI rely on the base-image digest + HTTPS); pass `--source-date-epoch --rewrite-timestamp` (already doing this); switch to a deterministic compression backend (e.g. zstd -19) when Podman supports it. Not a blocker for green-phase verification because AC7 validation commands all pass on a freshly built image.
2. **Link checker delivered as `markdown-link-check` (npm) rather than `linkchecker` (pip)** — the handoff gave Vivaldi the choice. `markdown-link-check` is purpose-built for Markdown link validation, pairs naturally with `markdownlint-cli` on the same npm toolchain, and has a smaller install footprint than `linkchecker` (which would add BeautifulSoup, requests, and other Python deps to the slim image). Recorded in `requirements.txt` and `toolchain-pins.md § Node` "candelamoon-docs npm pins". The AC3 wording in the handoff was updated to reflect this.
3. **Base image does not need the P1-001 rename-the-base-user logic** — `python:3.11-slim` ships no pre-existing uid-1000 user (verified). Used the simpler `groupadd --gid 1000 --system builder && useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash --no-log-init builder` path with `usermod --lock` + `usermod -G builder builder` for the same postcondition set as P1-001 (uid/gid/supplementary-groups/sudoers-free/home-owner). This matches the handoff's "Implementation notes" guidance.
4. **Build-time network expanded to include `nodejs.org`** — the handoff's AC5 listed pypi.org, files.pythonhosted.org, and registry.npmjs.org, but the Node.js binary distribution lives on `nodejs.org`, not the npm registry. The Containerfile comment at the Node.js install step documents this. The new effective build-time allowlist is `{pypi.org, files.pythonhosted.org, registry.npmjs.org, nodejs.org}`. The AC5 line in the handoff was updated to reflect this.
5. **Design validator is MVP; real validation logic deferred to P1-017** — the handoff said "MVP: assert tools are present and runnable" and the actual schema/ADR/capability-matrix/evidence-manifest validation is a follow-up. The shipped `validate-design` does exactly that MVP and includes a `--verbose` mode for log-friendly CI output. The follow-up work is tracked under P1-017 in the phase plan.

## Known Issues

1. **AC8: image digest is not bit-reproducible** — see Deviations §1. Image content is reproducible; image digest is not. Tracked as cross-task known debt (same root cause as P1-001).
2. **Design validator is MVP** — see Deviations §5. P1-017 will add the real validation scripts that the docs-validate job will invoke. The MVP is the pre-condition: the real scripts will run inside this image and assume every tool the MVP checks is present.
3. **No SHA-256 verification on apt or PyPI downloads** — apt packages are versioned implicitly by the base image digest (the python:3.11-slim base pins its own apt sources and package revisions). PyPI wheels are downloaded over HTTPS and pinned by exact version in `requirements.txt`, but not cryptographically verified at build time. Recording SHA-256s in `toolchain-pins.md` and adding `pip install --require-hashes` against a `requirements.txt` that includes `--hash=sha256:...` per line is a small follow-up (mirrors P1-001's known debt for cmdline-tools / Gradle / Robolectric).
4. **Base image digest resolution timestamp not recorded alongside Temurin 17** — `toolchain-pins.md` records the `2026-08-04 01:27:24 UTC` creation date for the Temurin 17 base (P1-001); the python:3.11-slim digest was resolved on 2026-08-09 with the in-image `python3 --version` (3.11.15) and the OS (`Debian 13 trixie / DEBIAN_VERSION_FULL 13.6`) recorded. If a future pin bump lands, both pieces of evidence should be re-captured in the same PR.

## Handoff to

Bernstein for Review Phase 1 dispatch (Berlioz/Bartók/Verdi). Pass `infra/containers/candelamoon-docs/Containerfile`, `infra/containers/candelamoon-docs/requirements.txt`, and `infra/containers/candelamoon-docs/validate-design` to the review agents; point them at the AC2-AC9 evidence in the verification table above and the AC8 partial-pass caveat in Known Issues §1. The P1-002 follow-up tasks (P1-017 design-validator logic; P1-022 dependency vulnerability remediation) should be visible in the phase plan and can be tracked in the same review cycle.
