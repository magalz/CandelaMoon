---
change_id: "P1-003"
phase: "Phase 1"
task: "Create candelamoon-security Containerfile"
status: "in-progress"
repository: "magalz/CandelaMoon"
branch: "phase1/p1-003-candelamoon-security-containerfile"
base_sha: "26a203c1873b166c4df3698c63aa76e10dde8125"
head_sha: ""
pr_url: ""
acceptance_criteria:
  - "AC1: Containerfile at `infra/containers/candelamoon-security/` builds successfully with `podman build`."
  - "AC2: Base image is digest-pinned (python:3.11-slim or equivalent; digest resolved via ci-architecture.md procedure)."
  - "AC3: Non-root `builder` user (uid/gid 1000) is the final USER directive."
  - "AC4: Installed tools include Node.js 22 LTS, Python 3.11 + pip deps, security scanners (gitleaks, trivy, syft; semgrep or bandit; cosign for artifact verification)."
  - "AC5: Follows all common conventions from ci-architecture.md (source mount at /workspace, cache mounts, output mounts, network policy, mtime normalization for SOURCE_DATE_EPOCH)."
  - "AC6: Build-time network endpoints are documented inline (GitHub releases for scanner binaries, PyPI, npm registry, nodejs.org, deb.debian.org)."
  - "AC7: Run-time network policy is `--network=none` by default; `cosign verify` declares registry access explicitly."
  - "AC8: Image is reproducible — two `--no-cache` builds produce file-count-identical content under /opt, /usr/local, and /home/builder."
  - "AC9: `.containerignore` at repo root excludes non-build artifacts; build context stays minimal."
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
  session_handout: ".maestro-space/maestro-works/phase-1-delivery-system/p1-003-candelamoon-security-containerfile/session-handout.md"
  memtrace_repo_id: "CandelaMoon"
memtrace_indexed_sha: ""
memtrace_episode_ids: []
capability_rows: []
adrs:
  - "0014"
verification:
  tests_pass: false
  memtrace_review: false
  acceptance_audit: false
  edge_case_hunt: false
  blind_hunt: false
  security_review: false
  policy_check: false
known_debt: []
rollback_strategy: "Delete `infra/containers/candelamoon-security/` directory and revert the task branch commits."
---

# Task: P1-003 — Create candelamoon-security Containerfile

## Context

This is the third of four container images defined in ci-architecture.md § "Images". The `candelamoon-security` image provides the containerized security-scanning environment for the CandelaMoon delivery pipeline. It is used by the `security-scan`, `sbom-delta`, image-promotion scans, and `release-sign` verification jobs.

The pattern follows P1-001 (candelamoon-android) and P1-002 (candelamoon-docs): digest-pinned base image, non-root `builder` user (uid 1000), mtime normalization for reproducibility, inline doc comments linking every step to governing docs, and fail-closed every step.

**Spec reference**: `docs/infrastructure/ci-architecture.md` § "candelamoon-security" (lines 78-85) and § "Common conventions" (lines 53-58).
**Toolchain pins**: `docs/infrastructure/toolchain-pins.md` § "Node.js 22 LTS", "Python", "Container Base Images".
**ADR**: 0014 (Podman-First Execution).
**Base image**: `python:3.11-slim` (same base and digest as candelamoon-docs; digest `sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` — resolves to Python 3.11.15 on Debian 13 "trixie").
**Reference Containerfiles**: 
- `infra/containers/candelamoon-android/Containerfile` (P1-001 — the canonical pattern)
- `infra/containers/candelamoon-docs/Containerfile` (P1-002 — same base image, Node.js/Python pattern)

## Instructions for Agent

1. Read this handoff first, then read the spec and reference Containerfiles.
2. Work on `phase1/p1-003-candelamoon-security-containerfile` in `D:\Repos\CandelaMoon`.
3. Create `infra/containers/candelamoon-security/Containerfile` following the established patterns from P1-001 and P1-002:
   - **Base image**: `docker.io/library/python:3.11-slim@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` (digest already resolved in P1-002; record resolution metadata inline).
   - **Reproducibility**: `SOURCE_DATE_EPOCH=1735689600`, `LC_ALL=C.UTF-8`.
   - **OS helpers**: `ca-certificates`, `curl`, `git`, `xz-utils` (per P1-002 pattern; needed for scanner binary downloads).
   - **Node.js 22 LTS**: version 22.23.2, SHA-256 verified tarball from nodejs.org. Install to `/opt/node`. Pins: `NODE_VERSION=22.23.2`, `NODE_SHA256_LINUX_X64=d60acfe00a2932254bb0ad20e01b0d74397a0875595de719654b214f4b03f307` (already resolved in toolchain-pins.md).
   - **Non-root builder user**: uid/gid 1000, created from scratch (like P1-002 — the python:3.11-slim base has no pre-existing uid-1000 user). Lock password, strip supplementary groups, validate identity.
   - **Python pip deps**: security-specific pip packages. Create `infra/containers/candelamoon-security/requirements.txt` with pinned security tooling deps and a `requirements.lock` with `--hash=sha256:...` lines. Use the SEC-02 root/builder split pattern from P1-002: download as builder, install as root with `--only-binary=:all:`.
   - **Security scanners** (pinned, never `latest`):
     - **gitleaks** — secret scanning. Install via npm: `gitleaks` (or via Go binary from GitHub releases — document the choice).
     - **trivy** — vulnerability scanning. Install from GitHub releases (Go binary; statically linked).
     - **syft** — SBOM generation. Install from GitHub releases (Go binary; statically linked).
     - **cosign** — artifact signature verification. Install from GitHub releases (Go binary; statically linked).
     - **semgrep** — SAST. Install via pip in requirements.txt (semgrep is a Python package). Alternative: bandit for Python-only scans — semgrep covers multiple languages and is already used in CI (mobsfscan.yml implies SAST is active).
     - **npm audit** — built into Node.js/npm (no additional install).
     - **pip-audit** — install via pip in requirements.txt.
   - **Build-time network allowlist**: `nodejs.org` (Node.js tarball), `github.com` + `objects.githubusercontent.com` (scanner binaries from GitHub releases), `pypi.org` + `files.pythonhosted.org` (pip), `registry.npmjs.org` (npm), `deb.debian.org` (apt).
   - **Run-time mounts**: source ro at `/workspace`, `trivy-db` cache (ro), `go-pkg` cache, `reports` + `artifacts` output.
   - **Mtime normalization**: touch `/opt/node`, `/usr/local`, `/home/builder`, `/workspace` to `SOURCE_DATE_EPOCH`.
   - **Final runtime**: `USER builder`, `WORKDIR /workspace`, default `CMD ["bash"]` (or an entrypoint that prints installed tool versions for verification).
4. Verify with `podman build -t candelamoon-security:dev -f infra/containers/candelamoon-security/Containerfile .`
5. After the build, verify each installed tool reports its version: `podman run --rm --network=none candelamoon-security:dev <tool> --version`.
6. Verify reproducibility: run a second `podman build --no-cache` and compare file counts.
7. Update this handoff: populate `implementation_artifacts`, set `head_sha`, complete the Agent Output section.

## Agent Output

### Vivaldi (DevOps Architect) — Implementation (2026-08-09)

*To be filled by Vivaldi after implementation.*

