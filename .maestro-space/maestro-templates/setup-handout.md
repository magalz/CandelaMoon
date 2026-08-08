# Setup Handout Template

> The continuity artifact produced at the end of the phase setup session.
> Carries everything the first task session needs to begin.

**File location**: `<workspace-dir>/phase-N-<short-desc>/setup-handout.md`

---

```markdown
# Setup Handout — Phase N: <Title>

**Date**: <YYYY-MM-DD>
**Setup by**: Bernstein

---

## Phase Identity

- **Phase**: Phase N
- **Title**: <title>
- **Goal**: <one-line goal>
- **Exit gate**: <measurable exit condition>
- **Related ADRs**: <IDs>

---

## Task Roster

| # | ID | Title | Status | Depends On | Complexity | Task File |
|---|---|---|---|---|---|---|
| 1 | P{N}-001 | <title> | Pending | — | M | `<path>` |
| 2 | P{N}-002 | <title> | Pending | P{N}-001 | S | `<path>` |

---

## First Task Key

- **Next task**: <task-id> — <title>
- **Task file**: `<path>`
- **Handoff will go to**: `<workspace-dir>/phase-N-<desc>/<task-id>-<desc>/handoff.md`
- **Production agent**: <Bach / Vivaldi / Paganini / Haydn / Schubert / Debussy>

---

## External Context Keys

- **Global objectives**: `<plans-dir>/global-objectives.md`
- **Master roadmap**: `<plans-dir>/master-roadmap.md`
- **Spec**: `/docs/superpowers/specs/<spec>.md`
- **ADR register**: `/docs/adr/`
- **Infrastructure docs**: `/docs/infrastructure/`

---

## Workspace Path

`<workspace-dir>/phase-N-<short-desc>/`

---

## Pre-Flight Checklist

- [ ] Previous phase post-phase report committed
- [ ] Previous phase maintenance phase complete
- [ ] No Critical findings unaddressed
- [ ] Phase plan created at `<path>`
- [ ] All task files created
- [ ] Workspace directory created
```
