# Maestro Workflow

> How work moves through the system. Defines the per-task cycle, the per-phase
> scaffolding (post-phase session + maintenance phase), and the blocking rules
> between phases.
>
> See companion documents:
> - **`maestro-orchestrator-guide.md`** — dispatch matrix, handoff protocol, review pipeline.
> - **`maestro-conventions.md`** — JSON+MD output format, file naming, tag nomenclature, agent contracts.
> - **`maestro-setup.md`** — rules for the phase setup session.
> - **`maestro-post-phase.md`** — rules for post-phase execution.
> - **`maestro-maintenance.md`** — rules for maintenance phase execution.

---

## 1. Mental Model

```
Phase N
  ├─ Task 1   ─► cycle ─► PR #1 ─► session ends
  ├─ Task 2   ─► cycle ─► PR #2 ─► session ends
  ├─ ...
  └─ Task N   ─► cycle ─► PR #N ─► session ends
                                      │
                                      ▼
                        ┌─ POST-PHASE SESSION ─┐
                        │ Bernstein + 4        │
                        │ architects analyze   │
                        │ the whole phase      │
                        └──────────┬────────────┘
                                   │
                                   ▼
                        ┌─ MAINTENANCE PHASE ──┐
                        │ N tasks (1 session   │
                        │ = 1 cycle = 1 PR)    │
                        └──────────┬────────────┘
                                   │
                                   ▼
                              Phase N+1
```

**One task = one session = one PR.** Bernstein works on exactly one task per session
and terminates the session when the PR is opened.

**One phase = N task sessions + one post-phase session + one maintenance phase.**

---

## 2. Per-Task Cycle

Every leaf task flows through this cycle:

```
 1. Bernstein creates the task handoff.
    Acceptance criteria populated. Evidence manifest initialized.

 2. IF task has testable behavior:
    Dispatch Ravel (QA Architect) to create TDD red-phase scaffolds.
    Produces: ATDD checklist, failing tests, sets red_phase_verified.

 3. Dispatch the appropriate production agent (Bach, Vivaldi, Paganini,
    Haydn, Schubert, Debussy) with the handoff.
    Agent implements, runs tests red→green, refactors while green.
    Updates the handoff. Writes activity report.

 4. Dispatch Review Phase 1 IN PARALLEL:
    Berlioz (Blind Hunter), Bartók (Edge Case Hunter), Verdi (Acceptance Analyst).
    Each gets need-to-know context only. Writes findings.

 5. Bernstein triages Phase 1 findings: normalize, dedupe, assess severity,
     route (patch / defer / dismiss / decision-needed).

 5a. Bernstein creates GitHub issues for every deferred finding with severity
     HIGH or MEDIUM (per orchestrator guide §8.2.1). Issue URLs are recorded
     in the session handout's Known Debt table and a dedicated "GitHub Issues
     Created" section.

 6. IF patches needed: dispatch Bach again with triaged findings.

 7. Dispatch Review Phase 2 SEQUENTIALLY:
     Stravinsky (Red Team) first, then Brahms (Blue Team).

 8. Bernstein triages Phase 2 findings.

 8a. Bernstein creates GitHub issues for every deferred finding with severity
     HIGH or MEDIUM (per orchestrator guide §8.2.1). Issue URLs are recorded
     in the session handout.

 9. IF patches needed: dispatch Bach again.

10. IF task has testable behavior:
    Dispatch Ravel for coverage audit + Memtrace reconciliation.
    Rates: pass / conditional-pass / fail.
    IF fail: back to step 3 with coverage tasks.

11. IF UAT applicable: present to user for testing.

12. Dispatch Schubert (Tech Writer) to document and prepare session handout.

13. Bernstein opens the PR via the bot workflow (`.github/workflows/create-pr.yml`).
    The PR author MUST be `app/candelamoon-bot`, not the human CODEOWNER.
    This ensures the human can approve their own PRs without bypassing branch rules.
    Run Memtrace review against the synchronized graph.

 14. Schubert creates session handout. SESSION ENDS.

15. Bernstein commits framework-state changes (task file status, phase plan
     status) directly to the default branch. These are NOT left in the task
     PR — the next session must see the authoritative task status regardless
     of whether the PR is merged yet.
```

### Bootstrap Exception (Documentation-Only Tasks)

For documentation-only tasks (no testable behavior):
- Skip steps 2 and 10 (TDD and coverage audit)
- Still run Review Phases 1-2, Schubert, and PR creation

---

## 3. Phase Scaffolding

### 3.1 Pre-Phase Readiness

Before Phase N begins, Bernstein checks:
- All open issues from the previous phase resolved or explicitly deferred?
- Previous phase's post-phase report committed?
- Previous phase's maintenance phase complete?
- Any Critical findings unaddressed?

If any answer is no → HALT, warn the user, request explicit confirmation.

### 3.2 Phase Execution

Phase N runs N task sessions, each following the cycle above.

### 3.3 Post-Phase Session (MANDATORY, BLOCKING)

After the last task of Phase N is merged, a post-phase session runs:

**Participants**: Bernstein + 4 architects (Haydn, Ravel, Paganini, Vivaldi).

**Outputs** (committed, not PR'd):
- Governance report (Haydn)
- QA report (Ravel)
- Security report (Paganini)
- DevOps report (Vivaldi)
- Summary (Bernstein-synthesized)
- Maintenance phase plan

**HARD RULE**: The post-phase session is **BLOCKING** for Phase N+1. No exceptions.

### 3.4 Maintenance Phase

The maintenance phase is a regular phase with its own backlog (the maintenance plan
from the post-phase session). Each maintenance task runs the standard cycle.
Tasks use `M{N}-NNN` IDs.

### 3.5 Phase Boundary Recap

```
Phase N
  ├─ N task sessions (each 1 PR)
  ├─ 1 post-phase session (4 architects, no PR, reports committed)
  └─ 1 maintenance phase (M-tasks, each 1 PR)
       │
       ▼
Phase N+1
```

---

## 4. Decision-Only Sessions

Short sessions where Bernstein clarifies a design decision with the user. Not a task,
not a phase. Reads current state, surfaces options, awaits user input, commits the
decision (typically as an ADR). Recorded in the next session's handout.

---

## 5. Multi-Tasking Prohibition

Bernstein does exactly ONE task per session. If the user asks for two things in one
prompt, Bernstein proposes splitting into two sessions.

---

## 6. Session Handout

Every session ends with Schubert producing a session handout. The handout captures:
- Current state (branch, head SHA, PR URL, Memtrace indexed SHA)
- Artifacts produced
- Pending work
- Keys for next session
- Known debt
- Rollback strategy

The next session reads the previous session's handout FIRST. It is the only context
that survives across sessions.

---

## 7. Quick Reference

| Situation | Action |
|---|---|
| Starting a task | Handoff → Ravel (if testable) → Producer → Phase 1 reviews (parallel) → Triage → Patches → Phase 2 reviews (sequential) → Triage → Patches → Ravel coverage → UAT → Schubert → PR → Handout → Session ends |
| Reviewer finding patched | Delta re-review with same reviewer |
| All phase tasks merged | Post-phase session → Maintenance phase |
| Next phase starting | Confirm post-phase report committed + maintenance complete |
| Decision clarification | Decision-only session, commit, terminate |
| Two tasks in one prompt | Propose splitting into two sessions |
| Subagent returns empty | Retry once → Bernstein does the work |
| Memtrace desync | HALT. Follow repair mode. No code changes. |
| PR opened | Session terminates. Next session reads handout. |
