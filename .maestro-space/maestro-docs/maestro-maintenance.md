# Maestro Maintenance

> The rules, definitions, and directives for the maintenance phase. After the post-phase
> session produces the maintenance plan, Bernstein executes the maintenance phase — a
> regular phase with its own task sessions, each following the standard cycle. The
> maintenance phase is the buffer between phases.
>
> See companion documents:
> - **`maestro-workflow.md`** — task cycle and phase scaffolding.
> - **`maestro-setup.md`** — rules for the phase setup session.
> - **`maestro-post-phase.md`** — rules for post-phase execution.
> - **`maestro-orchestrator-guide.md`** — dispatch matrix, handoff protocol, review pipeline.

---

## 1. What Is the Maintenance Phase

The maintenance phase is a regular phase with its own backlog (the maintenance plan
produced by the post-phase session). It runs the standard per-task cycle for each
maintenance task. Tasks use `M{N}-NNN` IDs.

```
Phase N Complete
  │
  ├─ Post-Phase Session ─► Maintenance Plan (M{N}-NNN tasks)
  │
  ├─ Maintenance Phase
  │     ├─ M{N}-001 ─► Cycle ─► PR ─► session ends
  │     ├─ M{N}-002 ─► Cycle ─► PR ─► session ends
  │     └─ M{N}-NNN ─► Cycle ─► PR ─► session ends
  │                                   │
  │                          All M-tasks complete?
  │                                   │
  │                            ┌──────┴──────┐
  │                            │ YES         │ NO
  │                            ▼             ▼
  │                 Phase Complete    Continue M-tasks
  │                            │
  └────────────────────────────┘
                               │
                               ▼
                       Phase N+1 Setup
```

---

## 2. Maintenance Phase Lifecycle

### 2.1 Initiation

The maintenance phase begins immediately after the post-phase session completes.
Bernstein does NOT run a setup session — the maintenance plan IS the setup artifact.

### 2.2 Execution

Each maintenance task follows the standard cycle (maestro-workflow.md §2):
1. Bernstein creates the task handoff
2. (If testable) Ravel creates TDD scaffolds
3. Production agent implements
4-5. Phase 1 review (Berlioz, Bartók, Verdi) + triage
6. Patches if needed
7-8. Phase 2 security review (Stravinsky → Brahms) + triage
9. Patches if needed
10. (If testable) Ravel coverage audit
11. UAT (if applicable)
12. Schubert documentation
13. PR opened
14. Session handout → session ends

### 2.3 Tracking

Maintenance tasks are tracked in the maintenance plan document. Status transitions:
`Pending` → `In Development` → `Completed`. Bernstein updates the plan at the end of
each maintenance session.

### 2.4 Completion

The maintenance phase is complete when ALL maintenance tasks are `Completed`.
There is NO post-phase or maintenance-of-maintenance cycle. Once all M-tasks are
done, the phase boundary is clean and Phase N+1 may begin.

---

## 3. Maintenance Task Categories

| Category | Source | Example |
|---|---|---|
| Governance | Haydn (GRC) | "Create waiver for undocumented decision" |
| Quality | Ravel (QA) | "Rewrite flaky tests" |
| Security | Paganini (Security) | "Patch CVE in dependency" |
| Infrastructure | Vivaldi (DevOps) | "Rotate stale token" |
| Documentation | Any architect | "Backfill missing evidence manifests" |
| Process | Any architect | "Update stale toolchain pins" |

---

## 4. Maintenance Task File Structure

Each maintenance task has a task file with:

```markdown
# <Task ID>: <Title>

**Phase**: Maintenance M{N}
**Status**: Pending | In Development | Completed
**Source**: <architect report>
**Source Finding**: <finding ID>
**Severity**: low | medium | high | critical
**Dependencies**: <list or "none">
**Complexity**: S | M | L
**Related ADRs**: <IDs>

## Description
<What this maintenance task fixes.>

## Acceptance Criteria
- <testable criterion>

## Implementation Notes
<Guidance from the architect report.>

## Evidence Requirements
- <what proves the maintenance is effective>

## Session History
| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
```

---

## 5. Priority Rules

Maintenance tasks execute in priority order:
1. **Critical** (BLOCKING for Phase N+1) — first
2. **High** — second
3. **Medium** — third
4. **Low** — may be deferred to Phase N+1

Within the same severity, execute by dependency order then by M-ID.

---

## 6. Skip Rules

A maintenance task MAY be skipped only if:
- The user explicitly approves (decision recorded in the plan).
- It is severity `low` and does not block Phase N+1.
- The skip reason is documented.

MUST NOT be skipped if:
- Severity `critical` or `high`.
- It blocks Phase N+1 setup.
- The architect report flagged it as "must-fix."

---

## 7. Hard Rules

1. **No setup session for maintenance**: the post-phase handout IS the setup artifact.
2. **Standard cycle**: every M-task follows the full cycle. No shortcuts.
3. **One M-task = one session = one PR**.
4. **No maintenance-of-maintenance**: the maintenance phase is the terminal cleanup.
5. **Phase N+1 is blocked until M-tasks complete**.

---

## 8. Quick Reference

| Situation | Action |
|---|---|
| Post-phase session complete | Begin first M-task immediately |
| M-task is docs-only | Bootstrap exception: skip TDD + coverage audit |
| M-task needs implementation | Full cycle with production agent |
| User wants to skip M-task | Only if low severity + user approved + documented |
| All M-tasks complete | Produce completion handout (template: `maestro-templates/maintenance-completion-handout.md`) → Phase N+1 Setup |
| Critical M-task fails | Do not proceed to Phase N+1. Fix and re-run. |
| Maintenance plan empty | State "No maintenance tasks required" → Phase N+1 may proceed |
