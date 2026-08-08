# Global Objectives

> The north star for the CandelaMoon program. Defines the multi-phase strategy and the
> success criteria for the entire effort, as distilled from
> `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md`.

## 1. Mission

CandelaMoon becomes a TV-only Android client tailored to official LuminalShine releases.
It starts from Artemis (itself derived from Moonlight Android) and evolves into a
focused, evidence-driven product that does not remain a general Artemis, Apollo, or
Sunshine client.

The program establishes two evidence-backed architecture spines and a complete
host-to-client capability contract before feature development. Work proceeds through
small, dependency-ordered pull requests with explicit evidence and exit gates rather
than calendar promises.

## 2. Product Boundaries (from spec §2)

- **Host and transport**: official LuminalShine releases only; inherited classic
  Moonlight/GameStream-compatible transport. WebRTC path is out of scope for MVP.
- **Artemis inheritance**: Artemis is a frozen source baseline; no routine future
  Artemis merges. CandelaMoon assumes ownership of protocol, decoder, device, Android
  platform, security, native dependencies, and maintenance.
- **Application identity**: new application ID. No migration of existing Artemis
  installations, pairings, databases, or settings.
- **Form factor**: Android TV only. Phone, tablet, touch-first, portrait, foldable,
  DeX, and external-display-controller behavior are classified and removed in
  controlled phases.
- **Platform tiers**: `minSdk` stays at API 28 (TV 9-11 installable). API 31+ is the
  primary tier; API 28-30 is the compatibility tier. Enhancements are capability-gated.
- **UI direction**: one adaptive UI for both platform tiers. Compose for TV evaluated
  through a bounded prototype before selection. Streaming, JNI, MediaCodec, service,
  persistence, and input boundaries are protected until separate evidence justifies
  changing them.

## 3. Repository Ownership (from spec §3)

- **CandelaMoon** owns: the client architecture spine, ADRs, the LuminalShine
  integration profile, the cross-product capability contract, the inherited feature
  inventory and disposition ledger, the MVP product spec, the visual-system
  integration contract, the delivery roadmap, and phase evidence.
- **LuminalShine Integration Lab** (`magalz/luminalshine-mirror`) is an integration lab
  that may contain observed host architecture, documentation improvements, contract
  probes, and post-MVP experiments. It is never an implicit CandelaMoon runtime
  requirement.
- **Official LuminalShine** (`NortheBridge/luminalshine`) is the upstream authority.

## 4. Phase Strategy

The program organizes work into phases. Each phase:

1. Has a clearly stated goal and exit gate.
2. Runs N task sessions, each following the 14-step cycle.
3. Ends with a post-phase session (4 architects) and a maintenance phase.
4. Hands off to the next phase only after the post-phase report is committed and
   the maintenance phase is complete.

### Phase 0 — Delivery System Design (COMPLETE)

**Goal**: establish the framework that allows evidence-backed delivery to proceed.
**Exit gate**: spec, plan, design validator, agent architecture, and dual evidence
manifest schemas are committed and pass validation.

**Status**: complete.

**Phase plan**: `.maestro-space/maestro-plans/phase-0-delivery-system/phase-plan.md`

### Phase 1 — Delivery System (IN PROGRESS)

**Goal**: stand up the Podman-first CI pipeline, signed container images, GitHub
branch protection, evidence templates, per-commit / per-PR / nightly / release
workflows, self-hosted runners, and the canary PR that proves all paths.
**Exit gate**: a canary PR exercises every pipeline path (containerized + device +
Windows + evidence + sync); branch protection enforces the gates; all four images
are signed and published to GHCR; the design validator runs in CI.

**Status**: In Progress (1/21 tasks completed: P1-021).
**Phase plan**: `.maestro-space/maestro-plans/phase-1-delivery-system/phase-plan.md`
**Next pending**: P1-001 (candelamoon-android Containerfile).

### Phase 2+ — Product Phases (PLANNED)

The post-Phase 1 phases will be defined after the Phase 1 post-phase report and
maintenance phase complete.

**Phase 2 plan (stub)**: `.maestro-space/maestro-plans/phase-2-repositories-and-baselines/phase-plan.md`

## 5. Cross-Phase Principles

These are non-negotiable across all phases. They come from the spec, the ADRs, and
the framework's own conventions.

1. **Evidence over assertion**: every claim is backed by a command, a log, a graph
   query, or a test. `coverage_audit` and `Memtrace reconciliation` are gates, not
   decorations.
2. **One task = one session = one PR**: no multi-tasking, no session continuation
   across the PR-creation boundary.
3. **Post-phase is blocking**: the post-phase session + maintenance phase is
   mandatory between phases. Skipping it is a process violation.
4. **P-IDs are stable**: once a task ID is assigned, it persists. Re-ordering or
   re-numbering the backlog is allowed; renaming a task ID is not.
5. **ADRs are the architecture record**: every architectural decision is recorded
   as an ADR with status, context, decision, consequences, alternatives, and
   evidence. The framework is the keeper; the GRC architect is the auditor.
6. **No undocumented project changes**: the diff between any two merged commits
   is fully accounted for in the corresponding session's handoff and (for security-
   relevant changes) the security review.
7. **The framework is per-fork**: the framework files (`.maestro-space/`) are
   local to each fork or clone. The product (`/docs/`, `/app/`, etc.) is the
   shared artifact.

## 6. Success Criteria for the Program

- TV-only LuminalShine client is the only form factor delivered
- 100% of inherited Artemis features are dispositioned (kept / adapted / dropped /
  deferred) with evidence per decision
- Cross-product capability contract is complete and tested
- All four CI tiers (per-commit, per-PR, nightly, release-candidate) are green
- All four container images are signed and published
- The design validator runs in CI and gates every commit
- Memtrace is synchronized with every merged commit
- Every architectural decision has an ADR with evidence
- The product can be installed, paired, browsed, launched, streamed, controlled,
  recovered, and disconnected on every supported API tier
- The post-phase + maintenance discipline holds across all phase boundaries

## 7. Bernstein Path Configuration

> Read at session start so Bernstein knows where everything is without scanning.

### Phase Plans (ordered by execution)

| Phase | Status | Plan File | Workspace |
|---|---|---|---|
| 0 | Complete | `.maestro-space/maestro-plans/phase-0-delivery-system/phase-plan.md` | `.maestro-space/maestro-works/phase-0-delivery-system/` |
| 1 | In Progress | `.maestro-space/maestro-plans/phase-1-delivery-system/phase-plan.md` | `.maestro-space/maestro-works/phase-1-delivery-system/` |
| 2 | Pending | `.maestro-space/maestro-plans/phase-2-repositories-and-baselines/phase-plan.md` | `.maestro-space/maestro-works/phase-2-repositories-and-baselines/` |

### Framework Documents

| Document | Path |
|---|---|
| Orchestrator guide | `.maestro-space/maestro-docs/maestro-orchestrator-guide.md` |
| Workflow | `.maestro-space/maestro-docs/maestro-workflow.md` |
| Setup guide | `.maestro-space/maestro-docs/maestro-setup.md` |
| Post-phase guide | `.maestro-space/maestro-docs/maestro-post-phase.md` |
| Maintenance guide | `.maestro-space/maestro-docs/maestro-maintenance.md` |
| Conventions | `.maestro-space/maestro-docs/maestro-conventions.md` |
| Agent registry | `.maestro-space/maestro-agents/agent-manifest.json` |
| Templates | `.maestro-space/maestro-templates/` |

### Global Planning Files

| Document | Path |
|---|---|
| Global objectives | `.maestro-space/maestro-plans/global-objectives.md` |
| Master roadmap | `.maestro-space/maestro-plans/master-roadmap.md` |

### External Context (`/docs/`)

| Resource | Path |
|---|---|
| Spec | `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md` |
| ADR register | `docs/adr/` |
| Infrastructure docs | `docs/infrastructure/` |
| Schemas | `docs/schema/` |

### Session Start Order for Bernstein

1. Read this file (`global-objectives.md`) for the path map.
2. Read the orchestrator guide for dispatch rules.
3. Find the current phase from the table above.
4. Read the phase plan to find the next Pending task.
5. Read the task file for details and dependencies.
6. Read the session handout from the previous session (in the workspace).
7. Check git status, open PRs, CI state.
8. Report plan to user. Dispatch.
