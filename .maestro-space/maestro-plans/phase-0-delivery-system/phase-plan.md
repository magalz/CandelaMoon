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
| 1 | P0-001 | Machine-readable schemas | Completed | — | M | `p0-001-machine-readable-schemas.md` |
| 2 | P0-002 | Design validator script | Completed | P0-001 | M | `p0-002-design-validator.md` |
| 3 | P0-003 | ADR template and 20-decision register | Completed | P0-001 | L | `p0-003-adr-template-and-register.md` |
| 4 | P0-004 | Toolchain pins and dev environment | Completed | — | S | `p0-004-toolchain-pins.md` |
| 5 | P0-005 | Podman-first CI architecture | Completed | — | M | `p0-005-ci-architecture.md` |
| 6 | P0-006 | Device lab and runner architecture | Completed | — | M | `p0-006-device-lab-architecture.md` |
| 7 | P0-007 | Security design | Completed | — | L | `p0-007-security-design.md` |
| 8 | P0-008 | Operational policies and Phase 1 backlog | Completed | P0-005 | M | `p0-008-operational-policies.md` |
| 9 | P0-009 | Phase 0 audit and review | Completed | P0-001..P0-008 | M | `p0-009-phase-audit.md` |

## Post-Phase Tasks — COMPLETE

Phase 0 predates the framework. The phase-audit PR (#2) served as the post-phase equivalent.
Seven known-debt items (D1-D7) rolled into Phase 1 tasks.

## Maintenance Phase — COMPLETE

M0-001 through M0-007 rolled into Phase 1. See `backlog.md` for the mapping.
