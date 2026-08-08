# Master Roadmap — CandelaMoon Program

> The single high-level guide to "where do we go next." Derived from
> `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md` §11 (Phased Roadmap)
> and organized for execution under the maestro framework.
>
> Each phase below has a goal, an exit gate, a status, a pointer to its detailed
> backlog (if any), and the related ADRs. Per-phase backlogs live next to this file
> at `.maestro-space/maestro-plans/phase-N-<short>-backlog.md` and are produced
> at the start of the phase. Per-task session artifacts (handoffs, ATDD checklists,
> coverage audits, session handouts) live at
> `.maestro-space/maestro-works/phase-N-<short>/<task-id>-<short>/`.

**Source of truth**: `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md` §11.
**Framework contract**: each phase runs N task sessions (14-step cycle) + 1 post-phase
session (4 architects) + 1 maintenance phase before the next phase may begin
(see `.maestro-space/maestro-docs/maestro-workflow.md` §3).

---

## Status Snapshot

| Phase | Title | Status | Detailed backlog |
|---|---|---|---|
| 0 | Delivery-System Design | **DONE** | `.maestro-space/maestro-plans/phase-0-delivery-system-backlog.md` |
| 1 | Delivery Foundation | **IN PROGRESS** (1/21 tasks) | `.maestro-space/maestro-plans/phase-1-delivery-system-backlog.md` |
| 2 | Repositories And Baselines | PENDING (next) | `.maestro-space/maestro-plans/phase-2-repositories-and-baselines-backlog.md` |
| 3 | Two Architecture Spines | PLANNED | — |
| 4 | Contract, Dispositions, And MVP Spec | PLANNED | — |
| 5 | Platform Foundation And UI Evaluation | PLANNED | — |
| 6 | Core Host Journey | PLANNED | — |
| 7 | Library And Session Journey | PLANNED | — |
| 8 | Stream Configuration And In-Stream TV UX | PLANNED | — |
| 9 | Controllers And Retained Client Features | PLANNED | — |
| 10 | Controlled Deletion And Simplification | PLANNED | — |
| 11 | Hardening And Release | PLANNED | — |
| 12 | Maintenance And Post-MVP Innovation | PLANNED | — |

---

## Phase 0 — Delivery-System Design — DONE

**Goal**: establish the framework that allows evidence-backed delivery to proceed.
**Exit gate**: spec, plan, design validator, agent architecture, and dual evidence
manifest schemas are committed and pass validation.
**Related ADRs**: 0013 (GitHub-Memtrace split authority), 0014 (Podman-first execution),
0015 (Multi-agent architecture), 0016 (ATDD red-phase), 0017 (Two-phase adversarial
review), 0018 (Red/blue security), 0019 (Coverage audit with Memtrace), 0020 (Session
handout), plus 0001-0012 for product boundaries.
**Detailed backlog**: `.maestro-space/maestro-plans/phase-0-delivery-system-backlog.md`
**Session artifacts**: `.maestro-space/maestro-works/phase-0-delivery-system/post-phase-0/session-handout.md`
**Closed PRs**: PR #1 (spec + plan), PR #2 (Phase 0 audit).

---

## Phase 1 — Delivery Foundation — IN PROGRESS

**Goal**: stand up the Podman-first CI pipeline, signed container images, GitHub
branch protection, evidence templates, per-commit / per-PR / nightly / release
workflows, self-hosted runners, and the canary PR that proves all paths.
**Exit gate**: a canary PR (P1-018) exercises every pipeline path (containerized +
device + Windows + evidence + sync); branch protection (P1-006) enforces the gates;
all four images (P1-005) are signed and published to GHCR; the design validator
(P1-017) runs in CI.
**Related ADRs**: 0013, 0014, 0015, 0019.
**Detailed backlog**: `.maestro-space/maestro-plans/phase-1-delivery-system-backlog.md`
(21 tasks: P1-001 through P1-021).
**Progress**: 1/21 tasks done (P1-021 — baseline test fixes).
**Next pending**: P1-001 (candelamoon-android Containerfile).

---

## Phase 2 — Repositories And Baselines — PENDING (next major)

**Goal**: pin and synchronize the official LuminalShine baseline; establish the
tracked documentation and ADR vocabulary; inventory the local `new-design/` visual
decisions into a tracked disposition ledger.
**Exit gate**: both repositories (CandelaMoon + LuminalShine mirror) have reproducible,
synchronized baselines and no architecture claim depends on a moving branch.
**Related ADRs**: 0003 (frozen Artemis baseline), 0004 (integration-lab mirror),
0005 (new app identity).
**Detailed backlog (stub)**: `.maestro-space/maestro-plans/phase-2-repositories-and-baselines-backlog.md`
(decomposed at the start of Phase 2).

**Scope summary**:
- Select and pin the initial supported official LuminalShine release tag and commit
  (the current `main` snapshot is evidence input only until that selection).
- Establish mirror tracking and branch rules (continuation of ADR 0004).
- Establish documentation paths, vocabulary, IDs, and ADR template (consolidates the
  schema work done in Phase 0 Task 1).
- Configure Memtrace exclusions for vendored and generated code.
- Inventory local `new-design/` visual decisions and contradictions into a tracked
  disposition ledger without making the local directory a reproducibility dependency
  (per spec §3.1).

---

## Phase 3 — Two Architecture Spines — PLANNED

**Goal**: map both repositories by shared capability area while producing complete
repo-specific spines.
**Exit gate**: every spine component has source, graph, and test evidence; all core
journeys trace end to end.
**Scope summary**:
- **CandelaMoon coverage**: activities, services, discovery, pairing, app grid,
  profiles, preferences, streaming/JNI, decoder/audio, input, persistence, TV
  integration, build variants, tests, and debt.
- **LuminalShine mirror coverage**: classic client-facing control, trust, catalog,
  process/session lifecycle, negotiation, stream/input paths, virtual display
  effects, client-visible settings/errors, and version behavior.

---

## Phase 4 — Contract, Dispositions, And MVP Spec — PLANNED

**Goal**: complete the capability contract, classify every inherited feature, write
the MVP specification, normalize the visual system, and approve the initial ADRs.
**Exit gate**: unknown rows are resolved or explicitly deferred, and MVP contains
no mirror-only dependency.
**Scope summary**:
- Complete the capability contract with no silent omission.
- Classify every inherited feature (per ADR 0012 disposition policy).
- Define official-host support and capability detection.
- Write MVP requirements, non-functional requirements, device tiers, performance
  budgets, and acceptance tests.
- Normalize the visual system into tracked `DESIGN.md`.
- Approve the initial ADRs and phased deletion ledger.

---

## Phase 5 — Platform Foundation And UI Evaluation — PLANNED

**Goal**: establish CandelaMoon identity and platform services, evaluate Compose for
TV via a bounded prototype, and build the first adaptive component layer.
**Exit gate**: deterministic navigation, no focus traps, acceptable performance,
correct accessibility, lifecycle recovery, and clean native-stream interop.
**Scope summary**:
- Establish CandelaMoon identity and branding without migration code.
- Add a platform and capability service for API tier, device, codec, and official
  host capabilities.
- Prototype Compose for TV with host grid, D-pad restoration, pairing, app library,
  accessibility, recreation, and native stream handoff.
- Benchmark API 28-30 compatibility and API 31+ primary tiers.
- Decide Compose or modern Views by ADR (per ADR 0009 evaluation criteria).
- Build one adaptive component layer.

---

## Phase 6 — Core Host Journey — PLANNED

**Goal**: replace discovery, manual add, pairing, host status, and host actions while
preserving verified underlying services where appropriate.
**Exit gate**: a fresh install can pair with an official host entirely through D-pad
on both platform tiers.

---

## Phase 7 — Library And Session Journey — PLANNED

**Goal**: replace app catalog, artwork, loading, launch, resume, quit, busy-session,
unavailable-app, and disconnect behavior. Preserve host ownership of catalog and
session state and hand off to the classic native stream.
**Exit gate**: paired host to active stream and back completes without inherited UI.

---

## Phase 8 — Stream Configuration And In-Stream TV UX — PLANNED

**Goal**: rebuild settings and profiles around verified negotiation. Capability-gate
codec, HDR, resolution, frame rate, audio, and display options. Replace the in-stream
menu, HUD, warnings, keyboard invocation, and recovery while protecting native
boundaries.
**Exit gate**: configuration is truthful for the connected official host and device,
and recovery is deterministic.

---

## Phase 9 — Controllers And Retained Client Features — PLANNED

**Goal**: validate controller mapping, rumble, TV-relevant keyboard/mouse behavior,
shortcuts, diagnostics, and every retained client-only capability. Use API 31+
enhancements without regressing API 28-30 core control.
**Exit gate**: every MVP `retain-client` and `adapt-to-luminal` row has acceptance
evidence.

---

## Phase 10 — Controlled Deletion And Simplification — PLANNED

**Goal**: remove approved mobile UI and behavior, Apollo-specific integration,
Artemis branding, root build flavor, pre-O input capture paths, obsolete API branches,
dormant flags, and orphan resources in isolated changes.
**Exit gate**: no unsupported UI route, feature flag, host control, or orphan
resource remains, and every deletion satisfies the Memtrace gate (per ADR 0012
deletion-evidence policy).

---

## Phase 11 — Hardening And Release — PLANNED

**Goal**: complete device, codec, controller, long-session, reconnect, lifecycle,
network, update, performance, memory, thermal, accessibility, localization, security,
dependency, license, signing, and rollback validation.
**Exit gate**: all official-host MVP journeys and both Android platform-tier
contracts pass with synchronized GitHub and Memtrace state.

---

## Phase 12 — Maintenance And Post-MVP Innovation — PLANNED

**Goal**: refresh compatibility for official LuminalShine releases; maintain Android
target compliance, dependencies, security, codecs, devices, Podman images, and
runners; evaluate client-only ideas through lightweight ADRs and capability rows;
prototype host-dependent ideas in the mirror without making them official-product
dependencies.
**Standing rule**: keep WebRTC excluded from CandelaMoon; changing that boundary
requires a separately brainstormed product design and superseding ADR (per ADR 0002).

---

## How Phases Move

The framework treats every phase as a discrete scope with a hard contract:

1. **Task sessions** — one per backlog item, each following the 14-step cycle, each
   producing one PR. The 14-step cycle is defined in
   `.maestro-space/maestro-docs/maestro-workflow.md` §2.
2. **Post-phase session** — after the last task of a phase merges, the orchestrator
   dispatches the 4 architects (grc, qa, security, devops) in two parallel pairs to
   produce per-role reports, a synthesized summary, and a maintenance plan. The
   post-phase session is **BLOCKING** for the next phase. See
   `.maestro-space/maestro-docs/maestro-workflow.md` §3.3.
3. **Maintenance phase** — the maintenance plan from the post-phase session becomes
   a regular phase with `M{N}-NNN` task IDs. Each maintenance task runs the standard
   14-step cycle. See `.maestro-space/maestro-docs/maestro-workflow.md` §3.4.
4. **Next phase** — begins only after the post-phase session and maintenance phase
   are complete.

**Cross-cutting principles** (per `.maestro-space/maestro-plans/global-objectives.md` §5):
- Evidence over assertion
- One task = one session = one PR
- Post-phase is blocking
- P-IDs are stable
- ADRs are the architecture record
- No undocumented project changes
- The framework is per-fork (per `maestro-conventions.md` §9)
