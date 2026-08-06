# Orchestrator Guide

This document is the operational manual for the orchestrator (the main session agent acting as Product Owner). It defines which agent to dispatch for each task type, how to create and manage handoff files, how to scope context per agent, and how to run the review pipeline.

Reference: spec section 15 (Agent Architecture And Task Workflow).

---

## 1. Agent Dispatch Matrix

Map each task type to the correct agent and `subagent_type`:

### Production Agents (receive handoff, update it)

| Task Type | Agent | subagent_type | Receives |
|---|---|---|---|
| Code implementation (Java/Android) | Senior Developer | `senior-developer` | Handoff + TDD suite |
| Code implementation (Kotlin/Compose) | Senior Developer | `senior-developer` | Handoff + TDD suite |
| Code implementation (C/C++/NDK) | Senior Developer | `senior-developer` | Handoff + TDD suite |
| TDD red-phase scaffold creation | QA Architect | `qa-architect` | Handoff + task spec + AC |
| Coverage audit + Memtrace reconciliation | QA Architect | `qa-architect` | Handoff + diff + test results |
| Containerfiles, CI workflows, runners | DevOps Architect | `devops-architect` | Handoff + toolchain-pins + ci-architecture |
| Threat model, supply chain, secrets policy | Security Analyst | `security-analyst` | Handoff + spec sections |
| ADR governance, compliance, waiver validation | GRC Architect | `grc-architect` | Handoff + ADR register + evidence manifests |
| Architecture docs, session handouts, DESIGN.md | Tech Writer | `tech-writer` | Handoff + all task artifacts |
| Visual design, TV UX, accessibility, Compose eval | UX/UI Designer | `ux-ui-designer` | Handoff + design reference + spec |

### Review Agents (no handoff, need-to-know only)

| Review Role | subagent_type | Receives | Phase |
|---|---|---|---|
| Blind adversarial review | `blind-hunter` | Spec + diff + tests only | Phase 1 (parallel) |
| Edge case / boundary / deletion check | `edge-case-hunter` | Diff only | Phase 1 (parallel) |
| Acceptance criteria audit | `acceptance-analyst` | Spec + diff | Phase 1 (parallel) |
| Offensive security (STRIDE/OWASP) | `red-team-analyst` | Diff + spec context | Phase 2 (first) |
| Defensive security (mitigations) | `blue-team-analyst` | Red team findings + diff | Phase 2 (second, after red team) |

**Critical rule:** Review agents NEVER receive the handoff file, author rationale, or conversation history. They review cold with need-to-know context only.

---

## 2. Handoff File Protocol

### 2.1 When to Create

The orchestrator creates a handoff file BEFORE dispatching any production agent. The file lives at:

```
docs/handoffs/<phase>-<task-id>-handoff.md
```

Example: `docs/handoffs/phase0-t1-schemas-handoff.md`

### 2.2 Handoff File Structure

The handoff file has YAML frontmatter conforming to `evidence-manifest.schema.json` plus a markdown body:

```yaml
---
change_id: "P0-T1"
phase: "Phase 0"
task: "Machine-Readable Schemas"
status: "in-progress"
repository: "magalz/CandelaMoon"
branch: "docs/phase0-t1-schemas"
base_sha: "3397ec77"
head_sha: ""
pr_url: ""
acceptance_criteria:
  - "4 JSON Schema files created (ADR, evidence manifest, capability row, device matrix)"
  - "All schemas valid JSON Schema draft 2020-12"
  - "Validator confirms schemas pass"
tdd_artifacts:
  atdd_checklist: ""
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
  session_handout: ""
memtrace_repo_id: "CandelaMoon"
memtrace_indexed_sha: ""
memtrace_episode_ids: []
capability_rows: []
adrs: []
verification:
  tests_pass: false
  memtrace_review: false
  acceptance_audit: false
  edge_case_hunt: false
  blind_hunt: false
  security_review: false
  policy_check: false
known_debt: []
rollback_strategy: "Clean revert of the task branch"
---

# Task: Machine-Readable Schemas

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

Review agents do NOT update the handoff. The orchestrator triages their findings and writes them into `review_phase_1` or `review_phase_2` sections.

---

## 3. Context Scoping Rules

### Production Agents
Receive the full handoff file path and are instructed to read it. They also receive:
- The spec path and relevant section
- The plan path and relevant task
- The working directory path
- Any relevant ADR IDs

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

---

## 4. Review Pipeline Orchestration

### Phase 1: Parallel Adversarial Review

Dispatch three review agents IN PARALLEL (single message, three task calls):

1. **Blind Hunter** (`subagent_type: "blind-hunter"`)
   - Prompt: "Read the diff at [worktree path]. Run `git diff [base]..[head]` to see changes. Find at least 10 issues. Return a numbered markdown list."

2. **Edge Case Hunter** (`subagent_type: "edge-case-hunter"`)
   - Prompt: "Read the diff at [worktree path]. Walk every branching path and boundary condition. Return a JSON array of findings."

3. **Acceptance Analyst** (`subagent_type: "acceptance-analyst"`)
   - Prompt: "Read the spec at [spec path] section [section]. Read the diff at [worktree path]. Check for deviations from acceptance criteria. Return a markdown list of findings."

**If subagents return empty:** Retry once. If still empty, the orchestrator performs the review directly with the same methodology, noting that the subagent was unavailable.

### Triage (Orchestrator)

After all Phase 1 reviews complete:
1. Normalize all findings into a common format (id, source, title, detail, location)
2. Deduplicate — merge findings describing the same issue
3. Read the code at each finding location to assess real consequence
4. Assign severity: low, medium, high
5. Route: decision-needed (ask user), patch (send to developer), defer (pre-existing), dismiss (noise)
6. Write triaged findings into handoff `review_phase_1.triaged_findings`
7. If decision-needed findings exist, present to user before proceeding

### Phase 2: Sequential Security Review

Dispatch AFTER Phase 1 fixes are applied:

1. **Red Team** (`subagent_type: "red-team-analyst"`)
   - Prompt: "Review the diff at [worktree path] for exploitable security weaknesses. Walk the security checklist (STRIDE, OWASP). Return a JSON array."

2. Wait for Red Team to complete.

3. **Blue Team** (`subagent_type: "blue-team-analyst"`)
   - Prompt: "Here are red team findings: [paste JSON]. Review the diff at [worktree path]. Design concrete mitigations. Return a JSON array."

4. Triage security findings into handoff `review_phase_2.triaged_findings`

---

## 5. Task Execution Flow

For each leaf task in a phase:

```
1. Orchestrator creates handoff file
2. IF task has testable behavior:
   - Dispatch QA Architect (subagent_type: "qa-architect") with handoff
   - QA Architect creates TDD red-phase scaffolds, updates handoff
3. Dispatch appropriate production agent (see dispatch matrix) with handoff
   - Agent implements, updates handoff with artifacts + green-phase evidence
4. Dispatch Review Phase 1 (parallel: blind-hunter, edge-case-hunter, acceptance-analyst)
   - Each gets need-to-know context only, no handoff
5. Orchestrator triages Phase 1 findings into handoff
6. IF patches needed: dispatch production agent again with triaged findings
7. Dispatch Review Phase 2 (sequential: red-team-analyst, then blue-team-analyst)
8. Orchestrator triages Phase 2 findings into handoff
9. IF patches needed: dispatch production agent again with security findings
10. IF task has testable behavior:
    - Dispatch QA Architect for coverage audit with Memtrace reconciliation
    - QA Architect rates: pass / conditional-pass / fail
    - IF fail: back to step 3 with coverage tasks
11. IF UAT applicable: present to user for testing
12. Dispatch Tech Writer (subagent_type: "tech-writer") with handoff
    - Tech Writer documents, creates session handout, updates handoff
13. Orchestrator opens PR (or updates existing phase-audit PR)
    - Run Memtrace review_github_pr against the synchronized graph
14. Tech Writer creates session handout at docs/handoffs/<phase>-session-handout.md
```

### Bootstrap Exception

For documentation-only tasks (no testable behavior):
- Skip steps 2 and 10 (TDD and coverage audit)
- Still run Review Phases 1-2, Tech Writer, and PR creation
- The validator script is the "test" for documentation completeness

---

## 6. Phase Audit Protocol

At the end of every phase:

1. Run `python scripts/validate_design.py --strict` — must pass
2. Verify all task handoffs are complete (status: done)
3. Verify all evidence manifests have verification fields set
4. Verify no unresolved critical/high findings remain
5. Write phase audit document at `docs/infrastructure/phaseN-audit.md`
6. Push branch and create/update phase-audit PR
7. Tech Writer creates session handout at `docs/infrastructure/session-handout-phaseN.md`
8. Memtrace index verified against GitHub merge SHA

---

## 7. Subagent Dispatch Template

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
  
  After completing your work, update the handoff file's implementation_artifacts
  section with files created/modified and set the status field.
```

When dispatching a review agent:

```
subagent_type: "<review-agent-name>"

prompt: |
  Review the changes in <worktree path>.
  
  To see the diff, run: git diff <base_sha>..<head_sha>
  
  [For blind-hunter]: Find at least 10 issues. Return a numbered markdown list.
  [For edge-case-hunter]: Walk every branching path. Return a JSON array.
  [For acceptance-analyst]: Check against spec at <path> section <N>. Return a markdown list.
  [For red-team-analyst]: Walk the security checklist. Return a JSON array.
  [For blue-team-analyst]: Here are red team findings: <JSON>. Design mitigations. Return a JSON array.
  
  You do NOT have access to the handoff file, author rationale, or conversation history.
```

---

## 8. Error Handling

### Subagent returns empty
Retry once. If still empty, orchestrator performs the review directly using the same methodology, noting the subagent was unavailable in the handoff.

### Subagent crashes or times out
Record the failure in the handoff. Retry with a simpler prompt. If repeated failures, orchestrator does the work directly.

### Memtrace/GitHub desynchronization
Halt all development. Follow the repair mode protocol from spec section 7.2 and ADR 0013. No code changes until synchronization is restored.

### Memtrace MCP tools unavailable
Record in handoff. Proceed with manual evidence (git diff, file listing). Flag for re-reconciliation when Memtrace is restored. Do NOT skip the coverage audit — use manual methods instead.
