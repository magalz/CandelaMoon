# Session Handout — Restructure to tracked `.maestro-space/`

**Date**: 2026-08-08
**Task**: Restructure — bring the `.maestro-space/` framework into the tracked tree and align all documentation to the new locations.
**ADR**: 0020 (Session Handout for Context Continuity)
**Spec**: `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md` §15 (Agent Architecture And Task Workflow)

---

## Current State

- **Branch**: `docs/restructure-to-maestro-space`
- **Head SHA**: `855591f8` (this commit)
- **Base SHA**: `53659407` (`Merge pull request #5 from magalz/fix/bot-pr-quoting`)
- **PR URL**: https://github.com/magalz/CandelaMoon/pull/8
- **PR state**: DRAFT (awaiting `@magalz` review/approval)
- **PR author**: `candelamoon-bot`
- **PR title**: `docs(maestro-space): restructure to tracked .maestro-space/ framework (full reconciliation)`
- **Memtrace repo_id**: `CandelaMoon` (index will be reconciled after merge; current graph is on the pre-restructure source)
- **Handoff status**: in-progress (PR created; awaiting approval and merge before transitioning to `done`)
- **UAT decision**: not applicable (documentation-only restructure)

## Completed Evidence (this task)

| Gate | Result | Evidence |
|---|---|---|
| Phase A (framework creation) | `.maestro-space/` tree created with index.md, .gitignore, maestro-docs, maestro-plans, maestro-templates, maestro-agents, maestro-secrets, maestro-works | this commit |
| Phase B (docs/ reorganization) | orchestrator-guide deleted; implementation-backlog, session-handout-phase0, p1-021 handoffs/audit moved | this commit (renamed in git history) |
| Phase C (master roadmap + phase 2+ plans) | master-roadmap.md, phase-0-delivery-system-backlog.md, phase-2-repositories-and-baselines-backlog.md created | this commit |
| Phase D (template adaptation) | p1-021 handoff/atdd-checklist/session-handout/coverage-audit + JSON companions created; phase-0 session-handout adapted to new template | this commit |
| Phase E (reference reconciliation) | spec §15, plan post-restructure note, ADRs 0013/0015-0020, README, CONTRIBUTING, PULL_REQUEST_TEMPLATE, delivery-system-design, phase0-audit, .gitignore all updated | this commit |
| Phase F (validation) | `python scripts/validate_design.py --strict` → 48 passed, 0 failed | validator output (this commit) |
| Phase G (PR opened) | `open-pr-bot.yml` workflow dispatch run `31235029292` → PR #8 created in DRAFT state | GitHub Actions run + `gh pr view 8` |
| Phase H (this handout) | session-handout.md created at `.maestro-space/maestro-works/phase-1-delivery-system/restructure-to-maestro-space/` | this file |

## Artifacts Produced (this task)

| Path | Description |
|---|---|
| `.maestro-space/` (root) | NEW tracked framework directory. 25 new files. |
| `.maestro-space/index.md` | Framework entry point |
| `.maestro-space/.gitignore` | Excludes only `maestro-secrets/*` (defensive marker) |
| `.maestro-space/maestro-docs/maestro-{orchestrator-guide,workflow,conventions}.md` | 3 framework reference docs (operationalize spec §15) |
| `.maestro-space/maestro-plans/global-objectives.md` | North star for the program |
| `.maestro-space/maestro-plans/master-roadmap.md` | **NEW** — the program-wide roadmap distilled from spec §11 (Phase 0–12) |
| `.maestro-space/maestro-plans/phase-0-delivery-system-backlog.md` | **NEW** — retrofitted Phase 0 with framework note (DONE) |
| `.maestro-space/maestro-plans/phase-1-delivery-system-backlog.md` | RENAMED from `docs/infrastructure/implementation-backlog.md` (preserves 100% content; framework notes added) |
| `.maestro-space/maestro-plans/phase-2-repositories-and-baselines-backlog.md` | **NEW** — Phase 2 stub with 6 indicative task groups |
| `.maestro-space/maestro-templates/*` | 17 templates: agent-output.schema.json + 16 MD templates (handoff, atdd-checklist, coverage-audit, session-handout, post-phase-{grc,qa,security,devops,summary}, maintenance-phase-plan, issue-{deferred,tech-debt,secops}, pr, agent-activity-report, agent-findings-report) |
| `.maestro-space/maestro-agents/agent-manifest.json` | Agent registry mapping logical names to subagent_type (7 production + 5 review) |
| `.maestro-space/maestro-secrets/.gitkeep` | Defensive marker for the always-ignored secrets dir |
| `.maestro-space/maestro-works/phase-0-delivery-system/post-phase-0/session-handout.md` | MOVED from `docs/infrastructure/session-handout-phase0.md`; adapted to new template format (added Completed Evidence, UAT Decision, PR Status sections) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/handoff.{md,json}` | MOVED from `docs/handoffs/phase1-p1-021-...-handoff.md`; path references updated; JSON companion added |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/atdd-checklist.{md,json}` | MOVED + JSON companion added |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/coverage-audit.{md,json}` | MOVED + JSON companion added |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/session-handout.{md,json}` | MOVED + JSON companion added |
| `scripts/maestro-bootstrap.ps1` | NEW — the bootstrap mechanism that creates the `.maestro-space/` skeleton on fresh clones |
| `.github/PULL_REQUEST_TEMPLATE.md` | NEW — references `.maestro-space/maestro-templates/pr.md` |
| `docs/infrastructure/legacy/android-test-setup.md` | MOVED from `android_test_setup.md` (root) |
| `README.md` | MODIFIED — added `## CandelaMoon` section pointing to `.maestro-space/` |
| `.github/CONTRIBUTING.md` | MODIFIED — added `## CandelaMoon Development Workflow` section |
| `docs/adr/0013, 0015, 0016, 0017, 0018, 0019, 0020` | MODIFIED — each gets a `## Framework reference` section pointing to the relevant `.maestro-space/` doc |
| `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md` | MODIFIED — post-restructure note appended to §15 |
| `docs/superpowers/plans/2026-08-05-phase0-delivery-system-design.md` | MODIFIED — post-restructure note appended at end |
| `docs/infrastructure/delivery-system-design.md` | MODIFIED — corrected `orchestrator-guide.md` references to `.maestro-space/maestro-docs/maestro-orchestrator-guide.md` |
| `docs/infrastructure/phase0-audit.md` | MODIFIED — post-restructure reference appended |
| `.gitignore` | MODIFIED — removed `.maestro-space/` line; framework is now tracked; `maestro-secrets/*` exclusion is handled by `.maestro-space/.gitignore` |
| `scripts/validate_design.py` | MODIFIED — added fallback to look at the new maestro location for `phase-1-delivery-system-backlog.md` |

## Pending Work

1. **`@magalz` review/approval of PR #8** — the restructure is in DRAFT state. The validator passes (48/48), all paths resolve, all references reconcile. Approve and merge to `moonlight-noir`.
2. **After merge — reconcile the Memtrace graph** — the pre-restructure index is still on `53659407`. After merge, run a Memtrace reindex of `moonlight-noir` at the new head (merge commit) so subsequent `review_github_pr` calls and coverage audits have a current graph.
3. **After merge — begin P1-001** — the next pending Phase 1 work item is `candelamoon-android` Containerfile (P1-001). See `.maestro-space/maestro-plans/phase-1-delivery-system-backlog.md`. The handoff goes at `.maestro-space/maestro-works/phase-1-delivery-system/p1-001-candelamoon-android/`. This is the first task to fully exercise the tracked framework.
4. **After merge — open the first session handout at the canonical location** — when the first post-merge task starts, its session handout goes at `.maestro-space/maestro-works/<phase>/<task>/session-handout.md` (per the template). The P1-001 session handout is the proof-of-life for the tracked framework.

## Keys For Next Session

- **Handoff file**: `.maestro-space/maestro-works/phase-1-delivery-system/restructure-to-maestro-space/handoff.md` (this session's task; created in the same commit; to be updated when the task transitions to `done` after PR merge)
- **Handoff status**: in-progress (per ADR 0020 — only `done` after PR merge + UAT pass; this is a docs-only task, so UAT is not applicable; `done` is reached on PR merge)
- **Spec**: `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md` (§15 Agent Architecture And Task Workflow; post-restructure note appended)
- **Plan**: `docs/superpowers/plans/2026-08-05-phase0-delivery-system-design.md` (post-restructure note appended)
- **ADR register**: `docs/adr/` (21 ADRs: 0000 template + 0001-0020). Framework ADRs (0013, 0015-0020) each have a `## Framework reference` section pointing to the relevant `.maestro-space/` doc
- **Master roadmap**: `.maestro-space/maestro-plans/master-roadmap.md` (the program-wide guide distilled from spec §11; identifies next pending work at any time)
- **Per-phase backlogs**:
  - `.maestro-space/maestro-plans/phase-0-delivery-system-backlog.md` (DONE)
  - `.maestro-space/maestro-plans/phase-1-delivery-system-backlog.md` (IN PROGRESS, 1/21 done; P1-001 next)
  - `.maestro-space/maestro-plans/phase-2-repositories-and-baselines-backlog.md` (PENDING — stub; decompose at start of Phase 2)
- **Framework entry point**: `.maestro-space/index.md`
- **Orchestrator guide**: `.maestro-space/maestro-docs/maestro-orchestrator-guide.md`
- **Workflow**: `.maestro-space/maestro-docs/maestro-workflow.md`
- **Conventions**: `.maestro-space/maestro-docs/maestro-conventions.md`
- **Agent registry**: `.maestro-space/maestro-agents/agent-manifest.json`
- **Templates**: `.maestro-space/maestro-templates/` (17 files)
- **Validator**: `scripts/validate_design.py` (run with `--strict`) → 48/48 PASS
- **Bootstrap script**: `scripts/maestro-bootstrap.ps1` (creates the `.maestro-space/` skeleton on fresh clones)
- **OpenCode agents (for activation)**: `.opencode/agents/*.md` (12 agents — `.opencode/agents/` is NOT gitignored; the `.maestro-space/maestro-agents/agent-manifest.json` is the framework-side registry, not a copy of the agent .md files)
- **Worktree**: `C:\Users\magal\AppData\Local\Temp\opencode\candelamoon-restructure` on branch `docs/restructure-to-maestro-space`
- **Main repo**: `D:\Repos\CandelaMoon` on branch `phase1/p1-021-baseline-test-fixes` (P1-021 already merged to moonlight-noir as PR #6; the in-progress P1-021 branch has uncommitted .gitignore modifications that are no longer needed after this restructure merges)
- **PR #8**: https://github.com/magalz/CandelaMoon/pull/8 (DRAFT, awaiting review)
- **Workflow run that opened PR #8**: `31235029292` (succeeded)
- **CI run for PR #8**: `31235020238` (in progress at the time of this handout)

## Known Debt

| ID | Item | Severity | Resolution |
|---|---|---|---|
| RESTR-001 | PR #8 body has minor PowerShell escape character artifacts (backticks rendered as `\.` in some places due to PowerShell's escaping in the `gh workflow run` body parameter) | low (cosmetic) | Re-author the PR body via `gh pr edit` (raw API) if @magalz flags it; the markdown renders correctly despite the backslash artifacts |
| RESTR-002 | Agent reports and `findings-*.{json,md}` files for P1-021 are NOT included in this restructure (not findable in the prior session artifacts) | low | Future P-tasks will emit the full JSON+MD hybrid set per maestro-conventions §1; P1-021's gap is documented in the master roadmap and phase-1 backlog as historical debt |
| RESTR-003 | The pre-restructure Memtrace index is still on the pre-restructure HEAD (`53659407`). A reindex is needed after this PR merges | medium | Run the Memtrace reindex against the merge commit on `moonlight-noir`. Until then, `review_github_pr` on PR #8 will report against the stale graph. The graph content is unchanged (this is a docs-only restructure with no source-code symbol changes), so the impact is limited to false-positive "undocumented change" flags for the modified `.md` files |
| RESTR-004 | The P1-021 branch (`phase1/p1-021-baseline-test-fixes`) has uncommitted `.gitignore` modifications that added `.maestro-space/`. After this restructure merges, those modifications are no longer needed (the new `.gitignore` has the line removed) | low | The user can `git checkout .gitignore` on the P1-021 branch to drop the modification; or it can be left as a no-op (the added line is now redundant but harmless) |
| RESTR-005 | The `.github/workflows/create-pr.yml` file is untracked on the main worktree (was a prior in-progress untracked file) | low | Out of scope for this restructure; can be committed in a follow-up PR if needed |
| RESTR-006 | The `.opencode/`, `opencode.json`, and `.worktrees/` items in the main worktree's untracked state are out of scope for this restructure (they were pre-existing uncommitted changes on `phase1/p1-021-baseline-test-fixes`) | low | Commit or discard in a follow-up |

## UAT Decision

- **Status**: not applicable
- **User decision**: documentation-only restructure; no user-facing behavior to test
- **Rationale**: validator PASS (48/48), all path references reconcile, JSON schemas validate, no source-code changes. The "user" review is `@magalz`'s PR review and merge approval.

## PR Status

- **PR URL**: https://github.com/magalz/CandelaMoon/pull/8
- **Status**: DRAFT
- **Author**: `app/candelamoon-bot`
- **Title**: `docs(maestro-space): restructure to tracked .maestro-space/ framework (full reconciliation)`
- **Base branch**: `moonlight-noir`
- **Head branch**: `docs/restructure-to-maestro-space`
- **Head SHA**: `855591f8`
- **Workflow run that opened it**: `31235029292` (succeeded)
- **CI run**: `31235020238` (in progress at the time of this handout)
- **Memtrace GitHub PR review**: not yet run (orchestrator step 13 — runs after PR creation; gated on `@magalz` review and merge)

## Rollback Strategy

1. **If the PR is not yet merged**: close PR #8 and delete the `docs/restructure-to-maestro-space` branch. The `moonlight-noir` base branch is untouched. The pre-restructure state (with the legacy `docs/infrastructure/orchestrator-guide.md`, `docs/handoffs/`, `docs/audits/`, and `.maestro-space/` gitignored) is preserved.
2. **If the PR is merged and the framework rollout causes unforeseen issues**: revert the merge commit on `moonlight-noir` (`git revert -m 1 <merge-sha>`), re-add `.maestro-space/` to the root `.gitignore` (defensive), and re-create the legacy `docs/infrastructure/orchestrator-guide.md` (its content is preserved in the pre-PR commits).
3. **Files affected (this restructure)**: 58 files (7153 insertions, 2752 deletions). The deletions are concentrated in: the legacy orchestrator-guide.md (323 lines), the legacy implementation-backlog.md (131 lines, restored at the new location), the legacy session-handout-phase0.md (102 lines, restored at the new location), and the legacy android_test_setup.md (270 lines, restored under `legacy/`).
4. **Documentation rollback**: revert the spec/plan post-restructure notes, the ADR `## Framework reference` sections, the README/CONTRIBUTING/PR template additions, and the `.gitignore` change.
