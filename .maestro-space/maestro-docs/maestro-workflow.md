# Maestro Workflow

> How work moves through the system. Defines the per-task 14-step cycle, the per-phase
> scaffolding (post-phase session + maintenance phase), and the blocking rules between phases.
>
> See companion documents:
> - **`maestro-orchestrator-guide.md`** — dispatch matrix, handoff protocol, review pipeline.
> - **`maestro-conventions.md`** — JSON+MD output format, file naming, tag nomenclature, agent contracts.

---

## 1. Mental Model

```
Phase N
  ├─ Task 1   ─► 14-step cycle ─► PR #1 ─► session ends
  ├─ Task 2   ─► 14-step cycle ─► PR #2 ─► session ends
  ├─ ...
  └─ Task N   ─► 14-step cycle ─► PR #N ─► session ends
                                          │
                                          ▼
                            ┌─ POST-PHASE SESSION ─┐
                            │ Orchestrator + 4     │
                            │ architects analyze   │
                            │ the whole phase      │
                            │ (4 reports + summary │
                            │  + maintenance plan) │
                            └──────────┬────────────┘
                                       │
                                       ▼
                            ┌─ MAINTENANCE PHASE ──┐
                            │ N tasks (each one is  │
                            │ its own 14-step cycle,│
                            │ 1 task = 1 session    │
                            │ = 1 PR).              │
                            │ Fixes the issues that │
                            │ would block Phase N+1 │
                            └──────────┬────────────┘
                                       │
                                       ▼
                                  Phase N+1
```

**One task = one session = one PR.** That is the rigid rule. The orchestrator works on
exactly one task per session and terminates the session when the PR is opened.

**One phase = N task sessions + one post-phase session + one maintenance phase.**
The post-phase session and the maintenance phase are themselves discrete sessions with
their own handoffs and PRs (or commits, in the case of the post-phase report).

---

## 2. Per-Task 14-Step Cycle

This is the spec section 15.2 pipeline, operationalized for `.maestro-space/`. Every leaf
task in a phase flows through these 14 steps.

```
 1. Orchestrator creates the task handoff at
    .maestro-space/maestro-works/<phase>/<task-id>-<short-desc>/handoff.md
    Acceptance criteria populated. Evidence manifest initialized.

 2. IF task has testable behavior:
    Dispatch QA Architect (subagent_type: "qa-architect") with handoff
    QA Architect creates TDD red-phase scaffolds and writes:
    - atdd-checklist.md
    - the failing tests
    - sets tdd_artifacts.red_phase_verified = true
    Updates the handoff.

 3. Dispatch the appropriate production agent (see dispatch matrix) with handoff
    Agent implements, runs tests red→green, refactors while green.
    Updates the handoff with implementation_artifacts + green_phase_verified.
    Writes <agent>-activity-report.md + .json alongside the handoff.

 4. Dispatch Review Phase 1 in PARALLEL (single message, 3 task calls):
    - blind-hunter
    - edge-case-hunter
    - acceptance-analyst
    Each writes findings-phase-1.json + .md to the task folder.
    Each gets need-to-know context only (no handoff).

 5. Orchestrator triages Phase 1 findings into review_phase_1.triaged_findings
    Normalize, dedupe, assign severity, route (patch / defer / dismiss / decision-needed).
    If decision-needed findings exist → present to user.

 6. IF patches needed: dispatch the production agent again with the triaged findings.
    Optionally include a delta-only re-review by the same reviewer (see orchestrator-guide
    §4 Delta-Only Re-Review).

 7. Dispatch Review Phase 2 SEQUENTIALLY:
    First red-team-analyst. Then blue-team-analyst (with red team findings as input).
    Each writes findings-phase-2.json + .md to the task folder.

 8. Orchestrator triages Phase 2 findings into review_phase_2.triaged_findings.

 9. IF patches needed: dispatch the production agent again with security findings.
    Then optionally delta-only re-review.

10. IF task has testable behavior:
    Dispatch QA Architect for coverage audit with Memtrace reconciliation.
    QA writes coverage-audit.md in the task folder.
    QA rates: pass / conditional-pass / fail.
    IF fail: back to step 3 with coverage tasks.

11. IF UAT applicable: present to user for testing. Mark uat.status.

12. Dispatch Tech Writer (subagent_type: "tech-writer") with handoff.
    Tech Writer documents, finalizes the activity report, and prepares session handout.

13. Orchestrator opens the PR.
    Use .github/workflows/open-pr-bot.yml (the bot opens the PR as candelamoon-bot[bot]).
    Run Memtrace review_github_pr against the synchronized graph.
    Update handoff: pr_url, head_sha, status = "uat" (after PR opens) or "done" (after UAT passes).

14. Tech Writer creates session handout at
    .maestro-space/maestro-works/<phase>/<task-id>-<short-desc>/session-handout.md
    This is the continuity document for the next session.

    SESSION ENDS. Hard rule: no further work in this session.
```

### Bootstrap Exception (Documentation-Only Tasks)

For documentation-only tasks (no testable behavior):
- Skip steps 2 and 10 (TDD and coverage audit)
- Still run Review Phases 1-2, Tech Writer, and PR creation
- The validator script (e.g., `python scripts/validate_design.py --strict`) is the "test"
  for documentation completeness

---

## 3. Phase Scaffolding

### 3.1 Pre-Phase Readiness

Before Phase N begins, the orchestrator runs a thin readiness check:
- Are all open issues from the previous phase resolved or explicitly deferred?
- Is the previous phase's post-phase report committed?
- Is the previous phase's maintenance phase complete?
- Are any **Critical** findings unaddressed in the current branch?

If any answer is no → HALT, warn the user, request explicit confirmation before continuing.

### 3.2 Phase Execution

Phase N runs N task sessions, each following the 14-step cycle. PRs accumulate on the
phase branch (or each task gets its own branch and is merged individually — depends on
the phase's branch strategy recorded in the backlog).

### 3.3 Post-Phase Session (MANDATORY, BLOCKING)

After the last task of Phase N is merged, a **post-phase session** runs. This is a
distinct session — not a task — and its outputs are committed (not PR'd; they are
documents).

**Participants**: orchestrator + 4 architects, dispatched in sequence or two parallel pairs:
1. **grc-architect** — governance compliance, ADR alignment, waivers outstanding, evidence-manifest gaps
2. **qa-architect** — coverage trends, test debt, flakiness, untested paths, Memtrace drift
3. **security-analyst** — security debt, threat-model drift, dependency freshness, signing key health
4. **devops-architect** — CI debt, pipeline health, runner utilization, container/image staleness

**Outputs** (committed to the phase branch and to local `.maestro-space/maestro-works/<phase>/post-phase-N/`):
- `grc-report.md` + `.json`
- `qa-report.md` + `.json`
- `security-report.md` + `.json`
- `devops-report.md` + `.json`
- `summary.md` (orchestrator-synthesized; same shape as a normal handoff's Agent Output)
- `maintenance-phase-plan.md` — the list of tasks to run in the maintenance phase

**Templates** for each: `.maestro-space/maestro-templates/post-phase-{grc,qa,security,devops,summary}.md`

**HARD RULE**: The post-phase session is **BLOCKING** for Phase N+1. Phase N+1 cannot
begin until the post-phase session is complete and its outputs are committed. No
exceptions. If the post-phase session is skipped, every subsequent phase is operating
on un-tracked technical debt.

### 3.4 Maintenance Phase

The maintenance phase is a **regular phase** with its own backlog (the maintenance plan
produced by the post-phase session). It runs the standard per-task 14-step cycle for
each maintenance task.

**Goal**: fix the issues that would otherwise degrade or block Phase N+1.

**Examples** of maintenance tasks (illustrative, not exhaustive):
- "rotate stale GHA token surfaced by grc-architect"
- "rewrite 3 flaky tests flagged by qa-architect"
- "patch CVE in gradle wrapper flagged by security-analyst"
- "rebuild stale `candelamoon-android` image flagged by devops-architect"
- "create waiver for undocumented decision surfaced by grc-architect"
- "backfill missing evidence manifests for the phase"

**Naming**: maintenance tasks use `MN-NNN` IDs (where N matches the phase they precede;
M for "maintenance"). For example, after Phase 1, the maintenance phase is M1-001,
M1-002, etc. (not P2-001; that comes after M1 is complete).

### 3.5 Phase Boundary Recap

```
Phase N
  ├─ N task sessions (each 14-step, each 1 PR)
  ├─ 1 post-phase session (4 architects, no PR, all reports committed)
  └─ 1 maintenance phase (M1-XXX tasks, each 14-step, each 1 PR)
       │
       ▼
Phase N+1
```

The post-phase session is the gate. Maintenance is the buffer. Phase N+1 starts fresh.

---

## 4. Decision-Only Sessions (not a task, not a phase)

Sometimes the orchestrator needs to clarify a design decision with the user. This is a
short session that:
- Reads current state
- Surfaces the decision options
- Awaits user input
- Commits the decision (typically as an ADR or as a section of an existing doc)
- Terminates

Decision-only sessions are NOT a 14-step cycle, NOT a task, NOT a phase. They are
orchestrator-only sessions, typically <5 turns. They are recorded in the session
handout of the next regular session as "decisions taken during interphase work."

---

## 5. Multi-Tasking Prohibition

The orchestrator does **exactly one** task per session. A session is never:
- Two tasks in sequence (split into two sessions)
- A task plus a post-phase session (split into two sessions)
- A task plus a maintenance task (split into two sessions)

If the user asks for two things in one prompt, the orchestrator proposes splitting into
two sessions, with the second session's handoff pre-populated by the first session's
session handout.

---

## 6. Session Handout (continuity artifact)

Every session ends with the Tech Writer producing a `session-handout.md` in the task
folder. The handout captures:
- Current state (branch, head SHA, PR URL, Memtrace indexed SHA)
- Artifacts produced (file paths, descriptions)
- Pending work (next task description, dependencies)
- Keys for next session (handoff path, spec path, ADR register, evidence manifest, test artifacts)
- Known debt (deferred or incomplete items)
- Rollback strategy

The next session reads the previous session's handout FIRST. It is the only context
that survives across sessions (conversation history does not).

Templates:
- `.maestro-space/maestro-templates/session-handout.md`

---

## 7. Quick Reference

| Situation | Action |
|---|---|
| Starting a task | Create handoff → dispatch QA (if testable) → dispatch producer → Phase 1 review (parallel) → triage → patches → Phase 2 review (sequential) → triage → patches → coverage audit → UAT → Tech Writer → PR → session handout → session ends |
| Reviewer finding is patched | Re-dispatch the same reviewer with the delta (same `task_id` to resume context) |
| All phase tasks merged | Post-phase session (4 architects) → commit all outputs → maintenance phase |
| Next phase starting | Confirm post-phase report is committed + maintenance phase is complete |
| User asks for a clarification | Decision-only session, commit decision, terminate |
| User asks for two tasks in one prompt | Propose splitting into two sessions |
| Subagent returns empty | Retry once → if still empty, orchestrator does the work |
| Memtrace desync | HALT. Follow ADR 0013 / spec §7.2 repair mode. No code changes. |
| PR opened | Session terminates. Next session reads the handout. |
