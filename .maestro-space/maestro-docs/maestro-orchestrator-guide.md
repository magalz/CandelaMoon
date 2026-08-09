# Maestro Orchestrator Guide

> The operational manual for Bernstein (the Principal Orchestrator). It defines which
> agent to dispatch for each task type, how to create and manage handoff files, how
> to scope context per agent, and how to run the review pipeline.
>
> See companion documents:
> - **`maestro-workflow.md`** — 14-step task cycle and phase scaffolding (post-phase + maintenance).
> - **`maestro-setup.md`** — rules for the phase setup session.
> - **`maestro-post-phase.md`** — rules for post-phase execution.
> - **`maestro-maintenance.md`** — rules for maintenance phase execution.
> - **`maestro-conventions.md`** — JSON+MD output format, file naming, tag nomenclature, agent contracts.

---

## 1. Agent Dispatch Matrix

### Production Agents

| Task Type | Agent | subagent_type | Receives |
|---|---|---|---|
| Code implementation | Bach (Senior Developer) | `bach-senior-developer` | Handoff + TDD suite |
| TDD red-phase scaffolds | Ravel (QA Architect) | `ravel-qa-architect` | Handoff + task spec + AC |
| Coverage audit + Memtrace reconciliation | Ravel (QA Architect) | `ravel-qa-architect` | Handoff + diff + test results |
| Container builds, CI, runners, signing | Vivaldi (DevOps Architect) | `vivaldi-devops-architect` | Handoff + toolchain pins + CI docs |
| Threat model, supply chain, secrets | Paganini (Security Analyst) | `paganini-security-analyst` | Handoff + spec sections |
| ADR governance, compliance, waivers | Haydn (GRC Architect) | `haydn-grc-architect` | Handoff + ADR register + evidence manifests |
| Documentation, session handouts | Schubert (Tech Writer) | `schubert-tech-writer` | Handoff + all task artifacts |
| Visual design, UX, accessibility | Debussy (UX/UI Designer) | `debussy-ux-ui-designer` | Handoff + design reference + spec |
| Post-phase analysis (4 roles) | Haydn / Ravel / Paganini / Vivaldi | same as above | Whole-phase artifacts |
| Maintenance phase tasks | Per dispatch matrix | per task type | Standard handoff |

### Review Agents

| Review Role | Agent | subagent_type | Receives | Phase |
|---|---|---|---|---|
| Blind adversarial review | Berlioz (Blind Hunter) | `berlioz-blind-hunter` | Spec + diff + tests | Phase 1 (parallel) |
| Edge case / boundary / deletion | Bartók (Edge Case Hunter) | `bartok-edge-case-hunter` | Diff only | Phase 1 (parallel) |
| Acceptance criteria audit | Verdi (Acceptance Analyst) | `verdi-acceptance-analyst` | Spec + diff | Phase 1 (parallel) |
| Offensive security (STRIDE/OWASP) | Stravinsky (Red Team) | `stravinsky-red-team-analyst` | Diff + spec context | Phase 2 (first) |
| Defensive security (mitigations) | Brahms (Blue Team) | `brahms-blue-team-analyst` | Red team findings + diff | Phase 2 (second) |

**Critical rule:** Review agents NEVER receive the handoff file, author rationale,
conversation history, the plan document, ADR context, or any indication of which
agent did the work. They review cold with need-to-know context only.

---

## 2. Handoff File Protocol

### 2.1 When to Create

Bernstein creates a handoff file BEFORE dispatching any production agent. For a task
session, the file lives in the task workspace folder. The exact path is determined
per session from the phase plan.

### 2.2 Handoff File Structure

The handoff file has YAML frontmatter conforming to the agent-output JSON schema
plus a markdown body.

```yaml
---
change_id: "P1-007"
phase: "Phase 1"
task: "<task description>"
status: "in-progress"
repository: "<org/repo>"
branch: "<task-branch>"
base_sha: "<40-char hex>"
head_sha: ""
pr_url: ""
acceptance_criteria:
  - "<testable, atomic criterion>"
tdd_artifacts:
  atdd_checklist: "<path>"
  test_files: []
  red_phase_verified: false
implementation_artifacts:
  files_created: []
  files_modified: []
  green_phase_verified: false
review_phase_1:
  blind_hunter_findings: []
  edge_case_hunter_findings: []
  acceptance_analyst_findings: []
  triaged_findings: []
  fixes_applied: false
review_phase_2:
  red_team_findings: []
  blue_team_findings: []
  triaged_findings: []
  fixes_applied: false
coverage_audit:
  rating: ""
  risk_weighted_score: 0
  memtrace_reconciliation: ""
  coverage_gaps: []
uat:
  status: "pending"
  user_decision: ""
documentation:
  tech_writer_artifacts: []
  session_handout: "<path>"
verification:
  tests_pass: false
  memtrace_review: false
  acceptance_audit: false
  edge_case_hunt: false
  blind_hunt: false
  security_review: false
  policy_check: false
known_debt: []
rollback_strategy: ""
---
```

### 2.3 How Agents Update the Handoff

Each production agent, after completing its work:
1. Updates the `implementation_artifacts` section with files created/modified
2. Sets `green_phase_verified` (for code tasks) or fills `files_created` (for doc tasks)
3. Updates `head_sha` with the current commit SHA
4. Fills the markdown body's "Agent Output" section
5. Notes any deviations from the plan or known issues
6. Also writes a parallel JSON activity report (Decision A: JSON+MD hybrid).

Review agents do NOT update the handoff. Bernstein triages their findings and
writes them into `review_phase_1` or `review_phase_2` sections.

---

## 3. Context Scoping Rules

### Production Agents

Receive the full handoff file path and are instructed to read it. They also receive:
- The spec path and relevant section from `/docs/`
- The plan path and relevant task
- The working directory path
- Any relevant ADR IDs
- The path to the activity report template

### Review Agents

Receive ONLY:
- The diff (or instructions to run `git diff` in the worktree)
- The spec file path (for Verdi and Stravinsky only)
- The acceptance criteria (for Verdi only)
- Stravinsky's findings JSON (for Brahms only)

They do NOT receive: the handoff, author rationale, conversation history, the plan,
ADRs, or any indication of which agent did the work.

---

## 4. Review Pipeline

### Phase 1: Parallel

Dispatch Berlioz, Bartók, and Verdi IN PARALLEL. Each gets the same diff but a
different lens. If a subagent returns empty, retry once. If still empty, Bernstein
performs the review directly.

### Triage

Bernstein normalizes, deduplicates, assesses severity (low/medium/high), and routes:
**decision-needed** → ask user; **patch** → send to Bach; **defer** → known debt;
**dismiss** → noise / out-of-scope.

### Phase 2: Sequential

1. Dispatch Stravinsky (Red Team). Wait for completion.
2. Dispatch Brahms (Blue Team) with Stravinsky's findings as input.
3. Bernstein triages security findings.

### Delta-Only Re-Review

When Bach applies patches, Bernstein may re-dispatch the same reviewer with only the
delta, using the original `task_id` to resume reviewer context.

---

## 5. Subagent Dispatch Template

When dispatching a production agent:

```
subagent_type: "<agent-name from dispatch matrix>"

prompt: |
  Handoff file: <path to handoff .md file>
  Read it first. It contains your task, acceptance criteria, and context.
  
  Working directory: <worktree path>
  Spec: <spec path>, section <section number>
  Plan: <plan path>, Task <N>
  Relevant ADRs: <ADR IDs>
  
  Your agent identity and full operating rules are defined in your agent file.
  Read it to understand your role, contract, and deliverables.
  
  Activity report template: <template path>
  JSON schema: <schema path>
  
  After completing your work:
  1. Update the handoff file's implementation_artifacts section
  2. Set the status field
  3. Write a parallel activity report (JSON + MD) in the task folder.
```

When dispatching a review agent:

```
subagent_type: "<review-agent-name>"

prompt: |
  Review the changes in <worktree path>.
  To see the diff, run: git diff <base_sha>..<head_sha>
  
  [Agent-specific instructions here]
  
  Your agent identity and full operating rules are defined in your agent file.
  
  You do NOT have access to the handoff file, author rationale, or conversation history.
  Write your findings to the task folder as findings-phase-<N>.{json,md}.
```

---

## 6. Session Start Protocols

### 6.1 Phase Setup Session

When starting a new phase, Bernstein follows `maestro-setup.md`:
1. Read the global objectives and roadmap
2. Read external `/docs/` context (spec, plans, ADRs, infrastructure)
3. Create the phase folder and plan
4. Create individual task files
5. Create the phase workspace directory
6. Update the roadmap
7. Produce the setup handout → session ends

### 6.2 Task Session (Standard)

When continuing an in-progress phase, Bernstein:
1. Reads this guide
2. Reads the session handout from the previous task session
3. Checks git status, open PRs, CI state
4. Sweeps handoffs for `status: in-progress` — resumes them first
5. Checks Memtrace freshness against HEAD
6. Reports the plan to the user → dispatches per the task

### 6.3 Post-Phase Session

When all phase tasks are complete, Bernstein follows `maestro-post-phase.md`.

### 6.4 Maintenance Phase Session

After the post-phase session, Bernstein follows `maestro-maintenance.md`.

---

## 7. Error Handling

- **Subagent returns empty**: Retry once. If still empty, Bernstein performs the review directly.
- **Subagent crashes**: Record in handoff. Retry with simpler prompt. Fall back to direct work.
- **Memtrace desync**: HALT all development. Follow repair mode protocol. No code changes until restored.
- **Reviewer context loss**: Re-use the original `task_id` from the previous dispatch.

---

## 8. Phase Completion Sequence

Bernstein tracks phase progress continuously through the phase plan:

```
1. Setup Session → Phase plan created, all tasks: Pending
2. Task Sessions (N) → Task status: Pending → In Development → Completed
3. All Tasks Completed → Trigger Post-Phase
4. Post-Phase Complete → Trigger Maintenance Phase
5. Maintenance Complete → Phase marked Completed → Next Phase may begin
```

### 8.1 Continuous Tracking (End of Every Session)

Bernstein MUST update:
1. **Individual task file**: Add Session History row (date, status, head SHA, PR URL, handoff path).
2. **Phase plan**: Update task status in the Phase Tasks table.
3. **Session handout**: Schubert produces this. Bernstein verifies it exists.

### 8.2 Session Adjustments

Decisions made during a session that affect future tasks must be propagated:
1. **Dependency changes**: Update downstream task files and the phase plan.
2. **Scope changes**: Update task description and affected downstream tasks.
3. **New tasks**: Append with next available P-ID. Do not renumber existing tasks.
4. **Deferred findings**: Record as `known_debt`. Review at post-phase time.
   For every finding routed `defer` during triage with severity `high` or `medium`,
   Bernstein MUST create a GitHub issue per §8.2.1 below. `low` severity deferrals
   may be created at Bernstein's discretion or deferred entirely.
5. **ADR decisions**: Reference in the task file and notify downstream tasks.

### 8.2.1 GitHub Issue Creation from Deferred Findings

After each task session's review triage (steps 5 and 8 of the task cycle), Bernstein
creates GitHub issues for deferred findings. The issues serve as the durable, tracked
backlog that survives across sessions and is visible to the human owner.

**When to create an issue:**

| Finding severity | Finding type | Action |
|---|---|---|
| `high` | Any (deferred, tech-debt, secops) | **MUST** create a GitHub issue |
| `medium` | Any | **MUST** create a GitHub issue |
| `low` | Any | Bernstein's discretion; may skip |

**Issue templates and labels:**

| Finding origin | Template file | Title prefix | GitHub labels |
|---|---|---|---|
| Review Phase 1/2 — deferred (non-security, non-architectural) | `maestro-templates/issue-deferred.md` | `[Deferred.P{N}.NN]` | `Deferred` + severity label (`High` / `Medium` / `Low`) |
| Review Phase 1/2 — architectural or cross-cutting concern | `maestro-templates/issue-tech-debt.md` | `[Tech Debt.P{N}.NN]` | `Tech Debt` + severity label |
| Review Phase 2 — security finding (STR-xxx) | `maestro-templates/issue-secops.md` | `[SecOps.P{N}.NN]` | `SecOps` + severity label |

**Numbering**: `NN` is a sequential counter within the phase, shared across all issue
types. Gaps are tolerated. Bernstein tracks the next available `NN` in the phase plan.

**Issue content**: Each issue follows its template and is self-contained — an
individual agent in a new context can pick it up with no additional conversation
history. The issue body MUST reference the source task (P-ID), the source findings
file, and the relevant finding IDs.

**Recording**: After creation, Bernstein records the GitHub issue URL in the
relevant `known_debt` entry and in the session handout's Known Debt table.

**Scope**: This applies to findings deferred during task sessions only. The
post-phase session (§5 of `maestro-post-phase.md`) produces maintenance tasks
from whole-phase analysis; those follow a separate numbering scheme (`M{N}-NNN`).

Before dispatching, Bernstein checks:
- The phase plan for the next `Pending` task.
- No `In Development` task exists (one task at a time).
- The next task's dependencies are all `Completed`.
- If a dependency is not `Completed`: HALT. Report to user.

---

## 9. Session Boundary (Hard Rule)

A task session ends when the PR is opened. Bernstein MUST NOT continue work
in the same session after the PR is created. The next session starts fresh,
reads the session handout, and proceeds from the recorded state.

---

## 10. Paths

The only hardcoded external path is `/docs/` for project documentation.
All other paths (workspace, templates, handoffs, agent files) are acquired
per session from the phase plan, session handout, or orchestrator configuration.
