# Phase 0: Delivery-System Design Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce the complete DevOps/DevSecOps delivery-system design, ADR set, machine-readable schemas, and a validation script so that Phase 1 can implement the pipeline against an evidence-backed specification.

**Architecture:** All deliverables are documentation, JSON Schemas, and one Python validator script. No product code changes. The design defines Podman-first container execution, GitHub Actions CI, GitHub/Memtrace split-authority synchronization, branch/PR/TDD workflow, device lab, threat model, supply chain, secrets, signing, and operational policies.

**Tech Stack:** Markdown (design docs), JSON Schema draft 2020-12 (machine-readable schemas), Python 3.11+ (validator script), GitHub (repository hosting, rulesets, Actions).

**Spec:** `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md`, sections 7, 8, 9, and 11 Phase 0.

## Global Constraints

- `minSdk` remains API 28 so Android TV 9-11 devices can install the app.
- API 31 and newer form the primary product tier.
- GitHub pull requests and commits are authoritative for accepted source state.
- Memtrace is authoritative for derived architecture evidence, symbol history, change impact, decision provenance, and process provenance.
- All product development halts whenever local Git, GitHub, and Memtrace do not describe the same intended branch state.
- Rootless Podman by default. Commands are documented for Podman. Docker compatibility is not required.
- Every leaf roadmap task uses a new branch pushed to GitHub.
- Every PR passes: automated checks, Memtrace review, acceptance audit, edge-case hunt, blind hunt, security review, and final policy check.
- Critical and high-severity findings cannot be waived by the author.
- `app/build.gradle` currently uses `minSdk 21`, `targetSdk 34`, `compileSdk 36`, Gradle/AGP `8.13.0`.
- Current CI is AppVeyor (`appveyor.yml`); this design transitions to GitHub Actions + Podman.
- CandelaMoon origin: `https://github.com/magalz/CandelaMoon.git`
- LuminalShine mirror origin: `https://github.com/magalz/luminalshine-mirror.git`
- LuminalShine upstream: `https://github.com/NortheBridge/luminalshine.git` (fetch only, push disabled)

---

## File Structure

```
docs/
  superpowers/
    plans/
      2026-08-05-phase0-delivery-system-design.md  (this plan)
  adr/
    0000-template.md
    0001-luminalshine-only-compatibility.md
    0002-classic-transport-only.md
    ... (20 ADRs total)
  infrastructure/
    delivery-system-design.md
    ci-architecture.md
    device-lab-architecture.md
    toolchain-pins.md
    threat-model.md
    supply-chain-policy.md
    secrets-and-signing-policy.md
    incident-and-rollback-policy.md
    retention-cache-cost-maintenance-policy.md
    implementation-backlog.md
    phase0-audit.md
  schemas/
    evidence-manifest.schema.json
    capability-row.schema.json
    adr.schema.json
    device-matrix-row.schema.json
scripts/
  validate_design.py
  requirements.txt
```

---

## Task Workflow (14-Step Pipeline)

Every task in this plan flows through this pipeline per spec section 15.2:

1. Orchestrator creates task handoff (this plan provides the acceptance criteria)
2. QA Architect creates TDD red-phase test scaffolds (for tasks with testable behavior)
3. Senior Developer (or DevOps/Security agent for infra tasks) implements solution
4. Review Phase 1 (parallel): Blind Hunter, Edge Case Hunter, Acceptance Analyst
5. Orchestrator triages Phase 1 findings into handoff
6. Developer implements Phase 1 fixes
7. Review Phase 2 (sequential): Red Team Analyst then Blue Team Analyst
8. Orchestrator triages Phase 2 findings into handoff
9. Developer implements security fixes
10. QA Architect runs coverage audit with Memtrace reconciliation
11. UAT (user) when applicable
12. Tech Writer documents everything
13. Orchestrator opens PR using Memtrace code-review
14. Tech Writer creates session handout

**Bootstrap exception (spec section 12):** For Phase 0 documentation tasks, the TDD red phase (step 2) and coverage audit (step 10) apply only to the validator script (Task 2). Pure documentation tasks skip steps 2 and 10 but still require Review Phases 1-2, Tech Writer documentation, and PR creation.

---

## Task 1: Machine-Readable Schemas

**Files:**
- Create: `docs/schemas/evidence-manifest.schema.json`
- Create: `docs/schemas/capability-row.schema.json`
- Create: `docs/schemas/adr.schema.json`
- Create: `docs/schemas/device-matrix-row.schema.json`

**Interfaces:**
- Produces: four JSON Schema files that `validate_design.py` (Task 2) loads to validate design artifacts.

- [ ] **Step 1: Create the ADR schema**

Create `docs/schemas/adr.schema.json` with JSON Schema draft 2020-12 requiring fields: id (4-digit pattern), title, status (enum: proposed/accepted/superseded/deprecated), date, context, decision, consequences, alternatives (array with name and rejection_reason), and optional: supersedes, superseded_by, spec_section, evidence array.

- [ ] **Step 2: Create the evidence-manifest schema**

Create `docs/schemas/evidence-manifest.schema.json` requiring fields: change_id, phase (pattern `^Phase \d+$`), task, repository, branch, base_sha, head_sha, memtrace_repo_id, memtrace_indexed_sha, memtrace_episode_ids, capability_rows, adrs, verification (object with boolean fields: tests_pass, memtrace_review, acceptance_audit, edge_case_hunt, blind_hunt, security_review, policy_check), and optional: peer_pr, known_debt, rollback_strategy. Additionally include handoff fields from spec section 15.3: tdd_artifacts (object with atdd_checklist path, test_files array, red_phase_verified boolean), implementation_artifacts (object with files_created array, files_modified array, green_phase_verified boolean), review_phase_1 (object with blind_hunter_findings, edge_case_hunter_findings, acceptance_analyst_findings, triaged_findings, fixes_applied boolean), review_phase_2 (object with red_team_findings, blue_team_findings, triaged_findings, fixes_applied boolean), coverage_audit (object with rating enum, risk_weighted_score integer, memtrace_reconciliation string, coverage_gaps array), uat (object with status enum, user_decision string), documentation (object with tech_writer_artifacts array, session_handout string).

- [ ] **Step 3: Create the capability-row schema**

Create `docs/schemas/capability-row.schema.json` requiring fields: capability_id, domain (enum of 12 domains from spec section 4.3), user_value, upstream_release, upstream_commit, host_contract, client_implementation, state_owner (enum: client/host/shared), disposition (enum of 7 from spec section 4.4), mvp_status, min_api (integer >= 28), fallback, error_states, confidence, evidence_status, and optional: disposition_rationale, platform_tier, security_privacy_notes, test_evidence, related_adr, related_task, related_branch, related_pr, memtrace_records.

- [ ] **Step 4: Create the device-matrix-row schema**

Create `docs/schemas/device-matrix-row.schema.json` requiring: device_name, os_api_level (integer >= 28), soc, decoder_codecs (array), hdr_support (enum), frame_rate_behavior, controller_rumble_support (enum), network_path (enum), platform_tier (enum), test_date, test_result (enum: pass/fail/pending), optional: notes.

- [ ] **Step 5: Verify schemas are valid JSON**

Run: `python -c "import json, glob; [json.load(open(f)) for f in glob.glob('docs/schemas/*.json')]; print('All schemas valid JSON')"`
Expected: `All schemas valid JSON`

- [ ] **Step 6: Commit**

```bash
git add docs/schemas/
git commit -m "docs(schemas): add JSON Schemas for ADR, evidence manifest, capability row, and device matrix

Task 1 of Phase 0 delivery-system design.
Spec: docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md sections 4.4, 7.1, 10.3"
```

---

## Task 2: Design Validator Script

**Files:**
- Create: `scripts/validate_design.py`
- Create: `scripts/requirements.txt`

**Interfaces:**
- Consumes: all `docs/schemas/*.schema.json` (Task 1), all `docs/adr/*.md` (Task 3+), all `docs/infrastructure/*.md` (Tasks 4-8)
- Produces: exit code 0 (pass) or 1 (fail) with a report listing every check and result

- [ ] **Step 1: Write requirements file**

Create `scripts/requirements.txt`:
```
jsonschema>=4.20
pyyaml>=6.0
```

- [ ] **Step 2: Write the validator script**

Create `scripts/validate_design.py` (Python 3.11+) that:
1. Loads and validates all 4 JSON Schema files as valid JSON Schema
2. Extracts YAML frontmatter from each ADR markdown file and validates against `adr.schema.json`
3. Checks ADR IDs are sequential 0001..N
4. Checks ADR template exists (`0000-template.md`)
5. Checks all 10 infrastructure docs exist with non-trivial content
6. Checks each infrastructure doc has required sections (defined as a dict of filename -> list of required heading strings)
7. Prints a PASS/FAIL report with details for each check
8. Exit 0 if all pass, exit 1 if any fail
9. Supports `--strict` flag (treats warnings as failures)

Required infrastructure sections:
- `delivery-system-design.md`: `# Delivery System Design`, `## Repository`, `## Branch`, `## CI`, `## Synchronization`, `## TDD`, `## Review`
- `ci-architecture.md`: `# CI Architecture`, `## Podman`, `## Images`, `## Jobs`, `## Pipeline Tiers`
- `device-lab-architecture.md`: `# Device Lab`, `## Google TV Streamer`, `## Compatibility`, `## Fault Injection`
- `toolchain-pins.md`: `# Toolchain Pins`, `## JDK`, `## Android SDK`, `## NDK`, `## Gradle`, `## Podman`
- `threat-model.md`: `# Threat Model`, `## Trust Boundaries`, `## CI`, `## Secrets`, `## Signing`, `## Dependencies`, `## Containers`
- `supply-chain-policy.md`: `# Supply Chain Policy`, `## Actions`, `## Base Images`, `## Dependencies`, `## SBOM`, `## Provenance`, `## Vulnerability`
- `secrets-and-signing-policy.md`: `# Secrets And Signing Policy`, `## Secret Stores`, `## Signing`, `## Release`
- `incident-and-rollback-policy.md`: `# Incident And Rollback Policy`, `## Bad Release`, `## Compromised`, `## Stale Graph`
- `retention-cache-cost-maintenance-policy.md`: `# Retention Cache Cost Maintenance Policy`, `## Artifacts`, `## Cache`, `## Cost`, `## Maintenance`
- `implementation-backlog.md`: `# Phase 1 Implementation Backlog`, `## Work Items`

- [ ] **Step 3: Install deps and run validator**

```bash
pip install -r scripts/requirements.txt
python scripts/validate_design.py --strict
```
Expected: Schema checks PASS. ADR/infra checks FAIL (don't exist yet). This proves the validator works.

- [ ] **Step 4: Commit**

```bash
git add scripts/validate_design.py scripts/requirements.txt
git commit -m "docs(scripts): add design validator for ADR, schema, and infra-doc validation

Task 2 of Phase 0 delivery-system design.
Spec: docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md section 8.5"
```

---

## Task 3: ADR Template And Initial ADR Set

**Files:**
- Create: `docs/adr/0000-template.md`
- Create: `docs/adr/0001` through `docs/adr/0020` (20 ADR files)

**Interfaces:**
- Consumes: `docs/schemas/adr.schema.json` (Task 1)
- Produces: 20 ADR files with YAML frontmatter conforming to the ADR schema

- [ ] **Step 1: Create ADR template `0000-template.md`**

A markdown file with YAML frontmatter containing all required ADR schema fields with placeholder values, followed by a body template expanding context, decision, consequences, and alternatives.

- [ ] **Step 2: Write ADRs 0001-0020**

Each ADR has YAML frontmatter (conforming to `adr.schema.json`) plus a markdown body expanding each section. Key decisions:

- **0001**: LuminalShine-only host compatibility. No Apollo/Artemis/generic-Sunshine support.
- **0002**: Classic Moonlight transport only. WebRTC excluded; reopening requires new product design + superseding ADR.
- **0003**: Frozen Artemis baseline. No upstream merges. CandelaMoon owns all upkeep.
- **0004**: `luminalshine-mirror` as integration lab. Never an MVP dependency. Push to upstream disabled.
- **0005**: New application identity. No Artemis migration.
- **0006**: TV-only scope. Mobile classified then removed in controlled phases. Not conflated with decoder removal.
- **0007**: minSdk 28, API 31+ primary, API 28-30 compatibility. One adaptive UI. Capability-gated enhancements.
- **0008**: Single adaptive UI. No parallel legacy tree. Reduced effects is a config, not a codebase.
- **0009**: Compose for TV evaluated via bounded prototype in Phase 5. Protected boundaries remain until evidence.
- **0010**: Host owns session/library/capability semantics. Client owns TV nav, profiles, presentation, diagnostics, client-side input when not inventing host state.
- **0011**: MVP prohibits mirror-only host capabilities. Official LuminalShine releases only.
- **0012**: Every feature gets a disposition. No deletion without Memtrace impact, evidence, tests, rollback, doc updates.
- **0013**: GitHub authoritative for source. Memtrace authoritative for derived evidence. Conflict = stop, sync, regenerate, update via PR.
- **0014**: Podman-first. Rootless, non-root, pinned by digest. Audited host-bound exceptions for devices/Windows/signing.
- **0015**: Multi-agent architecture with production agents (Senior Developer, QA Architect, DevOps Architect, Security Analyst, GRC Architect, Tech Writer, UX/UI Designer) and review agents (Blind Hunter, Edge Case Hunter, Acceptance Analyst, Red Team, Blue Team). Handoff protocol connects agents.
- **0016**: ATDD red-phase-before-implementation. QA Architect creates failing test scaffolds before any implementation. No scaffold passes before code exists.
- **0017**: Two-phase adversarial review. Phase 1: Blind Hunter, Edge Case Hunter, Acceptance Analyst (parallel, no handoff). Phase 2: Red Team then Blue Team (sequential security review).
- **0018**: Red/blue team security review. Red Team finds exploitable weaknesses with STRIDE/OWASP. Blue Team designs concrete mitigations and assesses exploitability.
- **0019**: Coverage audit with Memtrace reconciliation as exit gate. QA Architect uses detect_changes, get_evolution, get_episode_replay to verify what changed vs what was documented. No task exits without coverage rating.
- **0020**: Session handout for context continuity. Tech Writer creates self-contained handout at end of every task/phase to prevent context rot across sessions.

- [ ] **Step 2b: Write ADRs 0015-0020 (Agent Architecture)**

Each ADR follows the same template. Key decisions:

- **0015**: Multi-agent architecture and handoff protocol. Production agents (Senior Developer, QA Architect, DevOps Architect, Security Analyst, GRC Architect, Tech Writer, UX/UI Designer) receive and update the handoff. Review agents (Blind Hunter, Edge Case Hunter, Acceptance Analyst, Red Team, Blue Team) receive only need-to-know info and never update the handoff. Orchestrator acts as Product Owner.
- **0016**: ATDD red-phase-before-implementation. QA Architect creates failing/ignored test scaffolds before any implementation. Developer activates one test at a time (red to green). Red phase is mandatory for features and bug fixes.
- **0017**: Two-phase adversarial review. Phase 1: Blind Hunter, Edge Case Hunter, Acceptance Analyst run in parallel without handoff or author rationale. Phase 2: Red Team then Blue Team run sequentially for security.
- **0018**: Red/blue team security review approach. Red Team finds exploitable weaknesses with concrete attack scenarios using STRIDE and OWASP. Blue Team receives red team findings and designs concrete, implementable mitigations. Blue Team confirms or rejects findings and checks for new risks.
- **0019**: Coverage audit with Memtrace reconciliation as exit gate. QA Architect builds static mapping of test scenarios to tests to ACs. Memtrace detect_changes/get_evolution/get_episode_replay verify what actually changed. Rating: pass/conditional/fail. Fail returns to developer.
- **0020**: Session handout for context continuity. Tech Writer creates self-contained handout at end of every task/phase with branch, commit, PR, artifacts, pending work, keys for next session, known debt, rollback strategy. Prevents context rot across sessions.

Each ADR frontmatter includes: id, title, status (accepted), date (2026-08-05), spec_section, context, decision, consequences, alternatives (at least 2 with rejection reasons), evidence.

- [ ] **Step 3: Run validator**

```bash
python scripts/validate_design.py --strict 2>&1 | grep -E "ADR|adr"
```
Expected: ADR template, validation, and sequencing checks PASS. Infra doc checks still FAIL.

- [ ] **Step 4: Commit**

```bash
git add docs/adr/
git commit -m "docs(adr): add ADR template and initial 20-decision register

Task 3 of Phase 0 delivery-system design.
ADRs 0001-0020: LuminalShine-only, classic transport, Artemis freeze,
integration lab, new app identity, TV-only, platform tiers, adaptive UI,
Compose evaluation, state ownership, MVP host constraint, disposition
policy, split authority, Podman-first.
ADRs 0015-0020: Multi-agent architecture, ATDD red-phase, two-phase
adversarial review, red/blue team security, coverage audit with Memtrace,
session handout for context continuity.
Spec: section 5.4"
```

---

## Task 4: Toolchain Pins And Development Environment

**Files:**
- Create: `docs/infrastructure/toolchain-pins.md`

- [ ] **Step 1: Write the toolchain pins document**

Create `docs/infrastructure/toolchain-pins.md` with sections: `# Toolchain Pins`, `## JDK` (17, eclipse-temurin:17-jdk), `## Android SDK` (compileSdk 36, targetSdk 34, minSdk 28, cmdline-tools, platform-tools), `## NDK` (27.0.12077973), `## Gradle` (AGP 8.13.0, wrapper version from gradle-wrapper.properties), `## CMake and Ninja`, `## Clang` (NDK shipped), `## Node` (LTS for docs/security containers), `## Podman` (pinned version, WSL2 backend on Windows), `## Python` (3.11+), `## GitHub Actions` (pinned by SHA, list each), `## Container Base Images` (digests for 4 image roles). Each pin: name, version, source URL, digest/SHA, rationale.

- [ ] **Step 2: Verify**

```bash
python scripts/validate_design.py --strict 2>&1 | grep "toolchain"
```
Expected: PASS (required sections present).

- [ ] **Step 3: Commit**

```bash
git add docs/infrastructure/toolchain-pins.md
git commit -m "docs(infra): add toolchain pins for JDK, SDK, NDK, Gradle, Podman, containers

Task 4 of Phase 0. Spec: section 9.1"
```

---

## Task 5: Podman-First CI Architecture

**Files:**
- Create: `docs/infrastructure/ci-architecture.md`

- [ ] **Step 1: Write the CI architecture document**

Create `docs/infrastructure/ci-architecture.md` with sections:
- `# CI Architecture`
- `## Podman`: rootless, non-root, pinned by digest, same image local+CI, cache key composition
- `## Images`: 4 image roles (candelamoon-android, candelamoon-docs, candelamoon-security, luminal-contract) each with: Containerfile location, base image, installed tools, non-root user, mount policy, network policy
- `## Jobs`: enumerate each CI job (lint-format, unit-tests, docs-validate, security-scan, sbom-delta, memtrace-sync, device-test, compat-test, windows-host-test, release-sign) with: name, image, triggers, inputs, outputs, validates
- `## Pipeline Tiers`: per-commit, per-PR, nightly, release-candidate — each with jobs, triggers, timeout, cache, artifacts

Enough detail that Phase 1 can write Containerfiles and workflow YAML without consulting the spec.

- [ ] **Step 2: Verify**

```bash
python scripts/validate_design.py --strict 2>&1 | grep "ci-architecture"
```

- [ ] **Step 3: Commit**

```bash
git add docs/infrastructure/ci-architecture.md
git commit -m "docs(infra): add Podman-first CI architecture with images, jobs, pipeline tiers

Task 5 of Phase 0. Spec: sections 9.2-9.5"
```

---

## Task 6: Device Lab And Runner Architecture

**Files:**
- Create: `docs/infrastructure/device-lab-architecture.md`

- [ ] **Step 1: Write the device lab document**

Sections: `# Device Lab`, `## Google TV Streamer` (primary reference, ADB connection, CI trigger, artifact capture), `## Compatibility` (API 28-30 emulators + representative hardware, boot/snapshot strategy, core journey tests only), `## Fault Injection` (13 fault types: host offline/reboot, network loss, cert mismatch, invalid PIN, pairing conflict, busy session, unsupported codec/HDR, decoder failure, no artwork, malformed response, low-memory recreation — each with trigger method, expected behavior, recovery verification), `## Self-Hosted Runners` (runner labels, OS, ephemeral, security posture, Podman invocation), `## Windows Host` (Windows runner for LuminalShine integration: OS, install, network path, streaming validation).

- [ ] **Step 2: Verify + Commit**

```bash
python scripts/validate_design.py --strict 2>&1 | grep "device-lab"
git add docs/infrastructure/device-lab-architecture.md
git commit -m "docs(infra): add device lab architecture for TV Streamer, compat, Windows host

Task 6 of Phase 0. Spec: section 10.3"
```

---

## Task 7: Security Design

**Files:**
- Create: `docs/infrastructure/threat-model.md`
- Create: `docs/infrastructure/supply-chain-policy.md`
- Create: `docs/infrastructure/secrets-and-signing-policy.md`
- Create: `docs/infrastructure/incident-and-rollback-policy.md`

- [ ] **Step 1: Write threat model**

Sections: `# Threat Model`, `## Trust Boundaries` (dev machine, Podman container, CI runner, GitHub Actions, device lab, Windows runner, Memtrace daemon, signing env, release artifacts), `## CI`, `## Secrets`, `## Signing`, `## Dependencies`, `## Release Artifacts`, `## Containers`, `## Memtrace Data`. Each: context paragraph, threat/control table, residual risk.

- [ ] **Step 2: Write supply-chain policy**

Sections: `# Supply Chain Policy`, `## Actions` (pin by SHA), `## Base Images` (pin by digest), `## Dependencies` (no SNAPSHOT, dedicated PR), `## SBOM` (CycloneDX, per build, diff between releases), `## Provenance` (SLSA L3 target), `## Vulnerability` (critical blocks release, SLA: 24h/72h/1week).

- [ ] **Step 3: Write secrets and signing policy**

Sections: `# Secrets And Signing Policy`, `## Secret Stores` (GitHub Secrets/Environments, no secrets in code/images/logs, OIDC where possible), `## Signing` (offline/restricted env, shortest exposure, rotation), `## Release` (signed APK/AAB, checksums, provenance attestation).

- [ ] **Step 4: Write incident and rollback policy**

Sections: `# Incident And Rollback Policy`, `## Bad Release` (halt, pull, advisory, fix, 1h/24h targets), `## Compromised` (dependency + base image procedures), `## Stale Graph` (halt, diagnose, repair, verify canary, resume; no waiver if Memtrace unavailable).

- [ ] **Step 5: Verify + Commit**

```bash
python scripts/validate_design.py --strict 2>&1 | grep -E "threat|supply|secrets|incident"
git add docs/infrastructure/threat-model.md docs/infrastructure/supply-chain-policy.md docs/infrastructure/secrets-and-signing-policy.md docs/infrastructure/incident-and-rollback-policy.md
git commit -m "docs(infra): add threat model, supply chain, secrets/signing, incident/rollback policies

Task 7 of Phase 0. Spec: sections 9.1, 9.2, 9.3"
```

---

## Task 8: Operational Policies, Master Design, And Backlog

**Files:**
- Create: `docs/infrastructure/retention-cache-cost-maintenance-policy.md`
- Create: `docs/infrastructure/delivery-system-design.md`
- Create: `docs/infrastructure/implementation-backlog.md`

- [ ] **Step 1: Write retention/cache/cost/maintenance policy**

Sections: `# Retention Cache Cost Maintenance Policy`, `## Artifacts` (CI 30d, releases indefinite, SBOMs indefinite, logs 30d), `## Cache` (key composition, eviction, poisoning prevention), `## Cost` (estimated monthly, optimization, budget cap), `## Maintenance` (annual target SDK, monthly deps, quarterly images, per-merge reindex, monthly security rules).

- [ ] **Step 2: Write delivery system design master document**

Sections: `# Delivery System Design`, `## Repository` (owner, visibility, branch protection, default branch plan), `## Branch` (naming convention, draft PR, phase-audit PR, cross-repo paired PRs), `## CI` (reference ci-architecture.md, summary of tiers), `## Synchronization` (GitHub/Memtrace split, state tuple, 5 gates, stop-work, repair mode, ADR 0013), `## TDD` (red-green-refactor, characterization, reachability, doc exemption), `## Review` (7-gate stack, severity, waiver governance, independence), `## Toolchain` (reference toolchain-pins.md), `## Device Lab` (reference device-lab-architecture.md), `## Supply Chain` (reference supply-chain-policy.md), `## Secrets and Signing` (reference secrets-and-signing-policy.md), `## Operational` (reference retention-cache-cost-maintenance-policy.md), `## Incident` (reference incident-and-rollback-policy.md). This is an integration layer that summarizes and links, not duplicates.

- [ ] **Step 3: Write implementation backlog**

`# Phase 1 Implementation Backlog`, `## Work Items` — 20 ordered items (P1-001 through P1-020):
1. candelamoon-android Containerfile
2. candelamoon-docs Containerfile
3. candelamoon-security Containerfile
4. luminal-contract Containerfile
5. Build and publish images to GHCR with signatures
6. GitHub branch protection rulesets
7. PR template with task/phase/capability/evidence fields
8. Issue/milestone templates
9. Evidence-manifest YAML template
10. Per-commit CI workflow
11. Per-PR CI workflow
12. Nightly CI workflow
13. Release-candidate CI workflow
14. Self-hosted runner for Google TV Streamer
15. Self-hosted Windows runner for LuminalShine
16. Memtrace sync check in CI
17. Design validator in candelamoon-docs image and CI
18. Canary PR proving all paths
19. Remove AppVeyor (appveyor.yml)
20. Phase 1 audit PR

Each item: ID, title, description, dependencies, complexity (S/M/L), related ADR.

- [ ] **Step 4: Run full validator**

```bash
python scripts/validate_design.py --strict
```
Expected: `RESULT: ALL CHECKS PASSED`, exit code 0.

- [ ] **Step 5: Commit**

```bash
git add docs/infrastructure/retention-cache-cost-maintenance-policy.md docs/infrastructure/delivery-system-design.md docs/infrastructure/implementation-backlog.md
git commit -m "docs(infra): add delivery system master design, ops policies, Phase 1 backlog

Task 8 of Phase 0. Completes all infrastructure design documents.
Spec: sections 7-9, 11 Phase 0"
```

---

## Task 9: Phase 0 Audit And Review

**Files:**
- Create: `docs/infrastructure/phase0-audit.md`

- [ ] **Step 1: Run full validator in strict mode**

```bash
python scripts/validate_design.py --strict
```
Expected: `RESULT: ALL CHECKS PASSED`, exit code 0.

If any check fails, fix the underlying document and re-run.

- [ ] **Step 2: Self-review — spec coverage**

Confirm every Phase 0 deliverable in spec section 9.1 maps to a design artifact. Record the coverage table in the audit doc. Fix any gaps.

- [ ] **Step 3: Acceptance audit**

Confirm: 20 ADRs conform to schema, 4 JSON Schemas valid, validator runs clean, 10 infra docs have required sections, backlog has 20 items, toolchain pins specify exact versions.

- [ ] **Step 4: Edge-case hunt**

Review design for: unavailable pinned versions, Podman unavailable, Google TV Streamer offline during CI, Memtrace indexing failure, fork PR secret exposure, malformed ADR frontmatter. Document findings and fixes.

- [ ] **Step 5: Blind hunt**

Dispatch an independent reviewer agent with fresh context. Provide spec, design docs, and validator output. Reviewer finds inconsistencies, missing requirements, security gaps, impractical controls. Fix findings.

- [ ] **Step 6: Security review**

Confirm: trust boundaries documented, secret stores isolated, containers non-root minimal caps, actions pinned by SHA, fork-PR secret exposure documented, release artifacts signed with provenance.

- [ ] **Step 7: Write phase-audit doc and commit**

Create `docs/infrastructure/phase0-audit.md` with: validator result, spec coverage table, acceptance audit results, edge-case findings/fixes, blind hunt findings/fixes, security review results, known debt, phase sign-off.

```bash
git add docs/infrastructure/phase0-audit.md
git commit -m "docs(infra): Phase 0 audit — all reviews passed, exit gate met

Task 9 of Phase 0. Validator PASS. Spec coverage complete.
Acceptance PASS. Edge-case PASS. Blind hunt PASS. Security PASS.
Phase 0 exit gate met; Phase 1 may begin."
```

- [ ] **Step 8: Push branch and create phase-audit PR**

```bash
git push -u origin docs/phase0-delivery-system-design
```

Create a draft PR titled `docs: Phase 0 — Delivery-System Design (phase audit)` linking all task commits, the spec, and the audit document.

---

## Self-Review

**1. Spec coverage:** Every Phase 0 deliverable in spec section 9.1 maps to a task:
- Repository/branch/PR traceability -> Task 8 (delivery-system-design.md)
- GitHub rulesets/checks/merge -> Task 8
- CI architecture -> Task 5
- Sync protocol + evidence manifest schema -> Task 1 (schemas) + Task 8 (sync section)
- TDD + review execution -> Task 8
- Toolchain pins -> Task 4
- Device lab -> Task 6
- Threat model -> Task 7
- Supply chain -> Task 7
- Secrets/signing/incident/retention/cache/cost/maintenance -> Tasks 7 + 8
- Infrastructure ADRs -> Task 3
- Implementation backlog -> Task 8
- Exit gate (acceptance, edge, blind, security reviews) -> Task 9

**2. Placeholder scan:** TBD/TODO/fill-in checked and confirmed resolved. All 14 CDRs have concrete decisions with spec references per Step 2 of Task 3. Schemas have concrete fields with defined types and enums. Implementation backlog has 20 concrete items with IDs.

**3. Type consistency:** ADR schema id field uses ^\d{4}$ pattern; all ADR files follow 0001-0020 format. Evidence manifest base_sha/head_sha use ^[0-9a-f]{7,40}$. Capability-row domain enum has 12 entries matching spec section 4.3. Device-matrix platform_tier enum matches ADR 0007 tiers.
