# Post-Phase Report — QA Architect Template

> The QA Architect's post-phase report. Reviews coverage trends, test debt, flakiness,
> untested paths, and Memtrace drift across the whole phase. The companion JSON is
> `qa-report.json`.

**File location**: `.maestro-space/maestro-works/<phase-short-desc>/post-phase-<N>/qa-report.md`

---

```markdown
# Post-Phase Report — QA Architect — <Phase> (<YYYY-MM-DD>)

- **Phase**: <Phase N> — <phase short description>
- **Branch state**: <list of task branches, head SHAs, PR URLs>
- **Reviewer**: QA Architect (`qa-architect`)
- **Date**: <YYYY-MM-DD>
- **Dispatched by**: <orchestrator session id>

---

## 1. Scope

[All tasks in the phase, plus the per-task coverage audits and the aggregated coverage
metrics if available.]

## 2. Coverage trends

### Per-task coverage ratings
| Task | Coverage rating | Risk-weighted score | Gaps |
|---|---|---|---|
| <task-id> | pass / conditional-pass / fail | X/Y | <gap list> |

### Aggregate coverage
[If the phase ran in a single CI job, the aggregate coverage report. Otherwise, the
union of per-task static mappings and any cross-cutting instrumented runs.]

## 3. Test debt

### Flaky tests
[Every test marked flaky in the phase. Each: test, flakiness pattern, root cause
hypothesis, mitigation cost, recommended action (fix / quarantine / accept).]

### Untested paths
[Code paths reached by the phase's diffs that are not exercised by any named test.
Static mapping plus Memtrace coverage if available.]

### Test infrastructure debt
[Missing or stale test utilities, deprecated shadows, JDK / Android SDK migrations
needed, dependency upgrades required.]

## 4. Memtrace drift

- Indexed SHAs across the phase
- Any working_tree episodes not followed by a git_commit
- Any drift between `memtrace_indexed_sha` and the task's `head_sha` at handoff time
- Index health (node/edge counts, community count, process count)

## 5. Findings

### QA-NN — <title>
- **Severity**: <low/medium/high/critical>
- **Location**: <test file or untested path>
- **Detail**: ...
- **Evidence**: ...
- **Suggested route**: <patch / defer to maintenance / dismiss / decision-needed>

## 6. Summary

- Total findings: N
- By severity: ...
- Coverage posture: <summary>
- Test debt summary: <one paragraph>
- Maintenance-phase recommendations: <list>

## Handoff to

[Orchestrator for synthesis into the post-phase summary.]
```
