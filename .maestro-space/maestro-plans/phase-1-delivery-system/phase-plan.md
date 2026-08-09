# Phase 1 — Delivery Foundation — IN PROGRESS

**Goal**: Stand up the Podman-first CI pipeline, signed container images, GitHub
branch protection, evidence templates, per-commit / per-PR / nightly / release
workflows, self-hosted runners, and canary PR.
**Exit gate**: Canary PR (P1-018) exercises every pipeline path; branch protection
(P1-006) enforces gates; all four images (P1-005) signed and published to GHCR;
design validator (P1-017) runs in CI.
**Related ADRs**: 0013, 0014, 0015, 0019
**Dependencies on previous phase**: Phase 0 complete.
**Estimated task count**: 22 tasks (4 completed, 0 in development, 18 pending)

---

## Phase Tasks

### Group A: Container Images (no deps)

| # | ID | Title | Status | Depends On | Complexity | Evidence |
|---|---|---|---|---|---|---|
| 1 | P1-001 | candelamoon-android Containerfile | **Completed** | — | M | Containerfile at `infra/containers/candelamoon-android/Containerfile`; green-verified 2026-08-08; review phases 1+2 closed; STR-06 applied. Handoff: `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android-containerfile/`. |
| 2 | P1-002 | candelamoon-docs Containerfile | **Completed** | — | S | Containerfile at `infra/containers/candelamoon-docs/Containerfile`; green-verified 2026-08-09; review phases 1+2 closed; SEC-01 (workspace import isolation) + SEC-02 (wheel-only pip + builder-account split) applied. Handoff: `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/`. |
| 3 | P1-003 | candelamoon-security Containerfile | Pending | — | M | — |
| 4 | P1-004 | luminal-contract Containerfile | Pending | — | S | — |

### Group B: Image Publication (deps on Group A)

| # | ID | Title | Status | Depends On | Complexity | Evidence |
|---|---|---|---|---|---|---|
| 5 | P1-005 | Build and publish images to GHCR with signatures | Pending | P1-001..P1-004 | M | No GHCR images published |

### Group C: GitHub Configuration

| # | ID | Title | Status | Depends On | Complexity | Evidence |
|---|---|---|---|---|---|---|
| 6 | P1-006 | GitHub branch protection rulesets | Pending | — | S | PR #3: CODEOWNERS (`* @magalz`), CI workflow exists. Rulesets pending (stale pre-framework — reset 2026-08-09). |
| 7 | P1-007 | PR template with task/phase/evidence fields | **Completed** | — | S | `.github/PULL_REQUEST_TEMPLATE.md` exists with full content (AC, evidence, review stack, rollback). PR #3. |
| 8 | P1-008 | Issue and milestone templates | Pending | — | S | `.github/ISSUE_TEMPLATE/` has bug_report, feature_request, config. Maestro-specific templates (deferred/tech-debt/secops) from `maestro-templates/` not yet added (stale pre-framework — reset 2026-08-09). |
| 9 | P1-009 | Evidence-manifest YAML template | Pending | — | S | — |

### Group D: CI Workflows (deps on Groups A+B)

| # | ID | Title | Status | Depends On | Complexity | Evidence |
|---|---|---|---|---|---|---|
| 10 | P1-010 | Per-commit CI (lint, format, fast tests, docs validate, secret scan, Codecov) | Pending | P1-001..P1-005 | L | `ci.yml` exists: test job + JaCoCo + Codecov. Missing: lint, format, docs validate, secret scan. Stale pre-framework — reset 2026-08-09. |
| 11 | P1-011 | Per-PR CI (full tests, API-tier matrix, Memtrace sync) | Pending | P1-010 | L | — |
| 12 | P1-012 | Nightly CI (emulator compat, dependency freshness, contract fixtures) | Pending | P1-010 | M | — |
| 13 | P1-013 | Release-candidate CI (device tests, signing, provenance) | Pending | P1-010 | L | — |

### Group E: Self-Hosted Runners

| # | ID | Title | Status | Depends On | Complexity | Evidence |
|---|---|---|---|---|---|---|
| 14 | P1-014 | Google TV Streamer runner | Pending | — | M | — |
| 15 | P1-015 | Windows runner for host integration | Pending | — | M | — |

### Group F: CI Integrations (deps on Group D)

| # | ID | Title | Status | Depends On | Complexity | Evidence |
|---|---|---|---|---|---|---|
| 16 | P1-016 | Memtrace sync check in CI | Pending | P1-011 | M | — |
| 17 | P1-017 | Design validator in candelamoon-docs image and CI | Pending | P1-002, P1-010 | S | — |

### Group G: Validation and Cleanup (deps on Groups A-F)

| # | ID | Title | Status | Depends On | Complexity | Evidence |
|---|---|---|---|---|---|---|
| 18 | P1-018 | Canary PR proving all paths | Pending | P1-005..P1-017 | M | — |
| 19 | P1-019 | Remove AppVeyor configuration | Pending | P1-018 | S | `appveyor.yml` still present at repo root |
| 20 | P1-020 | Phase 1 audit PR | Pending | P1-018 | S | — |

### Group H: Fixes (completed out of order)

| # | ID | Title | Status | Depends On | Complexity | Evidence |
|---|---|---|---|---|---|---|
| 21 | P1-021 | Fix baseline unit test failures | **Completed** | — | M | PR #6 merged. 68/68 green. Coverage PASS (50/50). |

### Group I: Security Remediation

| # | ID | Title | Status | Depends On | Complexity | Evidence |
|---|---|---|---|---|---|---|
| 22 | P1-022 | Dependency vulnerability remediation (48 Dependabot alerts) | Pending | P1-001..P1-004 (before P1-005) | L | 1 critical (Bouncy Castle), 21 high (16x Netty), 24 medium, 2 low |

### Interphase Framework Work

| # | ID | Title | Status | Depends On | Complexity | Evidence |
|---|---|---|---|---|---|---|
| — | — | Maestro framework v2 (musician naming, project-agnostic, 22 templates) | **Completed** | — | L | PR #9 merged. Phase plans and task files ready (PR #10). |

## Post-Phase Tasks

After all Phase Tasks complete → post-phase session per `maestro-post-phase.md`.

## Maintenance Phase Tasks

Generated by post-phase. M1-NNN IDs. Initially empty.

---

## Dependency Graph

```
Groups A, C, E can run in parallel (no dependencies)
P1-022 (Group I) depends on Group A — runs after P1-004, before P1-005
Group B depends on A + P1-022
Group D depends on A+B
Group F depends on D
Group G depends on A through F
P1-021 already completed (unblocks CI gate)
```

## Next Pending Tasks (in priority order)

1. P1-003 → P1-004 (Group A): Remaining Containerfiles (security, luminal-contract) — no deps, ready NOW
2. P1-022 (Group I): Dependency vulnerability remediation — depends on Group A, before P1-005
3. P1-005 (Group B): Build and publish images to GHCR — depends on Group A + P1-022
4. P1-008 (Group C): Issue templates — small, no deps, 3 maestro-specific templates to add
5. P1-009 (Group C): Evidence manifest template — no deps
6. P1-006 (Group C): Branch protection rulesets — GitHub settings/config task
7. P1-014, P1-015 (Group E): Self-hosted runners — no deps
8. P1-010 (Group D): Per-commit CI — add lint/format; full deps on P1-001..P1-005 for containerized jobs
