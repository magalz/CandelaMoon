# Phase 2 — Repositories And Baselines — PENDING (STUB)

> Stub for Phase 2. Decomposed at the start of Phase 2. The brief below is
> distilled from `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md`
> §11 Phase 2 and from the spec's repository-ownership rules (§3).

**Phase**: Phase 2 — Repositories And Baselines
**Status**: PENDING (decomposed at the start of Phase 2)
**Goal**: pin and synchronize the official LuminalShine baseline; establish tracked
documentation vocabulary; inventory `new-design/` visual decisions.
**Exit gate**: both repositories (CandelaMoon + LuminalShine mirror) have
reproducible, synchronized baselines and no architecture claim depends on a moving
branch.
**Related ADRs**: 0003 (frozen Artemis baseline), 0004 (integration-lab mirror),
0005 (new app identity).

---

## Indicative Task Groups (to be decomposed)

The following task groups are derived from the Phase 2 brief. Each becomes one or
more leaf tasks (P2-NNN) at the start of Phase 2, each running the standard
14-step cycle.

### P2-G1 — Pin official LuminalShine release

- **Goal**: select and pin the initial supported official LuminalShine release
  tag and commit. The current `main` snapshot is evidence input only until that
  selection (per spec §3.3).
- **Acceptance criteria (indicative)**:
  - One or more official LuminalShine release tags are identified as candidate
    supports.
  - At least one tagged official release is selected and pinned (commit SHA
    recorded in `docs/adr/` as a new ADR or as a supersession of ADR 0004).
  - The MVP allowlist is documented with the selected release(s) per spec §3.3.
- **Dependencies**: Phase 1 complete (canary PR proves the delivery system can
  support the pinning workflow).
- **Related ADRs**: 0003, 0004, 0005.
- **Indicative complexity**: M.

### P2-G2 — Establish mirror tracking and branch rules

- **Goal**: formalize the integration-lab mirror branch rules and the LuminalShine
  mirror tracking mechanism (continuation of ADR 0004).
- **Acceptance criteria (indicative)**:
  - Mirror branch strategy is documented (which branch tracks which upstream).
  - Mirror push rules are enforced (push to upstream disabled; per spec §3.2).
  - Mirror update cadence is documented.
- **Dependencies**: P2-G1 (the pin establishes the mirror base).
- **Indicative complexity**: S.

### P2-G3 — Documentation paths, vocabulary, IDs, and ADR template consolidation

- **Goal**: consolidate the documentation paths, vocabulary, IDs, and ADR
  template that were introduced in Phase 0 (P0-001) and Phase 1 (P1-007, P1-008,
  P1-009). Verify the spec section 4.1 artifact list is complete and discoverable.
- **Acceptance criteria (indicative)**:
  - Every spec §4.1 artifact is reachable at a documented path.
  - The ADR template at `docs/adr/0000-template.md` is reviewed for completeness
    against the 20 ADRs.
  - The implementation backlog is split between `.maestro-space/maestro-plans/`
    (per-phase) and the cross-phase reference docs.
- **Dependencies**: P2-G1.
- **Indicative complexity**: S.

### P2-G4 — Configure Memtrace exclusions for vendored and generated code

- **Goal**: configure Memtrace to exclude vendored libraries, generated code, and
  build artifacts so architecture scoring (community, centrality, dead-code,
  complexity) is not skewed by non-product code (per spec §5.3).
- **Acceptance criteria (indicative)**:
  - Memtrace exclusion config covers: `app/build/`, `app/.cxx/`, generated source,
    vendored libraries.
  - A re-index after exclusion shows the expected reduction in nodes/edges.
  - Documentation of the exclusion list is committed.
- **Dependencies**: P2-G1 (the pin is the baseline for the index).
- **Indicative complexity**: M.

### P2-G5 — Inventory `new-design/` visual decisions

- **Goal**: inventory the local `new-design/` visual decisions and contradictions
  into a tracked visual-reference disposition ledger (per spec §3.1, §11 Phase 2),
  without making the local directory a reproducibility dependency.
- **Acceptance criteria (indicative)**:
  - Every file in `new-design/` is referenced from the tracked disposition
    ledger with one of: `accepted`, `rejected`, `deferred`, `reinterpreted`.
  - The ledger is committed to a tracked path (e.g., `docs/visual-disposition.md`).
  - `new-design/` remains gitignored (per spec §3.1) and is no longer
    authoritative for any architecture or product conclusion.
- **Dependencies**: none (can start as soon as Phase 1 is complete).
- **Indicative complexity**: M.

### P2-G6 — Phase 2 audit and post-phase session

- **Goal**: per the framework, the last task of Phase 2 is a phase-audit PR that
  links all task PRs, capability rows, ADRs, tests, known debt, and exit-gate
  evidence. After P2-XXX merges, the post-phase session runs (4 architects).
- **Acceptance criteria**: per `.maestro-space/maestro-docs/maestro-workflow.md`
  §3.3.
- **Dependencies**: P2-G1 through P2-G5.
- **Indicative complexity**: S.

---

## Post-Phase 2 Session (BLOCKING for Phase 3)

Per the framework contract, the post-phase session is mandatory and blocking. See
`.maestro-space/maestro-docs/maestro-workflow.md` §3.3. Outputs (committed):
- `grc-report.md` + `.json`
- `qa-report.md` + `.json`
- `security-report.md` + `.json`
- `devops-report.md` + `.json`
- `summary.md` (orchestrator-synthesized)
- `maintenance-phase-plan.md` (becomes the M2-XXX backlog)

---

## Open Questions for Phase 2 Decomposition

1. Does the LuminalShine allowlist need to include more than one release at MVP
   cut (per spec §3.3 "at least one tagged official release")?
2. Should the visual-disposition ledger be a single file or one file per
   `new-design/` source?
3. Is the Memtrace exclusion config best placed in
   `.maestro-space/maestro-plans/` (configuration is framework-level) or in
   `docs/infrastructure/` (configuration is product-level)? My recommendation:
   `docs/infrastructure/memtrace-config.md` (product-level decision with
   framework-level enforcement).
4. Does the official-host integration profile
   (`docs/superpowers/specs/...md` §4.1 "luminalshine-integration-profile") get
   authored in P2-G1 or as a separate P2 task?

These questions are recorded for the next session to answer before P2-G1 begins.
