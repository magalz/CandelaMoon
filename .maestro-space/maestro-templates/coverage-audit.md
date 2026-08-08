# Coverage Audit Template

> The QA Architect's standalone coverage audit (ADR 0019). The companion JSON is
> `coverage-audit.json` (machine-readable AC matrix + risk-weighted score); this file
> is the human narrative with full evidence.

The companion JSON file is `coverage-audit.json`. See `agent-output.schema.json`
`artifact_type: coverage-audit`.

**File location**: `.maestro-space/maestro-works/<phase-short-desc>/<task-id>-<short-desc>/coverage-audit.md`

---

```markdown
# Coverage Audit — <task-id>: <task short title>

- **Task**: <task-id>
- **Branch**: `<task branch>`
- **Base SHA**: `<40-char hex>`
- **Head SHA**: `<40-char hex>`
- **Auditor**: QA Architect
- **Date**: <YYYY-MM-DD>
- **ADR**: 0019 (Coverage Audit with Memtrace Reconciliation)

## 1. Diff inventory — every changed symbol mapped to an AC

[For each changed file: the symbol, the change, the AC, and the test(s) covering it.
Group by production code, test code, and resource-only / line-ending changes.]

## 2. Red-phase evidence verification

| Claim | Evidence | Verified |
|-------|----------|----------|
| `<test> was red` | `<log path>, line N, FAILED; root cause …` | YES |
| `<test> was NOT red` | `<log path>; N tests, M failed (the predicted set); the predicted test passed` | YES |
| `Red phase run: N tests, M failed` | `<log path>` | YES |
| `Base suite: N tests, M failed` | `<log path>` | YES |

## 3. Green-phase evidence verification

[Same shape as the red-phase table. Reconcile any test count discrepancies and explain.]

## 4. Memtrace reconciliation

### Index verification
- repo_id, indexed SHA, branch, last indexed, node/edge counts

### detect_changes
[Diff → affected symbols. State any unexpected or out-of-scope symbols.]

### get_timeline
[For any non-trivial production symbol, show the version history and confirm the
implementation story matches the handoff narrative. Flag any reverted attempts.]

### get_evolution
[Episode counts in the task window. State any unexpected episodes or missing episodes.]

### Episode provenance
[For new symbols, confirm the provenance points at the expected agent/session.]

### Reconciliation conclusion
- [Bullet: every changed symbol is documented in the handoff]
- [Bullet: the implementation evolution is confirmed by the timeline]
- [Bullet: the indexed SHA matches head, no drift]
- [Bullet: any minor limitations and their impact on the audit]

## 5. Acceptance-criterion coverage matrix

| AC | Scenario | Test(s) | Status |
|----|----------|---------|--------|
| AC #N | <scenario description> | <test name(s)> | COVERED (with evidence pointer) |

## 6. Review triage verification

| Finding | Severity | Route | Fix applied | Verified |
|---------|----------|-------|-------------|----------|
| <id> | <sev> | patch / defer / dismiss / decision-needed | <what> | YES / NO + why |

## 7. Coverage tooling

[Tool versions, configuration, what was run, what was not. JaCoCo / Kover / Istanbul /
etc. State limitations explicitly.]

## 8. Risk-weighted score

| AC | Risk weight | Coverage | Score |
|----|------------|----------|-------|
| AC #N | high / medium / low | <coverage summary> | X/10 |

**Total**: N/M (P%)

## 9. Coverage gaps

- <gap 1 with severity and impact>
- <gap 2 with severity and impact>

## 10. Rating

**PASS / CONDITIONAL-PASS / FAIL**

[Justification: every AC covered, every changed symbol tested, no high-risk scenario
uncovered, Memtrace clean, no test weakening, full suite green with base comparison.]

[If conditional-pass: list the conditions for the next pass.]
[If fail: list the specific tasks to add to the backlog.]
```
