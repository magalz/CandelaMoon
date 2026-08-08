# Handoff Template

> The single source of truth for a task's state. YAML frontmatter conforms to the
> `evidence-manifest` shape (see `docs/schema/evidence-manifest.schema.json`); the
> markdown body is the agent-facing context and the human narrative.

The companion JSON file is `handoff.json`, which mirrors the frontmatter and is the
machine-parseable form. See `agent-output.schema.json` `artifact_type: handoff`.

**File location**: `.maestro-space/maestro-works/<phase-short-desc>/<task-id>-<short-desc>/handoff.md`

---

```yaml
---
change_id: "<P- or M- ID, e.g., P1-007>"
phase: "Phase N"
task: "<one-line task statement>"
status: "in-progress"           # in-progress | review | coverage-audit | uat | done | blocked
  repository: "<org/repo>"
branch: "<task branch>"
base_sha: "<40-char hex>"
head_sha: ""                    # updated as work progresses
pr_url: ""                      # filled at step 13
acceptance_criteria:
  - "<testable, atomic criterion>"
  - "<testable, atomic criterion>"
tdd_artifacts:
  atdd_checklist: ".maestro-space/maestro-works/<phase>/<task>/atdd-checklist.md"
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
  rating: ""                    # pass | conditional-pass | fail
  risk_weighted_score: 0
  memtrace_reconciliation: ""
  coverage_gaps: []
uat:
  status: "pending"             # pending | passed | failed
  user_decision: ""
documentation:
  tech_writer_artifacts: []
  session_handout: ".maestro-space/maestro-works/<phase>/<task>/session-handout.md"
  memtrace_repo_id: "<repo-id>"
memtrace_indexed_sha: ""
memtrace_episode_ids: []
capability_rows: []
adrs: []                        # ["0014", "0015", ...]
verification:
  tests_pass: false
  memtrace_review: false
  acceptance_audit: false
  edge_case_hunt: false
  blind_hunt: false
  security_review: false
  policy_check: false
known_debt: []
rollback_strategy: "<one-line rollback strategy>"
---

# Task: <one-line task statement>

## Context

[Bernstein provides: task description, spec section reference, plan task reference,
relevant ADRs. Link to:
- Spec: `/docs/superpowers/specs/<spec>.md` §X
- Plan: `/docs/superpowers/plans/<plan>.md` Task N
- ADRs: `/docs/adr/<NNNN>-<short>.md`]

## Instructions for Agent

[Bernstein provides: concrete steps from the implementation plan, file paths, acceptance
criteria. Include the production-agent dispatch template from
`maestro-docs/maestro-orchestrator-guide.md` §5 with placeholders filled in.]

## Agent Output

### <Agent Name> — <Phase> (<date>)

[Each agent fills its section. Sections are added in the order agents run: QA Architect
(red phase), Senior Developer (implementation + green), QA Architect (coverage audit),
Tech Writer (documentation), and any review-triage sections for fix cycles.]

#### Environment

[Execution boundary, container, host, key tools, version pins.]

#### Actions

[Numbered list of concrete actions. Reference files by path.]

#### Files

- Created: [list]
- Modified: [list]

#### Verification

[Commands run, expected output, observed output. Reference logs by path.]

#### Deviations

[Anything done that wasn't in the plan, with justification.]

#### Known Issues

[Anything observed that isn't actionable in this task but is worth recording.]

#### Handoff to

[The next agent in the pipeline. State the next concrete step.]
```
