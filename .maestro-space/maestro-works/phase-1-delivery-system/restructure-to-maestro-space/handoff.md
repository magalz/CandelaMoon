---
change_id: "RESTRUCTURE-2026-08-08"
phase: "Phase 1"
task: "Restructure documentation to tracked .maestro-space/ framework (full reconciliation)"
status: "in-progress"
repository: "magalz/CandelaMoon"
branch: "docs/restructure-to-maestro-space"
base_sha: "53659407e185a4629bf9654a14f0f39b2c5c38c0"
head_sha: "855591f8"
pr_url: "https://github.com/magalz/CandelaMoon/pull/8"
acceptance_criteria:
  - "All framework files moved from docs/{handoffs,audits,infrastructure} to .maestro-space/maestro-{works,plans,docs}/"
  - ".maestro-space/ tree created with index.md, .gitignore, maestro-docs (3 files), maestro-plans (5 files including master-roadmap), maestro-templates (17 files), maestro-agents (1 file), maestro-secrets marker, maestro-works starter"
  - "Master roadmap created at .maestro-space/maestro-plans/master-roadmap.md (distilled from spec §11)"
  - "Phase 0 backlog retrofitted at .maestro-space/maestro-plans/phase-0-delivery-system-backlog.md"
  - "Phase 2 stub created at .maestro-space/maestro-plans/phase-2-repositories-and-baselines-backlog.md"
  - "P1-021 handoff/atdd-checklist/session-handout/coverage-audit + JSON companions moved to .maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/"
  - "Phase 0 session-handout moved to .maestro-space/maestro-works/phase-0-delivery-system/post-phase-0/session-handout.md"
  - "All references in spec, plan, ADRs 0013/0015-0020, README, CONTRIBUTING, PR template, delivery-system-design, phase0-audit reconciled to new locations"
  - ".gitignore updated: .maestro-space/ exclusion removed (framework is now tracked); .maestro-space/maestro-secrets/ is the only ignored part (handled by .maestro-space/.gitignore)"
  - "scripts/validate_design.py updated to look at the new maestro location for the implementation backlog"
  - "python scripts/validate_design.py --strict passes 48/48"
  - "PR opened as bot via open-pr-bot.yml; awaiting @magalz review and merge"
tdd_artifacts:
  atdd_checklist: ""
  test_files: []
  red_phase_verified: false
  notes: "Docs-only restructure; no testable behavior. Bootstrap exception per maestro-workflow.md §2."
implementation_artifacts:
  files_created:
    - ".maestro-space/.gitignore"
    - ".maestro-space/index.md"
    - ".maestro-space/maestro-agents/agent-manifest.json"
    - ".maestro-space/maestro-docs/maestro-conventions.md"
    - ".maestro-space/maestro-docs/maestro-orchestrator-guide.md"
    - ".maestro-space/maestro-docs/maestro-workflow.md"
    - ".maestro-space/maestro-plans/global-objectives.md"
    - ".maestro-space/maestro-plans/master-roadmap.md"
    - ".maestro-space/maestro-plans/phase-0-delivery-system-backlog.md"
    - ".maestro-space/maestro-plans/phase-2-repositories-and-baselines-backlog.md"
    - ".maestro-space/maestro-secrets/.gitkeep"
    - ".maestro-space/maestro-templates/agent-activity-report.md"
    - ".maestro-space/maestro-templates/agent-findings-report.md"
    - ".maestro-space/maestro-templates/agent-output.schema.json"
    - ".maestro-space/maestro-templates/atdd-checklist.md"
    - ".maestro-space/maestro-templates/coverage-audit.md"
    - ".maestro-space/maestro-templates/handoff.md"
    - ".maestro-space/maestro-templates/issue-deferred.md"
    - ".maestro-space/maestro-templates/issue-secops.md"
    - ".maestro-space/maestro-templates/issue-tech-debt.md"
    - ".maestro-space/maestro-templates/maintenance-phase-plan.md"
    - ".maestro-space/maestro-templates/post-phase-devops.md"
    - ".maestro-space/maestro-templates/post-phase-grc.md"
    - ".maestro-space/maestro-templates/post-phase-qa.md"
    - ".maestro-space/maestro-templates/post-phase-security.md"
    - ".maestro-space/maestro-templates/post-phase-summary.md"
    - ".maestro-space/maestro-templates/pr.md"
    - ".maestro-space/maestro-templates/session-handout.md"
    - ".maestro-space/maestro-works/.gitkeep"
    - ".maestro-space/maestro-works/phase-0-delivery-system/post-phase-0/session-handout.md"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/atdd-checklist.json"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/atdd-checklist.md"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/coverage-audit.json"
    - ".maestro-space/maetro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/coverage-audit.md"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/handoff.json"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/handoff.md"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/session-handout.json"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/session-handout.md"
    - ".maestro-space/maestro-works/phase-1-delivery-system/restructure-to-maestro-space/session-handout.md"
    - ".github/PULL_REQUEST_TEMPLATE.md"
    - "scripts/maestro-bootstrap.ps1"
  files_modified:
    - ".github/CONTRIBUTING.md"
    - ".gitignore"
    - "README.md"
    - "docs/adr/0013-github-memtrace-split-authority.md"
    - "docs/adr/0015-multi-agent-architecture.md"
    - "docs/adr/0016-atdd-red-phase-before-implementation.md"
    - "docs/adr/0017-two-phase-adversarial-review.md"
    - "docs/adr/0018-red-blue-team-security-review.md"
    - "docs/adr/0019-coverage-audit-with-memtrace.md"
    - "docs/adr/0020-session-handout-for-context-continuity.md"
    - "docs/infrastructure/delivery-system-design.md"
    - "docs/infrastructure/phase0-audit.md"
    - "docs/superpowers/plans/2026-08-05-phase0-delivery-system-design.md"
    - "docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md"
    - "scripts/validate_design.py"
  files_deleted:
    - "android_test_setup.md"
    - "docs/infrastructure/orchestrator-guide.md"
  files_renamed:
    - "docs/infrastructure/implementation-backlog.md -> .maestro-space/maestro-plans/phase-1-delivery-system-backlog.md"
    - "docs/infrastructure/session-handout-phase0.md -> .maestro-space/maestro-works/phase-0-delivery-system/post-phase-0/session-handout.md"
    - "android_test_setup.md -> docs/infrastructure/legacy/android-test-setup.md"
  green_phase_verified: true
  green_phase_evidence: "python scripts/validate_design.py --strict: 48 passed, 0 failed (no testable behavior; validator is the documentation test)"
review_phase_1:
  blind_hunter_findings: []
  edge_case_hunter_findings: []
  acceptance_analyst_findings: []
  triaged_findings: []
  fixes_applied: false
  notes: "Bootstrap exception (docs-only task): Review Phase 1 may be performed by user during PR review."
review_phase_2:
  red_team_findings: []
  blue_team_findings: []
  triaged_findings: []
  fixes_applied: false
  notes: "Bootstrap exception: Review Phase 2 may be performed by user during PR review."
coverage_audit:
  rating: "pass"
  risk_weighted_score: 0
  memtrace_reconciliation: "Not applicable for this docs-only restructure; Memtrace index will be reconciled after PR merge (see session-handout.md RESTR-003). The graph content is unchanged (no source-code symbol changes), so the impact is limited to false-positive 'undocumented change' flags for the modified .md files in review_github_pr."
  coverage_gaps: []
uat:
  status: "pending"
  user_decision: "Not applicable (docs-only); user decision is the PR review/approval."
documentation:
  tech_writer_artifacts:
    - ".maestro-space/maestro-works/phase-1-delivery-system/restructure-to-maestro-space/session-handout.md"
  session_handout: ".maestro-space/maestro-works/phase-1-delivery-system/restructure-to-maestro-space/session-handout.md"
memtrace_repo_id: "CandelaMoon"
memtrace_indexed_sha: ""
memtrace_episode_ids: []
capability_rows: []
adrs:
  - "0013"
  - "0015"
  - "0016"
  - "0017"
  - "0018"
  - "0019"
  - "0020"
verification:
  tests_pass: true
  memtrace_review: false
  acceptance_audit: true
  edge_case_hunt: false
  blind_hunt: false
  security_review: false
  policy_check: true
  notes: "tests_pass = validator PASS; memtrace_review/edge_case_hunt/blind_hunt/security_review are pending PR review by @magalz; acceptance_audit and policy_check are passed (all references reconcile; PR opened by the bot workflow). Final transition to status: done is gated on PR merge."
known_debt:
  - "RESTR-001: PR #8 body has minor PowerShell escape character artifacts (cosmetic)."
  - "RESTR-002: P1-021 agent reports and findings-*.{json,md} not included (not findable in prior session artifacts)."
  - "RESTR-003: Memtrace index is on pre-restructure HEAD; reconcile after PR merge."
  - "RESTR-004: P1-021 branch has uncommitted .gitignore modification that adds .maestro-space/; redundant after this restructure merges."
  - "RESTR-005: .github/workflows/create-pr.yml untracked on main worktree (out of scope)."
  - "RESTR-006: .opencode/, opencode.json, .worktrees/ untracked on main worktree (out of scope)."
rollback_strategy: "Close PR #8 and delete the docs/restructure-to-maestro-space branch before merge. After merge, revert the merge commit on moonlight-noir, re-add .maestro-space/ to .gitignore, and re-create the legacy docs/infrastructure/orchestrator-guide.md (its content is preserved in the pre-PR commits)."
---

# Task: Restructure documentation to tracked .maestro-space/ framework

## Context

The user observed that the new `.maestro-space/` workflow structure was created
(PR #7, `interphase/maestro-space-bootstrap`) but the documentation was not
fully aligned to it. Framework files (orchestrator guide, handoffs, audits,
session handouts) were still tracked under `docs/{infrastructure,handoffs,audits}/`,
and the `.maestro-space/` itself was gitignored (per the original "per-fork,
local-only" design). The user directed: "we will remove .maestro-space from the
gitignore ... and have all in the remote" — i.e., make the framework tracked so
it can be reviewed, branched, and merged normally. They also asked for the
**master plan** to be created from the original superpowers plan (spec §11),
transformed into the phase/task structure under `.maestro-space/maestro-plans/`.

This is a **full reconciliation**: every framework file is moved to its
authoritative location, all references reconcile, and the framework becomes
the single source of truth for "how the framework orchestrates the work."

## Instructions for Agent

This handoff records the executed task. The task is complete; the PR is open
and awaiting user review. No further work is required from subagents.

## Agent Output

### Orchestrator (Product Owner) — Restructure (2026-08-08)

**Phase**: A through H (per the planned sequence).

**Execution summary**:
- **Phase A** (framework creation): copied `.maestro-space/` from the bootstrap worktree
  (interphase/maestro-space-bootstrap) into the new worktree at
  `C:\Users\magal\AppData\Local\Temp\opencode\candelamoon-restructure`. Created
  `.maestro-space/.gitignore` (excludes only `maestro-secrets/*`).
- **Phase B** (docs/ reorganization): deleted `docs/infrastructure/orchestrator-guide.md`,
  moved implementation-backlog.md → `.maestro-space/maestro-plans/phase-1-delivery-system-backlog.md`,
  moved session-handout-phase0.md → `.maestro-space/maestro-works/phase-0-delivery-system/post-phase-0/session-handout.md`,
  moved p1-021 handoffs/audit (already in the new location from the bootstrap
  worktree). Moved `android_test_setup.md` → `docs/infrastructure/legacy/`.
- **Phase C** (master roadmap + phase backlogs): created
  `.maestro-space/maestro-plans/master-roadmap.md` (program-wide guide from spec
  §11), `.maestro-space/maestro-plans/phase-0-delivery-system-backlog.md`
  (retrofitted), `.maestro-space/maestro-plans/phase-2-repositories-and-baselines-backlog.md`
  (stub).
- **Phase D** (template adaptation): updated path references in p1-021
  handoff/atdd-checklist/session-handout/coverage-audit; added JSON companions
  (handoff.json, atdd-checklist.json, coverage-audit.json, session-handout.json)
  per maestro-conventions §1; adapted phase-0 session-handout to the new
  template format (added Completed Evidence, UAT Decision, PR Status sections).
- **Phase E** (reference reconciliation): added `## Framework reference` sections
  to ADRs 0013, 0015-0020; added post-restructure notes to spec §15, the plan,
  phase0-audit.md, and the README; updated CONTRIBUTING.md; created
  `.github/PULL_REQUEST_TEMPLATE.md` referencing `.maestro-space/maestro-templates/pr.md`;
  corrected delivery-system-design.md references.
- **Phase F** (validation): updated `scripts/validate_design.py` to look at the
  new maestro location for the Phase 1 implementation backlog; ran
  `python scripts/validate_design.py --strict` → 48 passed, 0 failed.
- **Phase G** (PR): committed all changes (commit `855591f8`, 58 files,
  7153 insertions, 2752 deletions); pushed branch `docs/restructure-to-maestro-space`
  to origin; triggered `open-pr-bot.yml` workflow (run `31235029292`, succeeded);
  PR #8 created in DRAFT state by `candelamoon-bot` at
  https://github.com/magalz/CandelaMoon/pull/8.
- **Phase H** (this handout): created session-handout.md (and this handoff.md)
  at `.maestro-space/maestro-works/phase-1-delivery-system/restructure-to-maestro-space/`.

**Deviations from plan**: none material. The PR body has minor PowerShell
escape character artifacts (RESTR-001) due to PowerShell's escaping in the
`gh workflow run` body parameter — the markdown renders correctly despite
the backslash artifacts. This is cosmetic; the PR is fully readable and
actionable.

**Known issues**: see `known_debt` in frontmatter and in session-handout.md.

**Handoff to**: `@magalz` for PR review and merge. After merge, the next
session's expected first action is to begin P1-001 (the next pending Phase 1
work item per `.maestro-space/maestro-plans/phase-1-delivery-system-backlog.md`).
The P1-001 handoff goes at `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android/`.
