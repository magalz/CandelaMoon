# Maestro Orchestrator Guide

> The operational manual for the orchestrator (the main session agent acting as Product Owner).
> It defines which agent to dispatch for each task type, how to create and manage handoff files,
> how to scope context per agent, and how to run the review pipeline.
>
> See companion documents:
> - **`maestro-workflow.md`** — 14-step task cycle and phase scaffolding (post-phase + maintenance).
> - **`maestro-conventions.md`** — JSON+MD output format, file naming, tag nomenclature, agent contracts.

---

## 1. Agent Dispatch Matrix

Map each task type to the correct agent and `subagent_type`. The full registry lives at
`.maestro-space/maestro-agents/agent-manifest.json`. The matrix below is the dispatch reference.

### Production Agents (receive handoff, update it)

| Task Type | Agent | subagent_type | Receives |
|---|---|---|---|
| Code implementation (Java/Android, Kotlin/Compose, C/C++/NDK) | Senior Developer | `senior-developer` | Handoff + TDD suite |
| TDD red-phase scaffold creation | QA Architect | `qa-architect` | Handoff + task spec + AC |
| Coverage audit + Memtrace reconciliation | QA Architect | `qa-architect` | Handoff + diff + test results |
| Containerfiles, CI workflows, runners | DevOps Architect | `devops-architect` | Handoff + toolchain-pins + ci-architecture |
| Threat model, supply chain, secrets policy | Security Analyst | `security-analyst` | Handoff + spec sections |
| ADR governance, compliance, waiver validation | GRC Architect | `grc-architect` | Handoff + ADR register + evidence manifests |
| Architecture docs, session handouts, post-phase consolidation | Tech Writer | `tech-writer` | Handoff + all task artifacts |
| Visual design, TV UX, accessibility, Compose eval | UX/UI Designer | `ux-ui-designer` | Handoff + design reference + spec |
| Post-phase analysis (4 roles) | grc / qa / security / devops architects | same as above | Whole-phase artifacts |
| Maintenance phase tasks (per task) | Production agent per dispatch matrix | per task type | Standard handoff |

### Review Agents (no handoff, need-to-know only)

| Review Role | subagent_type | Receives | Phase |
|---|---|---|---|
| Blind adversarial review | `blind-hunter` | Spec + diff + tests only | Phase 1 (parallel) |
| Edge case / boundary / deletion check | `edge-case-hunter` | Diff only | Phase 1 (parallel) |
| Acceptance criteria audit | `acceptance-analyst` | Spec + diff | Phase 1 (parallel) |
| Offensive security (STRIDE/OWASP) | `red-team-analyst` | Diff + spec context | Phase 2 (first) |
| Defensive security (mitigations) | `blue-team-analyst` | Red team findings + diff | Phase 2 (second, after red team) |

**Critical rule:** Review agents NEVER receive the handoff file, author rationale, or
conversation history. They review cold with need-to-know context only.

---

## 2. Handoff File Protocol

### 2.1 When to Create

The orchestrator creates a handoff file BEFORE dispatching any production agent. For a task
session, the file lives at:

```
.maestro-space/maestro-works/<phase>-<short-desc>/<task-id>-<short-desc>/handoff.md
```

Example: `.maestro-space/maestro-works/phase-1-delivery-system/p1-007-pr-template/handoff.md`

For post-phase session: `.maestro-space/maestro-works/<phase>-<short-desc>/post-phase-<phase>/<role>-report.md`

### 2.2 Handoff File Structure

The handoff file has YAML frontmatter conforming to `agent-output.schema.json` (canonical
JSON schema at `.maestro-space/maestro-templates/agent-output.schema.json`) plus a markdown
body. The required frontmatter shape for a task handoff is below; for post-phase
session handoffs, see `maestro-templates/post-phase-*.md`.

```yaml
---
change_id: "P1-007"
phase: "Phase 1"
task: "PR template with task/phase/capability/evidence fields"
status: "in-progress"        # in-progress | review | coverage-audit | uat | done | blocked
repository: "magalz/CandelaMoon"
branch: "phase1/p1-007-pr-template"
base_sha: "<40-char hex>"
head_sha: ""
pr_url: ""
acceptance_criteria:
  - "<testable, atomic criterion>"
  - "<testable, atomic criterion>"
tdd_artifacts:
  atdd_checklist: ".maestro-space/maestro-works/.../atdd-checklist.md"
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
  rating: ""                  # pass | conditional-pass | fail
  risk_weighted_score: 0
  memtrace_reconciliation: ""
  coverage_gaps: []
uat:
  status: "pending"           # pending | passed | failed
  user_decision: ""
documentation:
  tech_writer_artifacts: []
  session_handout: ".maestro-space/maestro-works/.../session-handout.md"
memtrace_repo_id: "CandelaMoon"
memtrace_indexed_sha: ""
memtrace_episode_ids: []
capability_rows: []
adrs: []                      # ["0015", "0017", ...]
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

# Task: <one-line task statement>

## Context
[Orchestrator provides: task description, spec section reference, plan task reference, relevant ADRs]

## Instructions for Agent
[Orchestrator provides: concrete steps from the implementation plan, file paths, acceptance criteria]

## Agent Output
[Agent fills: files created/modified, evidence, deviations, known issues]
```

### 2.3 How Agents Update the Handoff

Each production agent, after completing its work:
1. Updates the `implementation_artifacts` section with files created/modified
2. Sets `green_phase_verified` (for code tasks) or fills `files_created` (for doc tasks)
3. Updates `head_sha` with the current commit SHA
4. Fills the markdown body's "Agent Output" section
5. Notes any deviations from the plan or known issues
6. Also writes a parallel `*.json` activity report next to the handoff, conforming to
   `agent-output.schema.json` — this is the machine-parseable counterpart (Decision A: JSON+MD hybrid).

Review agents do NOT update the handoff. The orchestrator triages their findings and
writes them into `review_phase_1` or `review_phase_2` sections. Reviewer findings are
emitted as `findings-phase-N.json` + `findings-phase-N.md` files in the same task folder.

---

## 3. Context Scoping Rules

### Production Agents

Receive the full handoff file path and are instructed to read it. They also receive:
- The spec path and relevant section (e.g., `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md` §X)
- The plan path and relevant task
- The working directory path (the worktree)
- Any relevant ADR IDs
- The path to the activity report template (`.maestro-space/maestro-templates/agent-activity-report.md`)

### Review Agents

Receive ONLY:
- The diff (or instructions to run `git diff` in the worktree)
- The spec file path (for acceptance analyst and red team only)
- The acceptance criteria (for acceptance analyst only)
- Red team findings JSON (for blue team only)

They do NOT receive:
- The handoff file path
- Author rationale or conversation history
- The plan document
- ADR context
- Any indication of which agent did the work
- The session handout or post-phase reports

---

## 4. Review Pipeline Orchestration

### Phase 1: Parallel Adversarial Review

Dispatch three review agents IN PARALLEL (single message, three task calls). Each gets
the same diff but a different lens.

1. **Blind Hunter** (`subagent_type: "blind-hunter"`)
   - Prompt: "Read the diff at [worktree path]. Run `git diff [base]..[head]` to see changes.
     Find at least 10 issues. Return a numbered markdown list and a parallel findings JSON."

2. **Edge Case Hunter** (`subagent_type: "edge-case-hunter"`)
   - Prompt: "Read the diff at [worktree path]. Walk every branching path and boundary
     condition. Return a JSON array of findings (per `agent-output.schema.json`)
     and a parallel markdown narrative."

3. **Acceptance Analyst** (`subagent_type: "acceptance-analyst"`)
   - Prompt: "Read the spec at [spec path] section [section]. Read the diff at
     [worktree path]. Check for deviations from acceptance criteria. Return a markdown
     list of findings and a parallel findings JSON."

**If subagents return empty:** Retry once. If still empty, the orchestrator performs
the review directly with the same methodology, noting that the subagent was unavailable
in the handoff.

### Triage (Orchestrator)

After all Phase 1 reviews complete:
1. Normalize all findings into a common format (id, source, title, detail, location)
2. Deduplicate — merge findings describing the same issue
3. Read the code at each finding location to assess real consequence
4. Assign severity: low, medium, high
5. Route: **decision-needed** (ask user), **patch** (send to developer), **defer**
   (pre-existing or low-priority for follow-up), **dismiss** (noise / out-of-scope)
6. Write triaged findings into handoff `review_phase_1.triaged_findings`
7. If decision-needed findings exist, present to user before proceeding

### Phase 2: Sequential Security Review

Dispatch AFTER Phase 1 fixes are applied:

1. **Red Team** (`subagent_type: "red-team-analyst"`)
   - Prompt: "Review the diff at [worktree path] for exploitable security weaknesses.
     Walk the security checklist (STRIDE, OWASP). Return a JSON array of findings
     and a parallel markdown narrative."

2. Wait for Red Team to complete.

3. **Blue Team** (`subagent_type: "blue-team-analyst"`)
   - Prompt: "Here are red team findings: [paste JSON]. Review the diff at
     [worktree path]. Design concrete mitigations. Return a JSON array of
     mitigations and a parallel markdown narrative."

4. Triage security findings into handoff `review_phase_2.triaged_findings`.

### Delta-Only Re-Review (Optimization)

When the Senior Developer applies patches for a finding, the orchestrator may re-dispatch
the **same** reviewer (e.g., blind-hunter) with the **delta** (the specific fix) and
ask it to verify the patch addresses its original concern. To preserve reviewer context,
the orchestrator passes the original `task_id` so the reviewer session resumes its prior
context. This avoids re-running the entire 10+ issue review when the developer
addressed one specific point.

---

## 5. Subagent Dispatch Template

When dispatching a production agent:

```
subagent_type: "<agent-name from dispatch matrix>"

prompt: |
  You are working on the CandelaMoon project.
  
  Handoff file: <path to handoff .md file>
  Read it first. It contains your task, acceptance criteria, and context.
  
  Working directory: <worktree path>
  Spec: <spec path>, section <section number>
  Plan: <plan path>, Task <N>
  Relevant ADRs: <ADR IDs>
  
  Activity report template: .maestro-space/maestro-templates/agent-activity-report.md
  JSON schema: .maestro-space/maestro-templates/agent-output.schema.json
  
  After completing your work:
  1. Update the handoff file's implementation_artifacts section
  2. Set the status field
  3. Write a parallel <agent>-activity-report.md AND <agent>-activity-report.json
     in the same task folder. Both must conform to the activity-report template
     and the JSON schema respectively.
```

When dispatching a review agent:

```
subagent_type: "<review-agent-name>"

prompt: |
  Review the changes in <worktree path>.
  
  To see the diff, run: git diff <base_sha>..<head_sha>
  
  [For blind-hunter]: Find at least 10 issues. Return a numbered markdown list
  AND a parallel findings JSON conforming to agent-output.schema.json.
  [For edge-case-hunter]: Walk every branching path. Return a JSON array of
  findings and a parallel markdown narrative.
  [For acceptance-analyst]: Check against spec at <path> section <N>. Return
  a markdown list AND parallel JSON.
  [For red-team-analyst]: Walk the security checklist. Return a JSON array of
  findings and a parallel markdown narrative.
  [For blue-team-analyst]: Here are red team findings: <JSON>. Design mitigations.
  Return a JSON array of mitigations and a parallel markdown narrative.
  
  You do NOT have access to the handoff file, author rationale, or conversation history.
  Write your findings to <worktree path>/.maestro-space/maestro-works/<phase>/<task>/findings-<phase>.{json,md}.
```

---

## 6. Error Handling

### Subagent returns empty
Retry once. If still empty, orchestrator performs the review directly using the same
methodology, noting the subagent was unavailable in the handoff.

### Subagent crashes or times out
Record the failure in the handoff. Retry with a simpler prompt. If repeated failures,
orchestrator does the work directly.

### Memtrace/GitHub desynchronization
Halt all development. Follow the repair mode protocol from spec section 7.2 and ADR 0013.
No code changes until synchronization is restored.

### Memtrace MCP tools unavailable
Record in handoff. Proceed with manual evidence (git diff, file listing). Flag for
re-reconciliation when Memtrace is restored. Do NOT skip the coverage audit — use manual
methods instead.

### Reviewer context loss
If a delta-only re-review needs the original reviewer's prior context, the orchestrator
re-uses the original `task_id` from the previous dispatch so the reviewer session resumes.

---

## 7. Session Boundary (Hard Rule)

A **task session** ends when the PR is opened. The orchestrator MUST NOT continue work
in the same session after the PR is created. The next session (which may be a new task
session, a post-phase session, or a maintenance phase task) starts fresh, reads the
session handout, and proceeds from the recorded state.

This rule applies at every level:
- Task session ends → PR opened → session terminates.
- Post-phase session ends → 4 reports + summary + maintenance plan committed → session terminates.
- Maintenance phase task session ends → PR opened → session terminates.
