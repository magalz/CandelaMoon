# Task File Template

> Individual task file. Bernstein creates one per task during the setup session.
> Lives next to the phase plan. Updated at the end of every session for that task.

**File location**: `<plans-dir>/phase-N-<short-desc>/<task-id>-<short-desc>.md`

---

```markdown
# <Task ID>: <Title>

**Phase**: Phase N
**Status**: Pending | In Development | Completed
**Dependencies**: <list of task IDs or "none">
**Complexity**: S | M | L
**Related ADRs**: <comma-separated IDs>

## Description

<One paragraph describing what this task accomplishes.>

## Acceptance Criteria

- <testable, atomic criterion>
- <testable, atomic criterion>

## Implementation Plan

1. <concrete step for the production agent>
2. <concrete step>
3. ...

## Evidence Requirements

- <what evidence proves this task is complete>
- <specific test command or validation check>

## Known Risks

- <risk description>
- <mitigation>

## References

- Spec: <path> §<section>
- Plan: <path> Task <N>
- ADRs: <IDs>

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| (populated as sessions execute) | | | | |
```

## Lifecycle

- **Created**: during the setup session by Bernstein.
- **Updated**: at the end of every task session for this task.
  The Session History table gains a new row.
- **Never deleted**: persists for the life of the phase as part of the evidence trail.
