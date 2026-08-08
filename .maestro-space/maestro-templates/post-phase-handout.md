# Post-Phase Handout Template

> The continuity artifact produced at the end of the post-phase session.
> Carries everything the maintenance phase needs to begin.

**File location**: `<workspace-dir>/phase-N-<short-desc>/post-phase-<N>/post-phase-handout.md`

---

```markdown
# Post-Phase Handout — Phase N: <Title>

**Date**: <YYYY-MM-DD>
**Synthesized by**: Bernstein

---

## Phase Summary

<One paragraph: what was accomplished, key metrics, overall assessment.>

---

## Architect Reports

| Role | Architect | Report |
|---|---|---|
| Governance | Haydn | `<grc-report-path>` |
| Quality | Ravel | `<qa-report-path>` |
| Security | Paganini | `<security-report-path>` |
| DevOps | Vivaldi | `<devops-report-path>` |

---

## Maintenance Plan

**Plan document**: `<maintenance-phase-plan-path>`

| ID | Title | Source | Severity | Status |
|---|---|---|---|---|
| M{N}-001 | <title> | grc-report | high | Pending |
| M{N}-002 | <title> | security-report | medium | Pending |

**First maintenance task**: M{N}-001 — <title>

---

## Known Debt Carried Forward

| ID | Item | Severity | Phase Introduced | Resolution Target |
|---|---|---|---|---|
| <id> | <description> | low | Phase N | Phase N+1 |

---

## Keys for Maintenance Phase

- **Maintenance plan**: `<path>`
- **Post-phase handout**: `<path>` (this file)
- **All architect reports**: see table above
- **Spec**: `/docs/superpowers/specs/<spec>.md`
- **ADR register**: `/docs/adr/`

---

## Keys for Next Phase (Phase N+1)

- **Global objectives**: `<plans-dir>/global-objectives.md`
- **Master roadmap**: `<plans-dir>/master-roadmap.md`
- **Setup guide**: `maestro-setup.md`
```
