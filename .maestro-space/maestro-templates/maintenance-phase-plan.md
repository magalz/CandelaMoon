# Maintenance Phase Plan Template

> The output of the post-phase session that the maintenance phase executes. Each
> maintenance task is a standard 14-step task (1 task = 1 session = 1 PR). The
> companion JSON is `maintenance-phase-plan.json` (`agent-output.schema.json`
> `artifact_type: maintenance-plan`).

**File location**: `.maestro-space/maestro-works/<phase-short-desc>/post-phase-<N>/maintenance-phase-plan.md`

---

```markdown
# Maintenance Phase Plan — after <Phase> (<YYYY-MM-DD>)

- **Preceding phase**: <Phase N>
- **Maintenance phase ID range**: <M1-001 .. M1-NNN>
- **Synthesized by**: Orchestrator (from post-phase reports)
- **Date**: <YYYY-MM-DD>

---

## 1. Goal

[One paragraph: what the maintenance phase fixes so that the next phase can begin
clean. Explicitly state what BLOCKS the next phase if the maintenance phase is skipped.]

## 2. Task list

### M1-001: <title>

- **Source finding**: <GRC-01 / QA-02 / SEC-03 / DO-04> (from <which post-phase report>)
- **Severity**: <low/medium/high/critical>
- **Blocking for next phase**: yes / no
- **Estimated complexity**: S / M / L
- **Description**: <one paragraph>
- **Acceptance criteria**:
  - <testable criterion>
  - <testable criterion>
- **Related ADR**: <id, if any>
- **Risk if skipped**: <one paragraph>

### M1-002: <title>
[Same shape.]

[One block per maintenance task. Order by blocking-first, then by severity.]

## 3. Dependency graph

[If maintenance tasks have dependencies between them, list them. Otherwise note
"no inter-task dependencies; can be parallelized up to runner availability."]

## 4. Estimated effort

- Total maintenance tasks: <N>
- Blocking tasks: <N>
- Non-blocking tasks: <N>
- Estimated total session-hours: <rough estimate>

## 5. Completion criteria

The maintenance phase is COMPLETE when:
- Every blocking task is `done` (PR merged)
- Every non-blocking task is either `done` or explicitly deferred to the next phase
  with a `[Tech Debt.P{N+1}.NN]` issue filed
- The post-maintenance summary (a short version of the post-phase summary template)
  is committed
- The next phase's readiness check passes (see `maestro-workflow.md` §3.1)

## 6. Hand-off

[After the maintenance phase is complete, the next phase can begin. The hand-off is:
this plan (read), the post-phase summary (read), the maintenance task handoffs and
PRs (reviewed), and the next phase's backlog (now the active plan).]
```
