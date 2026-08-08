# Phase 1 — Delivery Foundation — IN PROGRESS

**Goal**: Stand up the Podman-first CI pipeline, signed container images, GitHub
branch protection, evidence templates, per-commit / per-PR / nightly / release
workflows, self-hosted runners, and the canary PR that proves all paths.
**Exit gate**: A canary PR (P1-018) exercises every pipeline path (containerized +
device + Windows + evidence + sync); branch protection (P1-006) enforces the gates;
all four images (P1-005) are signed and published to GHCR; the design validator
(P1-017) runs in CI.
**Related ADRs**: 0013, 0014, 0015, 0019
**Dependencies on previous phase**: Phase 0 complete (all 9 tasks, phase-audit PR #2 merged).
**Estimated task count**: 21 tasks (1 completed, 20 pending; plus 1 interphase framework
restructuring task completed).

---

## Phase Tasks

### Group A: Container Images (no dependencies — can parallelize)

| # | ID | Title | Status | Depends On | Complexity | Task File |
|---|---|---|---|---|---|---|
| 1 | P1-001 | candelamoon-android Containerfile | Pending | — | M | `p1-001-candelamoon-android-containerfile.md` |
| 2 | P1-002 | candelamoon-docs Containerfile | Pending | — | S | `p1-002-candelamoon-docs-containerfile.md` |
| 3 | P1-003 | candelamoon-security Containerfile | Pending | — | M | `p1-003-candelamoon-security-containerfile.md` |
| 4 | P1-004 | luminal-contract Containerfile | Pending | — | S | `p1-004-luminal-contract-containerfile.md` |

### Group B: Image Publication (depends on Group A)

| # | ID | Title | Status | Depends On | Complexity | Task File |
|---|---|---|---|---|---|---|
| 5 | P1-005 | Build and publish images to GHCR with signatures | Pending | P1-001, P1-002, P1-003, P1-004 | M | `p1-005-build-publish-images.md` |

### Group C: GitHub Configuration (no dependencies — can parallelize)

| # | ID | Title | Status | Depends On | Complexity | Task File |
|---|---|---|---|---|---|---|
| 6 | P1-006 | Configure GitHub branch protection rulesets | Pending | — | S | `p1-006-branch-protection.md` |
| 7 | P1-007 | Add PR template with task/phase/capability/evidence fields | Pending | — | S | `p1-007-pr-template.md` |
| 8 | P1-008 | Add issue and milestone templates | Pending | — | S | `p1-008-issue-templates.md` |
| 9 | P1-009 | Create evidence-manifest YAML template | Pending | — | S | `p1-009-evidence-manifest-template.md` |

### Group D: CI Workflows (depends on Groups A+B)

| # | ID | Title | Status | Depends On | Complexity | Task File |
|---|---|---|---|---|---|---|
| 10 | P1-010 | Per-commit CI workflow (lint, format, fast tests, docs validate, secret scan, Codecov) | Pending | P1-001..P1-005 | L | `p1-010-per-commit-ci.md` |
| 11 | P1-011 | Per-PR CI workflow (full tests, API-tier matrix, Memtrace sync check) | Pending | P1-010 | L | `p1-011-per-pr-ci.md` |
| 12 | P1-012 | Nightly CI workflow (emulator compat, dependency freshness, contract fixtures) | Pending | P1-010 | M | `p1-012-nightly-ci.md` |
| 13 | P1-013 | Release-candidate CI workflow (device tests, signing, provenance) | Pending | P1-010 | L | `p1-013-release-candidate-ci.md` |

### Group E: Self-Hosted Runners (no dependencies — can parallelize with Groups A-C)

| # | ID | Title | Status | Depends On | Complexity | Task File |
|---|---|---|---|---|---|---|
| 14 | P1-014 | Configure self-hosted runner for Google TV Streamer | Pending | — | M | `p1-014-tv-streamer-runner.md` |
| 15 | P1-015 | Configure self-hosted Windows runner for host integration | Pending | — | M | `p1-015-windows-runner.md` |

### Group F: CI Integrations (depends on Group D)

| # | ID | Title | Status | Depends On | Complexity | Task File |
|---|---|---|---|---|---|---|
| 16 | P1-016 | Integrate Memtrace synchronization check into CI | Pending | P1-011 | M | `p1-016-memtrace-sync-ci.md` |
| 17 | P1-017 | Integrate design validator into candelamoon-docs image and CI | Pending | P1-002, P1-010 | S | `p1-017-design-validator-ci.md` |

### Group G: Validation and Cleanup (depends on Groups A-F)

| # | ID | Title | Status | Depends On | Complexity | Task File |
|---|---|---|---|---|---|---|
| 18 | P1-018 | Canary PR proving all paths (containerized + device + Windows + evidence + sync) | Pending | P1-005..P1-017 | M | `p1-018-canary-pr.md` |
| 19 | P1-019 | Remove AppVeyor configuration (appveyor.yml) | Pending | P1-018 | S | `p1-019-remove-appveyor.md` |
| 20 | P1-020 | Phase 1 audit PR | Pending | P1-018 | S | `p1-020-phase-audit.md` |

### Group H: Pre-existing Fixes (completed out of order to unblock CI)

| # | ID | Title | Status | Depends On | Complexity | Task File |
|---|---|---|---|---|---|---|
| 21 | P1-021 | Fix baseline unit test failures surfaced by Phase 0 CI | **Completed** | — | M | `p1-021-baseline-test-fixes.md` |

### Interphase Work (framework restructuring — completed)

| # | ID | Title | Status | Depends On | Complexity | Task File |
|---|---|---|---|---|---|---|
| — | — | Maestro framework v2 (musician naming, project-agnostic, complete templates, phase plans) | **Completed** | — | L | PR #9 (pending merge) |

## Post-Phase Tasks

After all Phase Tasks are completed:
1. Execute the Post-Phase session per `maestro-post-phase.md`.
2. Four architects (Haydn, Ravel, Paganini, Vivaldi) produce per-role reports.
3. Bernstein synthesizes the summary and maintenance plan.
4. Outputs are committed to `.maestro-space/maestro-works/phase-1-delivery-system/post-phase-1/`.

## Maintenance Phase Tasks

Generated by the Post-Phase session. See `maestro-maintenance.md`.
Tasks use M1-NNN IDs. Initially empty.

| ID | Title | Source Report | Severity | Status | Depends On | Complexity |
|---|---|---|---|---|---|---|
| — | (populated post-phase) | — | — | — | — | — |

---

## Dependency Graph

```
Group A (P1-001..P1-004) ─────────────────────┐
Group C (P1-006..P1-009) ───┐                   │
Group E (P1-014, P1-015) ───┤                   │
                             │                   ▼
                             │              Group B (P1-005)
                             │                   │
                             │    ┌──────────────┘
                             │    ▼
                             ├─► Group D (P1-010)
                             │    ├─► P1-011 ──► P1-016
                             │    ├─► P1-012
                             │    ├─► P1-013
                             │    └─► P1-017
                             │         │
                             └─────────┼──────┐
                                       ▼      ▼
                                  Group G (P1-018)
                                       ├─► P1-019
                                       └─► P1-020

P1-021: Completed out of order (unblocked CI gate).
Interphase: Framework v2 restructuring (completed, PR #9 pending merge).
```

## Next Pending Tasks

1. **P1-001** — candelamoon-android Containerfile (Group A, no dependencies, M complexity)
2. **P1-002** — candelamoon-docs Containerfile (Group A, no dependencies, S complexity)
3. **P1-003** — candelamoon-security Containerfile (Group A, no dependencies, M complexity)
4. **P1-004** — luminal-contract Containerfile (Group A, no dependencies, S complexity)
5. **P1-006** through **P1-009**, **P1-014**, **P1-015** — also have no dependencies

Groups A, C, and E can all begin immediately. Groups B and D follow.
