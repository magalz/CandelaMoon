# Post-Phase Summary Template

> The orchestrator's synthesis of the four post-phase reports (GRC, QA, Security,
> DevOps). This is the single document the orchestrator commits to the branch; the
> four role-specific reports are the inputs. The companion JSON is `summary.json`
> (`agent-output.schema.json` `artifact_type: post-phase-summary`).

The orchestrator also uses this summary to produce the **maintenance phase plan**
(see `maintenance-phase-plan.md` template), which is a separate deliverable.

**File location**: `.maestro-space/maestro-works/<phase-short-desc>/post-phase-<N>/summary.md`

---

```markdown
# Post-Phase Summary — <Phase> (<YYYY-MM-DD>)

- **Phase**: <Phase N> — <phase short description>
- **Synthesized by**: Orchestrator
- **Date**: <YYYY-MM-DD>
- **Inputs**:
  - `grc-report.md` (GRC Architect)
  - `qa-report.md` (QA Architect)
  - `security-report.md` (Security Analyst)
  - `devops-report.md` (DevOps Architect)

---

## 1. Phase overview

[One-paragraph summary of what the phase delivered. Number of tasks, number of PRs,
key outcomes, exit gate status.]

## 2. Aggregated findings

| ID | Title | Source | Severity | Route |
|---|---|---|---|---|
| GRC-01 | <title> | GRC | <sev> | <route> |
| QA-01 | <title> | QA | <sev> | <route> |
| SEC-01 | <title> | Security | <sev> | <route> |
| DO-01 | <title> | DevOps | <sev> | <route> |

Totals: <N> findings; <breakdown by severity and source>.

## 3. Cross-cutting concerns

[Issues that appear in more than one report. E.g., "stale GHA token" reported by
both GRC and Security — consolidate, prioritize once.]

## 4. Maintenance phase plan

[A pointer to `maintenance-phase-plan.md` (the separate deliverable). Summary: <N>
maintenance tasks, IDs <M1-001..M1-NNN>, blocking-vs-non-blocking split.]

## 5. Exit gate verification

[Verify the phase's exit gate (from the phase backlog) is met. If met, declare the
phase COMPLETE. If not, list the remaining items.]

## 6. Hand-off to maintenance phase

[The maintenance phase is a regular phase. It uses the standard per-task 14-step
cycle. The hand-off is the maintenance plan + this summary, both committed to the
phase branch.]

## 7. Hand-off to next phase

[Only after the maintenance phase completes can Phase N+1 begin. The hand-off
includes: this summary, the maintenance plan, all maintenance task handoffs and
PRs, the next phase's backlog, and the readiness check confirmation.]
```
