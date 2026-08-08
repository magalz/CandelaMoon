# Phase 0 — Delivery-System Design — COMPLETE

**Goal**: Establish the framework that allows evidence-backed delivery to proceed.
**Exit gate**: Spec, plan, design validator, agent architecture, and dual evidence
manifest schemas are committed and pass validation.
**Related ADRs**: 0001-0020
**Dependencies on previous phase**: None (this is the first phase).
**Estimated task count**: 9 tasks

---

## Phase Tasks

| # | ID | Title | Status | Depends On | Complexity | Task File |
|---|---|---|---|---|---|---|
| 1 | P0-001 | Machine-readable schemas (ADR, evidence manifest, capability row, device matrix) | Completed | — | M | `p0-001-machine-readable-schemas.md` |
| 2 | P0-002 | Design validator script | Completed | P0-001 | M | `p0-002-design-validator.md` |
| 3 | P0-003 | ADR template and initial 20-decision register | Completed | P0-001 | L | `p0-003-adr-template-and-register.md` |
| 4 | P0-004 | Toolchain pins and development environment | Completed | — | S | `p0-004-toolchain-pins.md` |
| 5 | P0-005 | Podman-first CI architecture | Completed | — | M | `p0-005-ci-architecture.md` |
| 6 | P0-006 | Device lab and runner architecture | Completed | — | M | `p0-006-device-lab-architecture.md` |
| 7 | P0-007 | Security design (threat model, supply chain, secrets/signing, incident/rollback) | Completed | — | L | `p0-007-security-design.md` |
| 8 | P0-008 | Operational policies, master design, and Phase 1 backlog | Completed | P0-005 | M | `p0-008-operational-policies.md` |
| 9 | P0-009 | Phase 0 audit and review (acceptance, edge-case, blind, security) | Completed | P0-001..P0-008 | M | `p0-009-phase-audit.md` |

## Post-Phase Tasks

**Status**: COMPLETE (in retrospect — Phase 0 predates the framework).

After all Phase Tasks completed:
1. Phase 0 audit PR (#2) served as the post-phase equivalent, covering all four architect
   roles (acceptance/GRC, quality/QA, security, DevOps/infrastructure).
2. Seven known-debt items (D1-D7) recorded and rolled into Phase 1 work items.
3. Phase 0 handed off to Phase 1.

## Maintenance Phase Tasks

Maintenance items M0-001 through M0-007 rolled into Phase 1 tasks (P1-001 through
P1-013 resolve them). See `phase-0-delivery-system/backlog.md` for the full mapping.

| ID | Title | Source | Severity | Status | Resolved By |
|---|---|---|---|---|---|
| M0-001 | candelamoon-security base image decision (D2) | GRC | high | Completed | P1-003 |
| M0-002 | Populate GitHub Actions SHA pins (D7) | Security | medium | Completed | P1-010..P1-013 |
| M0-003 | TBD/DIGEST/SHA placeholder scan (D1) | Security | medium | Completed | Phase 1 |
| M0-004 | Validator UnicodeDecodeError handling gaps (D3) | QA | medium | Completed | Phase 1 |
| M0-005 | Signing key rotation cadence (D4) | Security | medium | Completed | Phase 1 ADR |
| M0-006 | SLSA L3 attainment plan (D5) | Security | low | Completed | Phase 1 ADR |
| M0-007 | Stale-graph max wait time (D6) | QA | low | Accepted | N/A |
