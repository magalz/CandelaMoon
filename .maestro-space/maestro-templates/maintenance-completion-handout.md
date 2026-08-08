# Maintenance Completion Handout Template

> The continuity artifact produced when all maintenance tasks are complete.
> Signals that Phase N+1 setup may begin.

**File location**: `<workspace-dir>/phase-N-<short-desc>/maintenance-completion-handout.md`

---

```markdown
# Maintenance Completion Handout — M{N} (after Phase N)

**Date**: <YYYY-MM-DD>
**Completed by**: Bernstein

---

## Maintenance Summary

All <N> maintenance tasks for M{N} are complete.

| ID | Title | PR URL | Head SHA | Status |
|---|---|---|---|---|
| M{N}-001 | <title> | <url> | <sha> | Completed |
| M{N}-002 | <title> | <url> | <sha> | Completed |

---

## Deferred to Phase N+1

| ID | Title | Severity | Reason |
|---|---|---|---|
| <id> | <description> | low | <reason> |

---

## Phase Boundary Status

- **Phase N**: Complete (tasks → post-phase → maintenance all done)
- **Phase N+1**: Unblocked. Setup session may begin.

---

## Remaining Known Debt

| ID | Item | Severity | Phase Introduced |
|---|---|---|---|
| <id> | <description> | <severity> | Phase N |

---

## Keys for Phase N+1 Setup

- **Setup guide**: `maestro-setup.md`
- **Global objectives**: `<plans-dir>/global-objectives.md`
- **Master roadmap**: `<plans-dir>/master-roadmap.md`
- **Phase N post-phase handout**: `<post-phase-handout-path>`
- **This handout**: `<path>` (this file)
```
