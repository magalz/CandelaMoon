<!--
  PR template for the CandelaMoon project.
  The framework template is at .maestro-space/maestro-templates/pr.md (used by the
  candelamoon-bot when it opens the PR). This file is the GitHub-side surface that
  references it.
-->

## <task-id>: <one-line task statement>

**Phase**: <Phase N>
**Branch**: `<task branch>` → `moonlight-noir`
**Task ID**: `<task-id>`
**Related ADRs**: `<id list>`

---

## Summary

<One paragraph: what this PR does and why.>

## Acceptance criteria

- [ ] <AC #1: testable criterion>
- [ ] <AC #2: testable criterion>
- [ ] <AC #N: testable criterion>

## Evidence

Reference the framework-side artifacts for full evidence:

- **Handoff**: `.maestro-space/maestro-works/<phase>/<task>/handoff.md`
- **ATDD checklist**: `.maestro-space/maestro-works/<phase>/<task>/atdd-checklist.md`
- **Coverage audit**: `.maestro-space/maestro-works/<phase>/<task>/coverage-audit.md` (ADR 0019)
- **Session handout**: `.maestro-space/maestro-works/<phase>/<task>/session-handout.md` (ADR 0020)

### Review stack (per `.maestro-space/maestro-docs/maestro-orchestrator-guide.md` §4)

- [ ] **Phase 1** — Blind Hunter, Edge Case Hunter, Acceptance Analyst (parallel, no handoff)
- [ ] **Phase 2** — Red Team then Blue Team (sequential security review)
- [ ] **Triage** — all triaged findings addressed or recorded as known debt
- [ ] **Coverage audit** — `rating: pass` (ADR 0019)
- [ ] **UAT** — user decision recorded in handoff

## Rollback

<One paragraph: how to roll back this PR if needed.>

## References

- Spec: `docs/superpowers/specs/<spec>.md` §<N>
- Plan: `docs/superpowers/plans/<plan>.md` Task <N>
- Framework: `.maestro-space/index.md` (the entry point for the orchestration framework)

---

🤖 Opened by `candelamoon-bot` via the orchestrator. **Approval required from @magalz before merge.** Memtrace `review_github_pr` is run by the orchestrator as part of step 13 of the per-task 14-step cycle.
