# Post-Phase Report — GRC Architect Template

> The GRC Architect's post-phase report. Reviews governance, ADR alignment, waivers,
> evidence-manifest gaps, and documentation completeness for the whole phase. The
> companion JSON is `grc-report.json` (`agent-output.schema.json`
> `artifact_type: post-phase-report`).

**File location**: `.maestro-space/maestro-works/<phase-short-desc>/post-phase-<N>/grc-report.md`

---

```markdown
# Post-Phase Report — GRC Architect — <Phase> (<YYYY-MM-DD>)

- **Phase**: <Phase N> — <phase short description>
- **Branch state**: <list of task branches, head SHAs, PR URLs, merge status>
- **Reviewer**: GRC Architect (`grc-architect`)
- **Date**: <YYYY-MM-DD>
- **Dispatched by**: <orchestrator session id>

---

## 1. Scope

[All tasks in the phase: their ADRs touched, their evidence manifests, their handoffs,
their session handouts. The GRC review walks the full phase, not a single diff.]

## 2. Governance compliance

### ADR coverage
[List every architectural decision touched in the phase. For each: ADR id, status
(proposed/accepted/superseded), the task that triggered it, evidence pointer.]

### Waiver register
[Every waiver active in the phase. Each waiver: id, what it waives, why, expiration.]

### Decision lineage
[Trace from spec → ADR → plan task → implementation → evidence. Any orphan decisions
(ADRs without spec linkage, or implementations without ADRs) are flagged.]

## 3. Evidence manifest completeness

| Task | Handoff | ATDD checklist | Coverage audit | Session handout | Reviewer findings | Memtrace reconciled |
|---|---|---|---|---|---|---|
| <task-id> | yes/no | yes/no | yes/no | yes/no | yes/no | yes/no |

[For any "no", the gap and the consequence.]

## 4. Compliance with framework conventions

[For each convention in `maestro-conventions.md`: confirm the phase's tasks comply.
Output format (JSON+MD), file naming, tag nomenclature, handoff shape, status
transitions, secrets handling, schema conformance.]

## 5. Findings

### GRC-NN — <title>
- **Severity**: <low/medium/high/critical>
- **Location**: <file or governance surface>
- **Detail**: ...
- **Evidence**: ...
- **Suggested route**: <patch / defer to maintenance / dismiss / decision-needed>

## 6. Summary

- Total findings: N
- By severity: ...
- Compliance posture: <summary>
- Maintenance-phase recommendations: <list of items to add to the maintenance plan>

## Handoff to

[Orchestrator for synthesis into the post-phase summary. The orchestrator then
produces the maintenance phase plan.]
```
