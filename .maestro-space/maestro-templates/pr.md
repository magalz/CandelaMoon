# Pull Request Template

> The standard PR description used for every task PR. The orchestrator (via the bot
> workflow) populates the placeholders. This is the markdown body that goes into
> the PR description; the GitHub-side template at `.github/PULL_REQUEST_TEMPLATE.md`
> should reference this file.

---

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

### Test results

| Phase | Command | Result | Log |
|---|---|---|---|
| Red (ADR 0016) | `<gradle command>` | <N> tests, <M> failed (predicted) | `<log path>` |
| Green (focused) | `<gradle command>` | <N>/<N> PASS | `<log path>` |
| Green (full suite) | `<gradle command>` | <N>/<N> PASS | `<log path>` |
| Base comparison | `<gradle command>` at base | <N> tests, <M> failed → <N'> tests, <M'> failed | `<log path>` |

### Coverage audit (ADR 0019)

- **Rating**: pass / conditional-pass / fail
- **Risk-weighted score**: <X>/<Y>
- **Memtrace reconciliation**: clean (no undocumented changes, no drift, indexed SHA = head)
- **Audit document**: `<path to coverage-audit.md>`

### Review Phase 1 (parallel)

- **Blind Hunter**: <N> findings, severity breakdown
- **Edge Case Hunter**: <N> findings, severity breakdown
- **Acceptance Analyst**: <N> findings, severity breakdown
- **Triage**: <N> triaged → <patched / deferred / dismissed / decision-needed>

### Review Phase 2 (sequential)

- **Red Team**: <N> findings, severity breakdown
- **Blue Team**: <N> mitigations designed
- **Triage**: <N> triaged → <patched / deferred / dismissed / decision-needed>

### UAT

- **Status**: passed / failed / not applicable
- **Decision**: <user decision text>

## Diff inventory

| File | Change | AC |
|---|---|---|
| `<file>` | <change> | <AC id> |

## Deviations

<List any deviations from the plan, with justification. Reference the handoff's
deviations section.>

## Known issues and debt

<List any known issues or debt. Reference the handoff's known_debt.>

## Rollback

<One paragraph: how to roll back this PR if needed.>

## References

- Spec: `docs/superpowers/specs/<spec>.md` §<N>
- Plan: `docs/superpowers/plans/<plan>.md` Task <N>
- Handoff: `.maestro-space/maestro-works/<phase>/<task>/handoff.md`
- Session handout: `.maestro-space/maestro-works/<phase>/<task>/session-handout.md`
- Coverage audit: `.maestro-space/maestro-works/<phase>/<task>/coverage-audit.md`

---

🤖 Opened by `candelamoon-bot` via the orchestrator. **Approval required from @magalz
before merge.** Memtrace `review_github_pr` is run by the orchestrator as part of
step 13 of the per-task 14-step cycle.
