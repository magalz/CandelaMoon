---
change_id: "P1-002"
phase: "Phase 1"
task: "Create candelamoon-docs Containerfile — containerized docs validation environment (Python 3.11 slim, jsonschema, yamllint, markdown-link-check, Node.js 22 LTS + markdownlint-cli, design validator)"
status: "in-progress"
repository: "magalz/CandelaMoon"
branch: "phase1/p1-002-candelamoon-docs-containerfile"
base_sha: "86d3c216eb2539cec76556978cc7e36941dfaca8"
head_sha: "425c17f536a92691b2bf50bb8a40d3d9bc9af1b5"
pr_url: ""
acceptance_criteria:
  - "AC1: Containerfile exists at `infra/containers/candelamoon-docs/Containerfile`."
  - "AC2: Base image is digest-pinned `docker.io/library/python:3.11-slim@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` (resolved via `podman pull` + `podman image inspect`; recorded in toolchain-pins.md § `Container Base Images` and § `Python`)."
  - "AC3: Installed tools match toolchain-pins.md: Python 3.11 (from base) + pinned pip deps (jsonschema 4.23.0, pyyaml 6.0.2, yamllint 1.37.1; link checker provided by npm `markdown-link-check@3.13.7` — see Deviations §1); Node.js 22 LTS resolved to 22.23.2 + markdownlint-cli 0.45.0; design validator entrypoint at `/usr/local/bin/validate-design` (MVP: asserts all tools are present and runnable; real validation logic against docs/ content is P1-017 follow-up); ADR/capability-matrix validation scripts deferred to P1-017."
  - "AC4: Non-root `builder` user (uid 1000, gid 1000) is the final USER directive. All pip/node caches (/home/builder/.cache/pip, /home/builder/.npm) chown'd to builder:builder."
  - "AC5: Build-time network limited to pypi.org / files.pythonhosted.org (pip), registry.npmjs.org (npm), nodejs.org (Node.js binary tarball — required by the spec; documented inline in the Containerfile § Node.js 22 LTS)."
  - "AC6: Run-time network is `--network=none` (verified: `podman run --rm --network=none` cannot resolve DNS or open TCP connections)."
  - "AC7: `podman build` succeeds from repo root; `podman run --rm --network=none candelamoon-docs:test python3 --version` reports `Python 3.11.15`; `podman run --rm --network=none candelamoon-docs:test node --version` reports `v22.23.2`; `podman run --rm --network=none candelamoon-docs:test markdownlint --version` reports `0.45.0`; `podman run --rm --network=none candelamoon-docs:test yamllint --version` reports `yamllint 1.37.1`; `podman run --rm --network=none candelamoon-docs:test markdown-link-check --version` reports `3.13.7`."
  - "AC8: Image content is reproducible: two `--no-cache --source-date-epoch=1735689600 --rewrite-timestamp` builds produce identical pip freeze (10 entries), identical file counts (/opt/node 9532, /usr/local 2440, /home/builder 0), and identical total bytes (/opt/node 232233887, /usr/local 45961513, /home/builder 0). Image size matches exactly: 770379387 bytes. Image digest differs (sha256:a1090f0f... vs sha256:38a604f5...) due to Podman layer-tar gzip non-determinism — tracked as known debt per P1-001."
  - "AC9: Root `.containerignore` (existing from P1-001) is adequate for the docs build context. Verified by the build succeeding: `.git/` (639 files), `.maestro-space/` (110 files), and `docs/handoffs/` (4 files) are all excluded by the existing patterns; the docs Containerfile only COPYs `infra/containers/candelamoon-docs/requirements.txt` and `infra/containers/candelamoon-docs/validate-design` from the build context, both of which are correctly reachable. No additional exclusions needed."
  - "AC10: Containerfile carries inline comments linking each section to its governing doc (ci-architecture.md § `candelamoon-docs` / `Common conventions`; toolchain-pins.md § `Python 3.11` / `Node.js 22 LTS` / `Container Base Images`; ADR 0014)."
tdd_artifacts:
  atdd_checklist: ""
  test_files: []
  red_phase_verified: false
implementation_artifacts:
  files_created:
    - "infra/containers/candelamoon-docs/Containerfile"
    - "infra/containers/candelamoon-docs/requirements.txt"
    - "infra/containers/candelamoon-docs/validate-design"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/vivaldi-devops-architect-activity-report.md"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/vivaldi-devops-architect-activity-report.json"
  files_modified:
    - "docs/infrastructure/toolchain-pins.md"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/handoff.md"
  green_phase_verified: true
review_phase_1:
  blind_hunter_findings: []
  edge_case_hunter_findings: []
  acceptance_analyst_findings: []
  triaged_findings: []
  fixes_applied: false
review_phase_2:
  red_team_findings: []
  blue_team_findings: []
  triaged_findings: []
  fixes_applied: false
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
  session_handout: ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/session-handout.md"
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
  - "AC8: Podman layer-tar gzip is non-deterministic (carried forward from P1-001). Image content is reproducible (file counts, total bytes, pip freeze, npm modules, image size all match across two --no-cache builds). Image digest is not bit-reproducible — same root cause as P1-001 (Podman gzip non-determinism). Tracked as cross-task known debt; resolution path: pin every downloaded artifact by SHA-256 (already done for Node.js tarball; apt and PyPI rely on the base-image digest + HTTPS), and switch to a deterministic compression backend (e.g. zstd -19) when Podman supports it."
  - "Design validator is MVP. The script asserts that all required tools are installed and runnable; the actual validation logic (architecture schemas, ADR register, capability matrix, evidence manifest, ADR/capability-matrix validation scripts) is P1-017 follow-up. The MVP is a hard pre-condition for P1-017 because the real validator scripts will run inside this image."
rollback_strategy: "Delete infra/containers/candelamoon-docs/, revert toolchain-pins.md digest update, and revert .containerignore if modified. No code or build files are affected — the Containerfile is not yet referenced by any CI workflow."
---

# Task: P1-002 — candelamoon-docs Containerfile

## Context

Phase 1 (Delivery Foundation) requires a containerized docs validation environment. ADR 0014 mandates Podman-first, rootless execution with images pinned by digest. The `candelamoon-docs` image is the second of four container image roles (after P1-001 candelamoon-android). It serves as the execution environment for the docs-validate CI job, memtrace-sync support, and evidence audit.

This task follows the P1-001 pattern (green-verified, review phases 1+2 closed). The Containerfile shares common conventions with P1-001: non-root `builder` user (uid/gid 1000), `--network=none` at run-time, digest-pinned base image, inline doc comments.

**Key references:**
- CI architecture: `docs/infrastructure/ci-architecture.md` § "candelamoon-docs" (lines 69-76) defines all image requirements
- Toolchain pins: `docs/infrastructure/toolchain-pins.md` — § `Python 3.11` (line 132-136), § `Node.js 22 LTS` (line 118-124), § `Container Base Images` (line 163-170)
- ADR 0014: `docs/adr/0014-podman-first-execution.md`
- Phase plan: `.maestro-space/maestro-plans/phase-1-delivery-system/phase-plan.md`
- P1-001 reference Containerfile: `infra/containers/candelamoon-android/Containerfile` (green-verified pattern to follow)
- P1-001 root `.containerignore`: `.containerignore` (existing, may need docs-specific additions)

## Instructions for Agent

**Production agent: Vivaldi (DevOps Architect)** — subagent_type: `vivaldi-devops-architect`

Read the handoff file first. It contains your task, acceptance criteria, and context.

**Working directory:** `D:\Repos\CandelaMoon`

**Spec:** `docs/infrastructure/ci-architecture.md` § "candelamoon-docs" (lines 69-76) + § "Common conventions" (lines 53-58)
**Plan:** `.maestro-space/maestro-plans/phase-1-delivery-system/phase-plan.md`, Task P1-002
**Relevant ADRs:** 0014 (Podman-First Execution)
**Reference docs:**
- `docs/infrastructure/ci-architecture.md` — "candelamoon-docs" section (lines 69-76) + "Common conventions" (lines 53-58) define all image requirements
- `docs/infrastructure/toolchain-pins.md` — normative tool versions (Python 3.11, Node.js 22 LTS, pip deps, base image digest)
- `infra/containers/candelamoon-android/Containerfile` — P1-001 reference: follow its structure, non-root user hardening, mtime normalization, inline doc comments, `.containerignore` patterns
- `.containerignore` — existing root file from P1-001; review and append docs-specific exclusions if needed

Your agent identity and full operating rules are defined in your agent file at `.maestro-space/maestro-agents/vivaldi-devops-architect.md`. Read it to understand your role, contract, and deliverables.

**Activity report template:** `.maestro-space/maestro-templates/agent-activity-report.md`

**Bootstrap exception (docs/infra task):** Skip TDD red phase and coverage audit (steps 2 and 10 of the 14-step cycle). Still produce the Containerfile and verify via `podman build` + toolchain validation commands.

**Implementation notes:**
- The `python:3.11-slim` base does NOT ship a pre-existing uid-1000 user — plan for `groupadd -g 1000 builder && useradd -u 1000 -g builder -m builder` (simpler than P1-001's rename logic)
- pip deps should be installed from a `requirements.txt` embedded in the Containerfile or in an adjacent `infra/containers/candelamoon-docs/requirements.txt`
- Node.js 22 LTS: install from the official NodeSource tarball or nodesource setup script; pin the major version
- `markdownlint-cli` is the npm package; install globally via `npm install -g markdownlint-cli`
- Link checker: use `markdown-link-check` (npm) or `linkchecker` (pip) — Vivaldi decides based on what runs best offline in the slim image
- Design validator entrypoint: a shell script at `/usr/local/bin/validate-design` that wraps the validation commands; for MVP, the validator just asserts that the schema files, pip tools, and node tools are present and runnable (the actual validation logic against `docs/` content is a follow-up in P1-017)
- Follow the P1-001 security patterns: `DEBIAN_FRONTEND=noninteractive`, `--no-install-recommends`, fail-closed on every step, mtime normalization to `$SOURCE_DATE_EPOCH`
- Use the same `builder` uid/gid as P1-001 (1000:1000) for cache volume compatibility

**After completing your work:**
1. Update the handoff file's `implementation_artifacts` section with created/modified files
2. Set `green_phase_verified: true` upon successful `podman build` + validation
3. Update `head_sha` with the current commit SHA
4. Write the Agent Output section below with your actions and verification
5. Write a parallel activity report (JSON + MD) in the task folder

## Agent Output

### Vivaldi (DevOps Architect) — Implementation (2026-08-09)

#### Actions

1. **Read** the handoff, `docs/infrastructure/ci-architecture.md`, `docs/infrastructure/toolchain-pins.md`, `docs/adr/0014-podman-first-execution.md`, `infra/containers/candelamoon-android/Containerfile` (P1-001 reference), and `.containerignore` to lock the spec.
2. **Resolved** the `python:3.11-slim` base image digest: `podman pull docker.io/library/python:3.11-slim` → `podman image inspect --format '{{index .RepoDigests 0}}'` → `docker.io/library/python@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` (image ID `245f9d32fabaec22e749aa5cfef79996088135e9d4410f4e7ebe133c2be98132`, created 2026-08-05 01:12:29 UTC, in-image `python3 --version` reports `Python 3.11.15`, `cat /etc/os-release` reports `Debian GNU/Linux 13 (trixie)` / `DEBIAN_VERSION_FULL 13.6`).
3. **Verified** the base ships no pre-existing uid-1000 user (`getent passwd 1000` returns nothing; `getent passwd builder` returns nothing) — confirmed the simpler `groupadd + useradd` path per the handoff's implementation note.
4. **Pinned** Node.js to `22.23.2` (latest 22.x LTS security release, 2026-07-28, line "Jod"). Resolved the SHA-256 of `node-v22.23.2-linux-x64.tar.xz` from `https://nodejs.org/dist/v22.23.2/SHASUMS256.txt` → `d60acfe00a2932254bb0ad20e01b0d74397a0875595de719654b214f4b03f307`.
5. **Wrote** `infra/containers/candelamoon-docs/Containerfile` (~290 lines, 19 steps: 1 FROM, 4 ENV, 10 RUN, 1 COPY ×2, 1 USER, 1 WORKDIR, 1 CMD). Inline comments cite `ci-architecture.md § candelamoon-docs` / `Common conventions`, `toolchain-pins.md § Python 3.11` / `Node.js 22 LTS` / `Container Base Images`, and ADR 0014 at every step (AC10).
6. **Wrote** `infra/containers/candelamoon-docs/requirements.txt` with the three pip pins (`jsonschema==4.23.0`, `pyyaml==6.0.2`, `yamllint==1.37.1`); the file's header documents the link-checker choice and the reason `linkchecker` was rejected.
7. **Wrote** `infra/containers/candelamoon-docs/validate-design` — the MVP design-validator entrypoint that asserts every required tool is installed and runnable. Uses `importlib.metadata` (deprecation-free) for Python versions and unanchored regex matching so a leading product name (e.g. `yamllint 1.37.1`) does not break the check. Supports `--verbose` for log-friendly CI output.
8. **Built** the image: `podman build --no-cache -t candelamoon-docs:test -f infra/containers/candelamoon-docs/Containerfile .` → succeeded.
9. **Iterated** to fix two issues found during green-phase verification:
   - **Issue A** (validate-design): `yamllint --version` outputs `yamllint 1.37.1` (with a leading product name); the original anchored regex `^[0-9]+\.` did not match. Switched to unanchored `[0-9]+\.[0-9]+` patterns so all CLIs work uniformly. Also replaced `jsonschema.__version__` (deprecated) with `importlib.metadata.version('jsonschema')` to drop the deprecation warning.
   - **Issue B** (AC8 reproducibility): the first two `--no-cache` builds produced identical file counts and nearly-identical total bytes, but `/home/builder/.npm/_logs/` contained timestamped npm debug-log files whose CONTENT varied between builds (different timestamps, durations, paths) — defeating AC8 even though mtimes were normalized. Fixed by adding `rm -rf /home/builder/.npm/_logs /home/builder/.npm/_cacache` to the npm install RUN, with a comment explaining why.
10. **Re-built** the image after the two fixes; build succeeded.
11. **Verified** AC7 (per the `podman run --rm --network=none candelamoon-docs:test ...` commands in the verification table below).
12. **Verified** AC8 reproducibility: two `--no-cache --source-date-epoch=1735689600 --rewrite-timestamp` builds produce identical file counts, total bytes, pip freeze (10 entries), and npm modules (4 global packages). The image size matches exactly: 770,379,387 bytes both times. Image digests differ (sha256:a1090f0f... vs sha256:38a604f5...) due to Podman layer-tar gzip non-determinism — carried forward from P1-001 AC8 as known debt.
13. **Verified** AC6 (`--network=none`): DNS resolution fails (`curl: (6) Could not resolve host: pypi.org`), TCP connections fail (`bash: connect: Network is unreachable`).
14. **Verified** AC9: the existing root `.containerignore` (from P1-001) is adequate for the docs build context. The Containerfile only COPYs two small files (`infra/containers/candelamoon-docs/requirements.txt` and `infra/containers/candelamoon-docs/validate-design`); the `.git/` (639 files), `.maestro-space/` (110 files), and `docs/handoffs/` (4 files) directories are all correctly excluded by the existing patterns. No additional exclusions were needed.
15. **Updated** `docs/infrastructure/toolchain-pins.md`: filled in the resolved python:3.11-slim digest in `Container Base Images` and `Python`; resolved Node.js 22.23.2 SHA-256 in `Node`; added a `candelamoon-docs pip pins` and `candelamoon-docs npm pins` subsection to the `Python` and `Node` sections respectively.
16. **Wrote** the parallel activity report (`vivaldi-devops-architect-activity-report.md` and `.json`).
17. **Updated** the handoff: `implementation_artifacts`, `green_phase_verified: true`, `head_sha`, `known_debt` additions, and the Agent Output section.

#### Verification table (AC7)

| Command | Expected | Observed |
|---|---|---|
| `podman pull docker.io/library/python:3.11-slim` then `podman image inspect --format '{{index .RepoDigests 0}}' ...` | digest `sha256:...` | `docker.io/library/python@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` |
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
| `podman run --rm --network=none candelamoon-docs:test curl https://pypi.org/` | network unreachable | `curl: (6) Could not resolve host: pypi.org` (exit 6) |
| AC8: two `--no-cache --source-date-epoch=1735689600 --rewrite-timestamp` builds | identical file counts and total bytes | `/opt/node 9532/232233887` (both), `/usr/local 2440/45961513` (both), `/home/builder 0/0` (both), `pip freeze` identical (both), image size 770,379,387 bytes (both); image digest differs: `sha256:a1090f0f...` vs `sha256:38a604f5...` (Podman gzip non-determinism, known debt) |

#### Deviations

1. **Link checker delivered as `markdown-link-check` (npm) rather than `linkchecker` (pip).** The handoff gave Vivaldi the choice. Rationale: (a) `markdown-link-check` is purpose-built for Markdown link validation and pairs naturally with `markdownlint-cli` on the same npm toolchain; (b) the pip alternative `linkchecker` carries many additional Python deps (BeautifulSoup, requests, ...) that bloat the slim base image; (c) using a single toolchain (npm) for both markdown lint and link check keeps the image simpler. Recorded in `requirements.txt` and `toolchain-pins.md § Node` "candelamoon-docs npm pins". AC3 wording was updated to reflect this.
2. **Base image does not need the P1-001 rename-the-base-user logic.** `python:3.11-slim` ships no pre-existing uid-1000 user (verified). Used the simpler `groupadd --gid 1000 --system builder && useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash --no-log-init builder` path with `usermod --lock` + `usermod -G builder builder` for the same postcondition set as P1-001 (uid/gid/supplementary-groups/sudoers-free/home-owner).
3. **Build-time network expanded to include `nodejs.org`.** AC5 in the handoff said "pypi.org, files.pythonhosted.org (pip), registry.npmjs.org (npm)" — but the Node.js binary distribution lives on `nodejs.org`, not the npm registry. The Containerfile comment at the Node.js install step documents this; the new effective build-time allowlist is `{pypi.org, files.pythonhosted.org, registry.npmjs.org, nodejs.org}`. The AC5 line in the handoff was updated to reflect this.
4. **Validator script is MVP; real validation logic deferred to P1-017.** The handoff said "MVP: assert tools are present and runnable" and the actual schema/ADR/capability-matrix/evidence-manifest validation is a follow-up. The shipped `validate-design` does exactly that MVP and includes a `--verbose` mode for log-friendly CI output.

#### Known issues

1. **AC8 image digest is not bit-reproducible** — same root cause as P1-001: Podman layer-tar gzip is non-deterministic. Image content IS reproducible (file counts, total bytes, image size 770,379,387 bytes all match exactly across two `--no-cache` builds). Resolution path: pin every downloaded artifact by SHA-256 (Node.js tarball already done; apt and PyPI rely on the base-image digest + HTTPS); switch to a deterministic compression backend (e.g. zstd -19) when Podman supports it. Out of scope for P1-002.
2. **Design validator is MVP** — see Deviations §4. P1-017 will add the real schema/ADR/capability-matrix/evidence-manifest validation scripts that the docs-validate job will invoke. The MVP is the pre-condition: the scripts will run inside this image and assume every tool the MVP checks is present.
3. **No SHA-256 verification on apt or PyPI downloads** — apt packages are versioned implicitly by the base image digest (the python:3.11-slim base pins its own apt sources and package revisions). PyPI wheels are downloaded over HTTPS and pinned by exact version in `requirements.txt`, but not cryptographically verified at build time. Recording SHA-256s in `toolchain-pins.md` and adding `pip install --require-hashes` against a `requirements.txt` that includes `--hash=sha256:...` per line is a small follow-up (mirrors P1-001's known debt for cmdline-tools / Gradle / Robolectric).
4. **Base image digest resolution timestamp not recorded alongside Temurin 17** — toolchain-pins.md records the `2026-08-04 01:27:24 UTC` creation date for the Temurin 17 base (P1-001); the python:3.11-slim digest was resolved on 2026-08-09 with the in-image `python3 --version` (3.11.15) and the OS (`Debian 13 trixie / DEBIAN_VERSION_FULL 13.6`) recorded. If a future pin bump lands, both pieces of evidence should be re-captured in the same PR.

#### Handoff to

Bernstein for Review Phase 1 dispatch (Berlioz/Bartók/Verdi). Pass `infra/containers/candelamoon-docs/Containerfile`, `infra/containers/candelamoon-docs/requirements.txt`, and `infra/containers/candelamoon-docs/validate-design` to the review agents; point them at the AC2-AC9 evidence in the verification table above and the AC8 partial-pass caveat in Known Issues §1. The P1-002 follow-up tasks (P1-017 design-validator logic; P1-022 dependency vulnerability remediation) should be visible in the phase plan and can be tracked in the same review cycle.
