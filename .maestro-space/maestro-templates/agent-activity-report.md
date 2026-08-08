# Activity Report Template

> Every agent emits this for every dispatch. The companion JSON (`<agent>-activity-report.json`)
> conforms to `agent-output.schema.json` `artifact_type: activity-report`. This file is
> the human narrative.

**File location**: `.maestro-space/maestro-works/<phase-short-desc>/<task-id>-<short-desc>/<agent>-activity-report.md`

---

```markdown
# Activity Report — <Agent Name>

- **Agent**: <agent name> (`<subagent_type>`)
- **Task**: <task-id> — <task short title>
- **Branch**: `<task branch>`
- **Base SHA**: `<40-char hex>`
- **Head SHA**: `<40-char hex>` (after this dispatch)
- **Date**: <YYYY-MM-DD>
- **Dispatched by**: <orchestrator session id>
- **task_id**: <subagent task_id, opaque ULID>

---

## Environment

[Execution boundary. Container or host. Key tools and versions. Any workarounds.]

## Actions

Numbered list of concrete actions taken.

1. Read `<file>` and understood `<concept>`.
2. Modified `<file>` to <change>.
3. Ran `<command>`; observed `<output>`.
4. ...

## Files

- **Created**: `<path>` — <purpose>
- **Modified**: `<path>` — <change>
- **Read**: `<path>` (for context, not modified)

## Verification

Commands run and observed output (concise; reference full logs by path).

| Command | Expected | Observed |
|---|---|---|
| `<command>` | <expected> | <observed> |
| `<command>` | <expected> | <observed> |

Full logs: `<path list>`

## Deviations

[Anything done that wasn't in the plan, with justification. Cross-reference the handoff's
deviations section if relevant.]

1. <deviation>: <why it was needed>

## Known Issues

[Anything observed that isn't actionable in this task but is worth recording.]

1. <issue>: <why it isn't actionable here; suggested follow-up>

## Handoff to

[The next agent or step. State the next concrete action.]
```
