# Session Handout — P1-002 candelamoon-docs Containerfile

**Date**: 2026-08-09
**Task**: P1-002 — Create candelamoon-docs Containerfile (containerized docs validation environment: Python 3.11 slim, jsonschema, yamllint, markdown-link-check, Node.js 22 LTS + markdownlint-cli, design validator)
**ADR**: 0014 (Podman-First Execution)
**Spec**: `docs/infrastructure/ci-architecture.md` § `candelamoon-docs` (lines 69-76) + § `Common conventions` (lines 53-58); `docs/infrastructure/toolchain-pins.md` § `Python 3.11` (line 130-145) + § `Node 22 LTS` (line 116-128) + § `Container Base Images` (line 170-186)
**Agent**: Schubert (Tech Writer) — final documentation dispatch for this task
**Produced for**: Bernstein (orchestrator) / @magalz (human merge approval)

---

## Current State

- **Branch**: `phase1/p1-002-candelamoon-docs-containerfile`
- **Head SHA**: `47e1a9f55b6b19772bcc21439097af46de9b68be` (47e1a9f5; this dispatch will add a docs commit on top — see "Code-impacting commits" in Rollback Strategy)
- **Base SHA**: `86d3c216eb2539cec76556978cc7e36941dfaca8`
- **PR URL**: TBD (PR not yet opened; recommended to be opened from this branch into `moonlight-noir` after this Schubert dispatch lands)
- **Memtrace repo_id**: `CandelaMoon`
- **Memtrace indexed SHA**: `2118b61cd1dc49d600b36f06f7d832d5a7b8b824` (base SHA; equals `memtrace_indexed_sha` recorded in handoff; P1-002 changes are infra-only and do not require a Memtrace re-index for symbol discovery, but the PR should trigger a re-index before merge for graph consistency)
- **Memtrace index**: not re-measured for this dispatch; the P1-002 code change is infra-only (Containerfile + 5 support files + toolchain-pins.md updates) and touches no application symbols that would alter the symbol/edge counts
- **Handoff status**: `done` (handoff `status` field; matches the evidence-manifest schema enum)
- **UAT decision**: `passed` — all ten acceptance criteria met, both review phases closed with fixes applied (Review Phase 1: 11 applied + 3 deferred + 8 dismissed; Review Phase 2: SEC-01 + SEC-02 applied + 4 deferred to CI + 1 dismissed), full AC7 regression suite green under `--network=none` on the final `candelamoon-docs:phase2` image (id `127a1439acb4…`, 23/23 build steps, 771,003,453 bytes)

## Completed Evidence

| Gate | Result | Evidence |
|---|---|---|
| **Red phase (ADR 0016)** | Skipped — bootstrap exception per handoff § Instructions (infra/docs task, no test files) | handoff line 275 |
| **Green phase (focused)** | 23/23 Containerfile build steps green on final image (`podman build` succeeds) | handoff Agent Output § Vivaldi step 8 + Bach phase-1 step 10 + Bach phase-2 step 4; logs `%TEMP%/opencode/p1-002-verify/build-review*.log`, `%TEMP%/opencode/p1-002-review/`, `%TEMP%/opencode/p1-002-phase2/` |
| **Green phase (full suite)** | AC7 validation suite green on every post-patch image: `python3 --version` (3.11.15), `node --version` (v22.23.2), `npm --version` (10.9.8), `markdownlint --version` (0.45.0), `yamllint --version` (1.37.1), `markdown-link-check --version` (3.13.7), `id` (uid=1000 builder, password-locked, sudoers-free, supplementary groups stripped), default-CMD `validate-design` (8/8 OK), `--network=none` curl test (DNS fail, exit 6), `pip freeze` (10 entries, matches lock), `npm ls -g --depth=0` (165 packages incl. markdownlint-cli + markdown-link-check) | handoff Vivaldi Verification table + Bach phase-1 Verification table + Bach phase-2 Verification table |
| **Base comparison** | N/A (bootstrap exception: no test files added; image is a new role rather than a baseline promotion) | handoff line 275 |
| **Review Phase 1** | 11 triaged findings all `applied`; 3 `deferred` (full APT snapshotting → P1-005; markdown-link-check offline config → P1-017; real design validation logic → P1-017); 8 `dismissed` (x64-only Node payload; /workspace-out mount points; USER ordering; APT paths not normalized; no negative tests; linkchecker removal; bind mount ownership; 1-byte image size difference) | handoff `review_phase_1.triaged_findings` (patches 1-11 + defer-1/2/3 + dismiss-1..8) |
| **Review Phase 2** | 7 triaged findings: SEC-01 + SEC-02 `applied` (workspace import isolation; wheel-only pip + builder-account split); SEC-03..SEC-06 `defer-to-CI` (build-time network allowlist; npm runtime sandbox; runtime network isolation; apt drift); SEC-07 `dismissed` (default validator is MVP tool-presence only — P1-017 scope) | handoff `review_phase_2.triaged_findings` |
| **Coverage audit (ADR 0019)** | Skipped — bootstrap exception (infra/docs task, no test surface) | handoff line 275 + handoff `coverage_audit.rating: n/a` |
| **UAT** | **passed** — all gates green; see "UAT Decision" below | this document + handoff `uat.status: passed` |
| **`git diff --check`** | clean (no whitespace errors on tracked files; untracked files in the task folder are framework artifacts, not changes) | `git diff --check` on the working tree (post-Containerfile / lockfile / validate-design changes) |
| **Workflow repair (if any)** | none | n/a |
| **PR opened** | TBD | TBD (recommended next action; see "Pending Work" § 8) |
| **Memtrace GitHub PR review** | n/a (PR not yet opened) | n/a |

### Acceptance criteria status (10/10)

| AC | Result | Evidence |
|---|---|---|
| **AC1** | PASS | `infra/containers/candelamoon-docs/Containerfile` exists (created 2026-08-09, commit `425c17f5`; final state at `91bd8403` after Review Phase 2 patches) |
| **AC2** | PASS | Base image is digest-pinned `docker.io/library/python:3.11-slim@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553`; recorded in `docs/infrastructure/toolchain-pins.md` § `Container Base Images` (line 177) and § `Python` (line 137) |
| **AC3** | PASS | Toolchain matches: Python 3.11.15 (from base) + pinned pip deps (jsonschema 4.23.0, pyyaml 6.0.2, yamllint 1.37.1; link checker delivered as npm `markdown-link-check@3.13.7` per Deviations §1); Node.js 22.23.2 + markdownlint-cli 0.45.0; design validator entrypoint at `/usr/local/bin/validate-design` (MVP: 8 tool-presence checks with exact version matching) |
| **AC4** | PASS | Non-root `builder` user (uid 1000, gid 1000) is the final `USER` directive. All pip/node caches (`/home/builder/.cache/pip`, `/home/builder/.npm`) chown'd to builder:builder. SEC-02 moved the builder-account creation above the pip block; the pip section temporarily switches USER to root for the offline install only, then back to builder (documented in the final-USER comment) |
| **AC5** | PASS | Build-time network limited to five domains documented in the Containerfile header allowlist comment and inline at each install step: `pypi.org` + `files.pythonhosted.org` (pip), `registry.npmjs.org` (npm), `nodejs.org` (Node.js binary tarball), `deb.debian.org` (apt). Consolidation applied as patch-11 (B-03 / B-04 / A-02) |
| **AC6** | PASS | Run-time network is `--network=none` (verified: `curl https://pypi.org/` → `curl: (6) Could not resolve host: pypi.org`, exit 6) |
| **AC7** | PASS | `podman build` succeeds (23/23 steps on the final SEC-02 image `127a1439acb4`); `podman run --rm --network=none <image> python3 --version` → `Python 3.11.15`; `node --version` → `v22.23.2`; `markdownlint --version` → `0.45.0`; `yamllint --version` → `yamllint 1.37.1`; `markdown-link-check --version` → `3.13.7`; default `validate-design` → `OK: all design validator tools present and runnable` (exit 0, 8/8 OK) |
| **AC8** | **PARTIAL PASS** (tracked as known debt) | Image **content** is reproducible: two `--no-cache --source-date-epoch=1735689600 --rewrite-timestamp` builds produce identical file counts and total bytes (`/opt/node 9446/231786503`, `/usr/local 2446/45964552`, `/home/builder 3/4553`, `/workspace 0/0` both), identical `pip freeze` (md5 `a6a8985a...`), identical file lists (md5 `dca115fa...`), and identical image size 771,003,453 bytes (1-byte diff between phase2 builds, dismissed A-03; same root cause as P1-001). Image **digest** is not bit-reproducible because Podman layer-tar gzip is non-deterministic — carried forward from P1-001 as cross-task known debt. Resolution path documented in "Known Debt" |
| **AC9** | PASS | Root `.containerignore` (existing from P1-001) is adequate for the docs build context. The Containerfile only COPYs `requirements.txt`, `requirements.lock`, `package.json`, `package-lock.json`, and `validate-design` from the build context; `.git/` (639 files), `.maestro-space/` (110 files), and `docs/handoffs/` (4 files) are correctly excluded by the existing patterns. No additional exclusions needed |
| **AC10** | PASS | Containerfile carries inline comments at every section linking to `ci-architecture.md` § `candelamoon-docs` / § `Common conventions`, `toolchain-pins.md` § `Python 3.11` / § `Node 22 LTS` / § `Container Base Images`, and ADR 0014 |

### Review Phase 1 stats (Berlioz / Bartók / Verdi)

- **Berlioz (Blind Hunter)** — `findings-phase-1-berlioz.md` / `.json` — produced blind-adversarial findings (B-01..B-18); 8 of 18 contributed to the 11 applied patches
- **Bartók (Edge Case Hunter)** — `findings-phase-1-bartok.md` / `.json` — produced edge-case findings (BAR-001..BAR-015); 11 of 15 contributed to the 11 applied patches (overlap with Berlioz consolidated)
- **Verdi (Acceptance Analyst)** — `findings-phase-1-verdi.md` / `.json` — produced acceptance-criterion findings (A-01..A-03); A-02 contributed to patch-11 (network allowlist consolidation), A-03 dismissed (1-byte image size diff), A-01 rolled into defer-3 (real validation logic)
- **Triaged patches applied**: 11 (B-06/BAR-003/004 pip lock with hashes; B-07/BAR-005 npm lock; B-11/BAR-013 PIP_NO_CACHE_DIR scoping; B-12/BAR-010 /workspace pre-create; B-14/BAR-007 exact version pins; B-15/BAR-006 real Python imports; B-16/BAR-008 arg validation; B-17 default CMD; BAR-009 sudoers loop; BAR-015 timeout; B-03/B-04/A-02 network allowlist consolidation)
- **Deferred**: 3 (full APT snapshotting → P1-005; markdown-link-check offline config → P1-017; real design validation logic → P1-017)
- **Dismissed**: 8 (x64-only Node payload; /workspace-out mount points; USER ordering; APT paths not normalized; no negative tests; linkchecker removal; bind mount ownership; 1-byte image size difference)
- **Open findings carried to Review Phase 2**: see Bach phase-1 handoff Agent Output § Handoff to

### Review Phase 2 stats (Brahms / Stravinsky)

- **Brahms (Blue Team / Defensive)** — `findings-phase-2-brahms.md` / `.json` — 7 findings (SEC-01..SEC-07): workspace import hijack (HIGH), wheel-vs-sdist pip execution as root (CRITICAL), build-time network allowlist enforcement (HIGH), npm runtime sandboxing (HIGH), runtime network isolation (HIGH), apt package version drift (MEDIUM), default validator is tool-presence only (MEDIUM)
- **Stravinsky (Red Team / Offensive)** — `findings-phase-2-stravinsky.md` / `.json` — produced the same 7 attack-surface findings (SEC-01..SEC-07) using an offensive lens; Brahms consolidated the defensive-side dispositions, Stravinsky cross-validated with red-team attack scenarios
- **Triaged dispositions**:
  - `applied`: SEC-01 (`python3 -I` + `cd /` in `validate-design`; workspace imports isolated), SEC-02 (builder-account split + wheel-only `pip download` → root `pip install --no-index` from local wheelhouse)
  - `defer-to-CI (P1-005 / P1-010)`: SEC-03 (build-time network allowlist enforcement), SEC-04 (npm runtime JavaScript sandboxing), SEC-05 (runtime network isolation), SEC-06 (apt version drift)
  - `dismissed`: SEC-07 (default validator is MVP tool-presence only — accurate but a P1-017 capability statement, not a container-security defect)

### Known debt items (full table in "Known Debt" section below)

- AC8 image-digest non-reproducibility (Podman gzip non-determinism, carried from P1-001)
- Design validator is MVP (P1-017 follow-up)
- npm audit: 8 vulnerabilities in locked transitive tree (P1-022 scope)
- ci-architecture.md § candelamoon-docs "Build-time network" still lists only 2 of 5 allowlist domains
- SEC-03..SEC-06 deferred to CI
- STR-10 archive resource bounds (open across P1-001 and P1-002)
- ci-architecture.md § candelamoon-docs Containerfile path line carries no status note (deferred to next PR)

## Artifacts Produced

| Path | Description | Tracked? |
|---|---|---|
| `infra/containers/candelamoon-docs/Containerfile` | Containerfile (Python 3.11.15 slim, Node.js 22.23.2, hash-locked pip tree, npm-locked tree, SEC-01 isolated validate-design, SEC-02 wheel-only pip, non-root builder, mtime normalization, default CMD validate-design) | **yes** (commit `91bd8403` after SEC-01/SEC-02 patch round; intermediate `425c17f5` for initial Vivaldi build and `ff6c64d0` for Review Phase 1 patch round) |
| `infra/containers/candelamoon-docs/requirements.txt` | Pinned direct pip deps (jsonschema 4.23.0, pyyaml 6.0.2, yamllint 1.37.1) with header documenting the linkchecker rejection | **yes** (commit `425c17f5`; minor edit in `ff6c64d0`) |
| `infra/containers/candelamoon-docs/requirements.lock` | Hash-locked transitive pip tree (9 packages = 3 direct + 6 transitive, every artifact carrying `--hash=sha256:...`; generated with `uv pip compile --generate-hashes --python-version 3.11 --python-platform x86_64-unknown-linux-gnu requirements.txt`) | **yes** (commit `ff6c64d0`) |
| `infra/containers/candelamoon-docs/package.json` | Pinned direct npm deps (markdownlint-cli 0.45.0, markdown-link-check 3.13.7) with exact pins | **yes** (commit `ff6c64d0`) |
| `infra/containers/candelamoon-docs/package-lock.json` | lockfileVersion 3, 165 packages with integrity hashes (`npm install --package-lock-only` on npm 11.13.0) | **yes** (commit `ff6c64d0`) |
| `infra/containers/candelamoon-docs/validate-design` | 8 tool-presence checks with anchored exact pins, real Python imports (`python3 -I`), default CWD `/`, arg validation (exit 2 on unknown/extra), `timeout 30` per probe | **yes** (commits `425c17f5` + `ff6c64d0` + `91bd8403`) |
| `docs/infrastructure/toolchain-pins.md` | Python base image digest recorded in § `Container Base Images` (line 177) and § `Python` (line 137); Node.js 22.23.2 SHA-256 in § `Node` (line 123); `candelamoon-docs pip pins` subsection (line 139-144) and `candelamoon-docs npm pins` subsection (line 125-127) added | **yes** (commit `425c17f5`; minor edit in `ff6c64d0`) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/handoff.md` | Per-task handoff: status `done`, UAT `passed`, 11 phase-1 patches + 2 phase-2 applied patches + 7 deferred + 9 dismissed, known_debt, Agent Output sections (Vivaldi + Bach phase-1 + Bach phase-2) | **no** (gitignored framework state) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/vivaldi-devops-architect-activity-report.md` / `.json` | Vivaldi (DevOps Architect) initial-build activity report (1 image, 2 green-phase iterations) | **no** (gitignored) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/bach-senior-developer-activity-report.md` / `.json` | Bach (Senior Developer) Review Phase 1 patch round activity report (11 applied + 3 deferred + 8 dismissed) | **no** (gitignored) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/bach-senior-developer-activity-report-phase2.md` / `.json` | Bach Review Phase 2 security patch round (SEC-01 + SEC-02 applied + 4 deferred-to-CI + 1 dismissed) | **no** (gitignored) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/findings-phase-1-berlioz.md` / `.json` | Phase 1 Berlioz (Blind Hunter) findings (B-01..B-18) | **no** (gitignored) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/findings-phase-1-bartok.md` / `.json` | Phase 1 Bartók (Edge Case Hunter) findings (BAR-001..BAR-015) | **no** (gitignored) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/findings-phase-1-verdi.md` / `.json` | Phase 1 Verdi (Acceptance Analyst) findings (A-01..A-03) | **no** (gitignored) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/findings-phase-2-brahms.md` / `.json` | Phase 2 Brahms (Blue Team) findings (SEC-01..SEC-07) | **no** (gitignored) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/findings-phase-2-stravinsky.md` / `.json` | Phase 2 Stravinsky (Red Team) findings (SEC-01..SEC-07) | **no** (gitignored) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/session-handout.md` | This document | **no** (gitignored) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/schubert-tech-writer-activity-report.md` / `.json` | Schubert (Tech Writer) documentation dispatch activity report | **no** (gitignored) |
| `.maestro-space/maestro-plans/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile.md` | Task file: Status → Completed; Session History row added (2026-08-09, Head SHA `47e1a9f5…`) | **no** (gitignored) |
| `.maestro-space/maestro-plans/phase-1-delivery-system/phase-plan.md` | Phase plan: P1-002 row → Completed with evidence link; task-count header updated (4 completed, 3 in development, 15 pending); Next Pending Tasks re-scoped (P1-003 → P1-004) | **no** (gitignored) |
| `docs/infrastructure/ci-architecture.md` | § `candelamoon-docs` Containerfile path line (recommended next PR — see "Pending Work" § 9) | **yes** (this dispatch; deferred) |

## Pending Work

1. **P1-003 (candelamoon-security Containerfile) — next Group A task** — *description*: Containerfile for the security scanning image (semgrep, bandit, osv-scanner/pip-audit, gitleaks, syft, trivy, cosign). *Why pending*: next task in the Group A table; no upstream dependencies. *Dependencies*: spec in `ci-architecture.md` § `candelamoon-security` (lines 78-85). The base image is TBD per spec; the first decision is "python:3.11-slim + scanner binaries" vs "distroless base for scanners only" — that decision is recorded as an ADR candidate and must be ratified before the image is built. *Next session's expected first action*: dispatch Vivaldi to write `infra/containers/candelamoon-security/Containerfile`; the npm-based scanners (gitleaks via npm distribution, semgrep engine dependencies) and the candelamoon-docs Containerfile's package-lock.json / npm-locked tree can be a reference for transitive-locking.

2. **P1-022 (Dependency vulnerability remediation) — Group I** — *description*: Address the 48 Dependabot alerts (1 critical Bouncy Castle, 21 high Netty, 24 medium, 2 low). *Why pending*: depends on Group A being complete (P1-001..P1-004); runs **before P1-005** per the phase plan. *Dependencies*: P1-001 (✓ done), P1-002 (✓ done), P1-003, P1-004 (pending). The 8 npm vulnerabilities in candelamoon-docs's locked tree (4 moderate, 4 high — `glob@11.0.3` and `whatwg-encoding@3.1.1` deprecations noted) and any 48 Dependabot alerts that touch the new Containerfiles are within this task's scope. *Next session's expected first action*: triage the Dependabot alert list against the four pinned images; bump transitive pins and regenerate the lockfiles; run a fresh AC7 + AC8 verification on each.

3. **P1-004 (luminal-contract Containerfile) — Group A** — *description*: Containerfile for the contract-testing image (Python 3.11, protocol fixtures, host-response simulation, parser validation). *Why pending*: parallel to P1-003. *Dependencies*: spec in `ci-architecture.md` § `luminal-contract` (lines 87-94). The base image is python:3.11-slim (same digest as P1-002 per toolchain-pins.md line 179); the candelamoon-docs Containerfile is the closest reference and can be cloned. *Next session's expected first action*: dispatch Vivaldi to write `infra/containers/luminal-contract/Containerfile`; relatively small (Python slim + pip deps).

4. **P1-005 (Build and publish images to GHCR with signatures) — Group B** — *description*: Wire up the promotion gates (SBOM, vulnerability scan, signature, provenance) and publish the four Group A images. *Why pending*: unblocked now that P1-001 and P1-002 are done. *Dependencies*: P1-001 (✓ done), P1-002 (✓ done), P1-003, P1-004 (pending), P1-022 (must precede P1-005 per the phase plan). The deferred SEC-03..SEC-06 controls (build-time network allowlist enforcement, npm runtime sandboxing, runtime `--network=none` enforcement, apt package version drift) land here as CI-side gates, not image-side controls. *Next session's expected first action*: after P1-003, P1-004, and P1-022 land, dispatch Vivaldi to write `.github/workflows/image-promotion.yml` with the gates, the SBOM, the cosign signature, and the GHCR push.

5. **P1-017 (Design validator in candelamoon-docs image and CI) — Group F** — *description*: Replace the MVP `validate-design` with the real schema validation scripts (architecture schemas, ADR register, capability matrix, evidence manifest). *Why pending*: P1-002's MVP is the pre-condition; P1-017 consumes the image. *Dependencies*: P1-002 (✓ done, MVP landed), P1-010 (per-commit CI). The new validator MUST adopt the SEC-01 isolated-import rule (`python3 -I`, explicit `/workspace` paths, image-path imports) — this is documented in the validate-design script header and required by the SEC-01 application note. *Next session's expected first action*: dispatch Vivaldi to write the real validator scripts in the image (e.g. `validate-design-schemas`, `validate-design-adrs`, `validate-design-capabilities`, `validate-design-evidence`) and refactor `validate-design` to call them; integrate into P1-010's docs-validate job.

6. **SEC-03..SEC-06 — P1-005 / P1-010 enforcement** — *description*: Build-time network allowlist enforcement (default-deny build namespace or approved HTTPS proxy permitting only the 5 documented domains), npm runtime JavaScript sandboxing (per-run hardened podman invocation with `--network=none --read-only --cap-drop=ALL --security-opt=no-new-privileges --user=1000:1000`), runtime `--network=none` enforcement (negative test proving the docs-validate job cannot reach an external endpoint), and apt package version drift (Debian snapshot pinning, shared with P1-001). *Why pending*: Brahms deferred to CI; not part of the image-level controls. *Dependencies*: P1-005 (publication job), P1-010 (per-commit CI). *Next session's expected first action*: when the CI workflow is defined, embed the 5-domain allowlist, the hardened podman run command, and the negative test; for the apt drift, set up the apt snapshot proxy in P1-005.

7. **STR-10 (archive resource bounds) — next apply-now patch round** — *description*: Add a guarded-download / check-zip helper with per-archive size / entry-count / expansion budgets (the P1-001 list: cmdline-tools 512 MiB / 2 GiB / 100k, platform-tools 256 MiB / 1 GiB / 50k, Gradle 512 MiB / 2 GiB / 100k, Robolectric 512 MiB / 2 GiB / 250k; P1-002 has only the Node.js tarball at ~80 MiB, so a smaller budget applies). *Why pending*: open across P1-001 and P1-002 from Brahms' review; not addressed in either image yet. *Dependencies*: none (image-only change). *Next session's expected first action*: dispatch Vivaldi or Bach to add the guarded-download helper uniformly to both Containerfiles; verify in-image with a hostile input that exceeds each budget.

8. **PR open for P1-002** — *description*: When this task folder is ready and a human is available, open the PR (`moonlight-noir` ← `phase1/p1-002-candelamoon-docs-containerfile`) with the title pattern `[P1-002] candelamoon-docs Containerfile` and a PR body generated from `.maestro-space/maestro-templates/pr.md`. *Why pending*: this Schubert dispatch completes the documentation side; the PR is the human approval gate. *Dependencies*: human availability. *Next session's expected first action*: dispatch the open-pr-bot workflow (`.github/workflows/create-pr.yml`) or have the human open the PR manually.

9. **ci-architecture.md § candelamoon-docs Containerfile path line — add status note** — *description*: Append a parenthetical status note to the Containerfile path line in `ci-architecture.md` § `candelamoon-docs` (line 70), matching the P1-001 status note pattern at line 61. *Why pending*: Schubert documentation debt (see `known_debt` entry #7); should be bundled with the build-time network spec fix (known_debt entry #4). *Dependencies*: none. *Next session's expected first action*: when the next PR touches the docs Containerfile or its spec, append the status note and fix the build-time network line in the same commit.

## Keys For Next Session

- **Handoff file**: `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/handoff.md` (single source of truth for task state; status `done`, UAT `passed`, 11 phase-1 patches + 2 phase-2 patches applied, 3 + 4 + 9 deferred/dismissed, 7 known-debt entries)
- **Spec**: `docs/infrastructure/ci-architecture.md` § `candelamoon-docs` (lines 69-76) + § `Common conventions` (lines 53-58)
- **ADR register**: `docs/adr/` (relevant: 0014 — Podman-First Execution; 0016 candidate for the security-image base decision; 0019 — coverage audit)
- **Implementation backlog**: `.maestro-space/maestro-plans/phase-1-delivery-system/phase-plan.md` (P1-001 **Completed**, P1-002 **Completed**, P1-003/004 Pending, P1-005 Pending, P1-022 Pending before P1-005, P1-017 Pending after P1-010)
- **Toolchain pins**: `docs/infrastructure/toolchain-pins.md` (Python 3.11-slim base image digest line 137 + line 177; Node.js 22.23.2 SHA-256 line 123; `candelamoon-docs pip pins` line 139-144; `candelamoon-docs npm pins` line 125-127)
- **CI architecture**: `docs/infrastructure/ci-architecture.md` (image role specs at § `candelamoon-android` / `candelamoon-docs` / `candelamoon-security` / `luminal-contract`; pipeline tiers at § `Pipeline Tiers`; cache-key rule at line 40)
- **Task workspace path**: `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/`
- **Task file**: `.maestro-space/maestro-plans/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile.md`
- **Phase plan**: `.maestro-space/maestro-plans/phase-1-delivery-system/phase-plan.md`
- **Containerfile (canonical)**: `infra/containers/candelamoon-docs/Containerfile`
- **Pip lock file**: `infra/containers/candelamoon-docs/requirements.lock` (regenerate with `uv pip compile --generate-hashes --python-version 3.11 --python-platform x86_64-unknown-linux-gnu requirements.txt` from the same UV toolchain version)
- **Npm lock file**: `infra/containers/candelamoon-docs/package-lock.json` (regenerate with `npm install --package-lock-only` on the same host npm 11.x)
- **Validator entrypoint**: `infra/containers/candelamoon-docs/validate-design` (8 tool-presence checks; SEC-01 isolated imports; P1-017 will extend)
- **Build-context exclusions**: `.containerignore` (existing from P1-001; verified adequate for the docs build context — see AC9)
- **Container-build verification logs** (off-tree, retained for audit): `%TEMP%/opencode/p1-002-verify/`, `%TEMP%/opencode/p1-002-review/build-review*.log` + `build-review-repro.log`, `%TEMP%/opencode/p1-002-phase2/build-phase2.log` + `build-phase2-repro.log`
- **Reference dev Containerfile** (pre-canonical, P1-001): `infra/containers/candelamoon-android/Containerfile` (and the P1-001 session handout at `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/session-handout.md` for the format and known-debt cross-references)
- **Memtrace repo_id**: `CandelaMoon` (indexed at base SHA `2118b61c…`; no re-index needed for the P1-002 change because it touches no application symbols, but a re-index should run before PR merge for graph consistency)
- **Memtrace episode IDs**: none (P1-002 is infra-only; no symbol-level episodes were recorded)
- **TDD red-phase checklist**: empty (bootstrap exception per handoff § Instructions)
- **Coverage audit**: empty (bootstrap exception; handoff `coverage_audit.rating: n/a`)
- **Orchestrator guide**: `.maestro-space/maestro-docs/maestro-orchestrator-guide.md`
- **Workflow**: `.maestro-space/maestro-docs/maestro-workflow.md`
- **Conventions**: `.maestro-space/maestro-docs/maestro-conventions.md`
- **Agent identity file**: `.maestro-space/maestro-agents/schubert-tech-writer.md` (this dispatch's contract)

## Known Debt

| ID | Item | Severity | Resolution |
|---|---|---|---|
| AC8 | Image digest is not bit-reproducible. Image **content** is reproducible (two `--no-cache` builds produce identical file counts and total bytes: `/opt/node 9446/231786503`, `/usr/local 2446/45964552`, `/home/builder 3/4553`, `/workspace 0/0`; pip freeze md5 `a6a8985a…`; file-list md5 `dca115fa…`; image size 771,003,453 bytes with 1-byte diff dismissed A-03), but image **digest** differs ~30 bytes in the last layer's gzip due to Podman layer-tar gzip non-determinism. | low (informational) | Resolution path: pin every downloaded artifact by SHA-256 in the Containerfile; pass `--rewrite-timestamp --source-date-epoch` (already doing this); switch to a deterministic compression backend (e.g. `zstd -19 --no-content-check`) when Podman supports it. Tracked as cross-task follow-up; out of scope for P1-002. |
| MVP-validator | Design validator is MVP. The script asserts that all required tools are installed and runnable (8 anchored exact-pinned checks); the actual validation logic (architecture schemas, ADR register, capability matrix, evidence manifest) is P1-017 follow-up. The MVP is a hard pre-condition for P1-017 because the real validator scripts will run inside this image and assume every tool the MVP checks is present. **[#24]** | low (P1-017) | P1-017 must (a) replace the MVP with the real scripts, (b) adopt the SEC-01 isolated-import rule (`python3 -I`, explicit `/workspace` paths, image-path imports — already documented in the validate-design header), and (c) receive its own threat model. |
| npm-audit-8 | 8 npm vulnerabilities (4 moderate, 4 high) in the locked transitive npm tree — `glob@11.0.3` and `whatwg-encoding@3.1.1` deprecations noted by `npm ci`. The tree is now LOCKED in `package-lock.json` so it cannot drift silently, but the vulnerable versions remain until a deliberate pin bump + lock regeneration. | medium (P1-022) | P1-022 must triage the npm audit output against the candelamoon-docs lockfile; bump transitive pins where a non-vulnerable alternative exists, regenerate the lockfile, re-run the full AC7 + AC8 verification suite. P1-001's locked tree (Bouncy Castle critical + 21 high Netty) and the other Group A images are also in P1-022's scope. |
| spec-network | `ci-architecture.md` § `candelamoon-docs` line 74 still lists only `PyPI, npm registry` under `Build-time network`. The Containerfile header and handoff AC5 now document the full 5-domain allowlist (`pypi.org`, `files.pythonhosted.org`, `registry.npmjs.org`, `nodejs.org`, `deb.debian.org`); the normative spec doc should be updated in the same PR as the next pin change. | low | Update line 74 to the 5-domain list. Bundle with the next Containerfile-touching PR (or this task's docs-only Schubert follow-up). |
| SEC-03 | Build-time network allowlist enforcement is image-documentary only. The 5-domain allowlist is documented in the Containerfile header and inline comments, but enforcement (default-deny build network namespace or approved HTTPS proxy permitting only the 5 domains) must live on the Linux build runner. **[#22]** | high (P1-005) | P1-005 publication job must enforce the allowlist; fail the build on `--network=host`; strongest mode prefetches all artifacts then builds with `podman build --network=none`. |
| SEC-04 | npm runtime JavaScript sandboxing is install-time-only. `npm ci --ignore-scripts` + lockfile integrity + root-owned `/opt/node` are the install-time controls. Every validation invocation must also run hardened (`--network=none --read-only --cap-drop=ALL --security-opt=no-new-privileges --user=1000:1000`, read-only /workspace bind, tmpfs /tmp, no sockets/secrets mounts). **[#21]** | high (P1-010) | P1-010 per-commit CI's docs-validate job must use the exact hardened podman run command. CI should also assert the lockfile is unchanged during `npm ci` and that no install script is enabled. |
| SEC-05 | Runtime `--network=none` is a caller convention. The merge-gate invocation becomes an exact centrally-owned podman run command (with `--network=none --read-only --cap-drop=ALL --security-opt=no-new-privileges --user=1000:1000`, read-only workspace bind, `--tmpfs /tmp`) plus a negative test proving the docs-validation job cannot reach an external endpoint. Networked link-checking, if ever needed, becomes a separately authorized job with an egress proxy. **[#23]** | high (P1-010) | P1-010 must include the exact podman run command and the negative test. Bundle the test with the docs-validate job so a regression is caught at the per-commit gate. |
| SEC-06 | apt package version drift is image-implicit. apt packages remain versioned implicitly by the base-image digest; full Debian snapshot/apt-proxy pinning with `package=version` installs and dpkg manifests is the shared P1-001/P1-002 build policy. **[#17]** | medium (P1-005) | P1-005 publication job must emit an SBOM with every APT package/version, compare with the approved toolchain baseline, and refresh the snapshot + base digest together. |
| SEC-07 | Default validator is tool-presence only. Accurate as a capability statement but not a container-security defect — P1-002 is explicitly the MVP tool-presence validator and real /workspace/docs validation is the documented P1-017 follow-up. | informational (dismissed) | P1-017 must adopt the SEC-01 isolated-import rule and explicit /workspace paths and receive its own threat model. |
| link-check-offline | markdown-link-check resolves HTTP(S) targets but the runtime contract says validation runs with `--network=none`. The current MVP only checks `--version`, so this incompatibility is not exercised. When the real validator lands, remote links must be handled: skip them in offline mode, validate in a separate networked job. **[#25]** | medium (P1-017) | P1-017 must separate local/offline link validation from a network-enabled job; configure the checker to skip remote links under `--network=none`; bound each request timeout explicitly. |
| STR-10 | Archive download and extraction resources are unbounded — a malicious but well-formed tar.xz could exhaust disk or memory during extraction. P1-002 has only the Node.js tarball (~80 MiB), so the practical exposure is smaller than P1-001's, but the same defensive helper applies. | low (per Brahms) | Add a guarded-download / check-zip helper with per-archive size / entry-count / expansion budgets and free-space checks before extract. Bundle with the P1-001 STR-10 patch round. |
| spec-status-note | `ci-architecture.md` § `candelamoon-docs` Containerfile path line (line 70) carries no status note, unlike § `candelamoon-android` line 61 (updated by P1-001's Schubert dispatch). | informational | Append a parenthetical status note pointing at the handoff; bundle with the spec-network fix. |
| deprecation-warning | jsonschema `__version__` DeprecationWarning on stderr when validate-design imports it. Harmless: the anchored pattern matches the version line; visible only as the first line in `--verbose` output. | informational | jsonschema 4.x will continue to emit this until 5.x. Re-evaluate on a jsonschema major-version bump. |

## GitHub Issues Created (from deferred findings)

Per orchestrator guide §8.2.1, every high/medium deferred finding creates a GitHub issue.

| Issue | Severity | Finding(s) | Target |
|---|---|---|---|
| [#21](https://github.com/magalz/CandelaMoon/issues/21) SecOps.P1.04 | HIGH | SEC-04 — npm runtime JS sandboxing | P1-010 |
| [#22](https://github.com/magalz/CandelaMoon/issues/22) SecOps.P1.03 | HIGH | SEC-03 — build-time network egress enforcement | P1-005 |
| [#23](https://github.com/magalz/CandelaMoon/issues/23) SecOps.P1.05 | HIGH | SEC-05 — runtime network isolation enforcement | P1-010 |
| [#24](https://github.com/magalz/CandelaMoon/issues/24) Deferred.P1.04 | MEDIUM | defer-3 — real design validation logic | P1-017 |
| [#25](https://github.com/magalz/CandelaMoon/issues/25) Deferred.P1.03 | MEDIUM | defer-2 — markdown-link-check offline mode | P1-017 |

Pre-existing issues carrying P1-002 findings:
| [#14](https://github.com/magalz/CandelaMoon/issues/14) SecOps.P1.01 | HIGH | P1-001 STR-01/03/04/05 — supply chain provenance | P1-005 |
| [#17](https://github.com/magalz/CandelaMoon/issues/17) Deferred.P1.02 | MEDIUM | P1-001 defer-2 / STR-02 / P1-002 SEC-06 — APT snapshotting | P1-005 |

## UAT Decision

- **Status**: **passed**
- **User decision**: `candelamoon-docs` Containerfile green-verified on `candelamoon-docs:phase2` (id `127a1439acb4…`, 771,003,453 bytes, 23/23 build steps); Vivaldi's initial build, Bach's Review Phase 1 patch round (11 applied + 3 deferred + 8 dismissed), and Bach's Review Phase 2 security patch round (SEC-01 + SEC-02 applied + 4 deferred-to-CI + 1 dismissed) all pass. Full AC7 validation suite green under `--network=none` (Python 3.11.15, Node v22.23.2, npm 10.9.8, markdownlint 0.45.0, yamllint 1.37.1, markdown-link-check 3.13.7, uid=1000 builder, default `validate-design` exits 0 with 8/8 OK). SEC-01 red→green proof captured: pre-fix image false-greens with a `/workspace/jsonschema.py` containing attacker code, fixed image exits 0 with real modules. Two-build reproducibility verified (identical pip freeze md5 `a6a8985a…`, identical file-list md5 `dca115fa…`, identical image size 771,003,453 bytes). The task is ready for human merge approval.
- **Rationale**: All ten acceptance criteria are met (AC8 is a partial pass with the content-reproducibility half verified and the digest-reproducibility half tracked as cross-task known debt per P1-001). The deferred items (3 phase-1 + 4 phase-2) are ownership-bound to later tasks (P1-005 / P1-010 / P1-017 / P1-022) and are not part of P1-002's UAT surface. The dismissed items (8 phase-1 + 1 phase-2) are explicitly out of scope per their respective dispositions. The 7 known-debt items are tracked in this handout and in the handoff `known_debt` list with severity, resolution path, and owning task.

## PR Status

- **PR URL**: TBD
- **Status**: TBD
- **Author**: TBD (`magalz` or `open-pr-bot`)
- **Title**: `[P1-002] candelamoon-docs Containerfile` (recommended)
- **Base branch**: `moonlight-noir`
- **Head branch**: `phase1/p1-002-candelamoon-docs-containerfile`
- **Head SHA**: `47e1a9f55b6b19772bcc21439097af46de9b68be` (at time of writing; this Schubert dispatch will add a docs commit on top)
- **Merge commit**: n/a
- **Merged at**: n/a
- **Workflow run that opened it**: n/a (TBD)
- **Memtrace GitHub review**: pending (PR not yet opened)
- **Coverage audit commit**: n/a (bootstrap exception)

## Rollback Strategy

1. **If the PR is not yet merged**: close PR and delete branch
2. **If the PR is merged**: revert the merge commit, force-reindex Memtrace, re-run base suite
3. **Files affected** (7 tracked files in this task, all infra/docs):
   - `infra/containers/candelamoon-docs/Containerfile` (the entire Containerfile is the change; 23 steps after SEC-01/SEC-02)
   - `infra/containers/candelamoon-docs/requirements.txt` (3 direct pip pins)
   - `infra/containers/candelamoon-docs/requirements.lock` (9 hash-locked pip packages)
   - `infra/containers/candelamoon-docs/package.json` (2 direct npm pins)
   - `infra/containers/candelamoon-docs/package-lock.json` (165 locked npm packages)
   - `infra/containers/candelamoon-docs/validate-design` (8 tool-presence checks; SEC-01 isolated imports)
   - `docs/infrastructure/toolchain-pins.md` (3 sections updated: `Container Base Images`, `Node`, `Python`)
4. **Documentation rollback**: revert `docs/infrastructure/ci-architecture.md` § `candelamoon-docs` Containerfile path line if the status note was appended; revert `.maestro-space/maestro-plans/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile.md` Status to Pending and clear the Session History row; revert `.maestro-space/maestro-plans/phase-1-delivery-system/phase-plan.md` P1-002 row to Pending and restore the task-count header
5. **Framework-state rollback**: the `.maestro-space/maestro-works/.../p1-002-.../` folder is gitignored; on full rollback, delete the folder to remove all session artifacts (handoff, findings, activity reports, session handout, Schubert dispatch)
6. **Handoff file modification note**: the handoff has been modified across 4 commits (initial handoff + Vivaldi activity report + phase-1 Bach activity report + phase-2 Bach activity report) plus this Schubert dispatch's documentation-update commit; `git log --oneline -- .maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/handoff.md` will show the full history. Code-impacting commits in the PR are `425c17f5` (initial Vivaldi build), `ff6c64d0` (Review Phase 1 patch round: lock files + validate-design hardening), and `91bd8403` (Review Phase 2 patch round: SEC-01 + SEC-02); the handoff-docs commits are `864b89db`, `4ead0667`, `e37c8c18`, `0c807769`, and `47e1a9f5`
7. **No code or test files are affected** — the Containerfile is not yet referenced by any CI workflow (P1-010 is the first consumer); reverting the PR does not break any tracked build path
