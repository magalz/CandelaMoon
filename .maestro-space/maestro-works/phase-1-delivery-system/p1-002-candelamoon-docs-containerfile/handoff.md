---
change_id: "P1-002"
phase: "Phase 1"
task: "Create candelamoon-docs Containerfile — containerized docs validation environment (Python 3.11 slim, jsonschema, yamllint, markdown-link-check, Node.js 22 LTS + markdownlint-cli, design validator)"
status: "in-progress"
repository: "magalz/CandelaMoon"
branch: "phase1/p1-002-candelamoon-docs-containerfile"
base_sha: "86d3c216eb2539cec76556978cc7e36941dfaca8"
head_sha: ""
pr_url: ""
acceptance_criteria:
  - "AC1: Containerfile exists at `infra/containers/candelamoon-docs/Containerfile`."
  - "AC2: Base image is digest-pinned `docker.io/library/python:3.11-slim@sha256:<DIGEST>` (resolved via `podman pull` + `podman image inspect`; recorded in toolchain-pins.md § `Container Base Images` and § `Python`)."
  - "AC3: Installed tools match toolchain-pins.md: Python 3.11 (from base) + pinned pip deps (jsonschema, pyyaml, yamllint, markdown-link-check or equivalent link checker); Node.js 22 LTS + markdownlint-cli; design validator entrypoint at `/usr/local/bin/validate-design` (schema validation for architecture schemas, ADR register, capability matrix, evidence manifest); ADR/capability-matrix validation scripts."
  - "AC4: Non-root `builder` user (uid 1000, gid 1000) is the final USER directive. All pip/node caches (/home/builder/.cache/pip, /home/builder/.npm) chown'd to builder:builder."
  - "AC5: Build-time network limited to pypi.org, files.pythonhosted.org (pip), registry.npmjs.org (npm)."
  - "AC6: Run-time network is `--network=none` (verified by AC7 validation commands)."
  - "AC7: `podman build` succeeds from repo root; `podman run --rm --network=none <image> python3 --version` reports Python 3.11.x; `podman run --rm --network=none <image> node --version` reports Node.js 22.x; `podman run --rm --network=none <image> markdownlint --version` reports a valid version; `podman run --rm --network=none <image> yamllint --version` reports a valid version."
  - "AC8: Image content is reproducible: two `--no-cache` builds produce identical pip freeze output and identical file counts under /usr/local and /home/builder. Image digest non-reproducibility is tracked as known debt (Podman gzip non-determinism per P1-001 AC8)."
  - "AC9: Root `.containerignore` (existing from P1-001) is adequate for the docs build context — verified by comparing build context size with and without the file, or by explicit inspection. Any additional docs-specific exclusions are appended."
  - "AC10: Containerfile carries inline comments linking each section to its governing doc (ci-architecture.md § `candelamoon-docs` / `Common conventions`; toolchain-pins.md § `Python 3.11` / `Node.js 22 LTS` / `Container Base Images`; ADR 0014)."
tdd_artifacts:
  atdd_checklist: ""
  test_files: []
  red_phase_verified: false
implementation_artifacts:
  files_created: []
  files_modified: []
  green_phase_verified: false
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
  tests_pass: false
  memtrace_review: false
  acceptance_audit: false
  edge_case_hunt: false
  blind_hunt: false
  security_review: false
  policy_check: false
known_debt:
  - "AC8: Podman layer-tar gzip is non-deterministic (known from P1-001). Image content will be reproducible; image digest will not be bit-reproducible. Tracked as cross-task known debt."
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

### <Agent Name> — <Phase> (<date>)

[To be filled by each dispatched agent.]
