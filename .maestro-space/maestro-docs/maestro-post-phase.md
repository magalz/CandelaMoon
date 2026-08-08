# Maestro Post-Phase

> The rules, definitions, and directives for post-phase execution. After the last task
> of a phase is merged, Bernstein runs the post-phase session — a distinct session that
> dispatches four architects, synthesizes their reports, and produces the maintenance
> plan. The post-phase session is **BLOCKING** for the next phase.
>
> See companion documents:
> - **`maestro-workflow.md`** — task cycle and phase scaffolding.
> - **`maestro-setup.md`** — rules for the phase setup session.
> - **`maestro-maintenance.md`** — rules for maintenance phase execution.
> - **`maestro-orchestrator-guide.md`** — dispatch matrix, handoff protocol, review pipeline.

---

## 1. When Post-Phase Runs

The post-phase session runs EXACTLY ONCE per phase, immediately after the last task
of the phase is merged.

**BLOCKING RULE**: Phase N+1 cannot begin until Phase N's post-phase session is
complete and its outputs are committed. No exceptions.

---

## 2. Pre-Flight Checklist

Before dispatching any architect, Bernstein confirms:

- [ ] All tasks in the phase plan are marked `Completed`.
- [ ] All phase PRs are merged to the default branch.
- [ ] The design validator passes at the current HEAD (if applicable).
- [ ] Memtrace is synchronized with HEAD (if applicable).
- [ ] No open `Critical` findings from the phase remain unaddressed.
- [ ] The phase workspace directory exists.
- [ ] The post-phase workspace subdirectory exists.

If any check fails → HALT, report to user, do not proceed.

---

## 3. Post-Phase Session Flow

```
Session Start
  │
  ├─ 1. Bernstein runs pre-flight checklist (§2).
  │
  ├─ 2. Bernstein creates the post-phase workspace.
  │
  ├─ 3. Bernstein dispatches four architects:
  │     ┌─ Pair 1 (parallel) ──────────────────────────┐
  │     │ Haydn (GRC Architect)                         │
  │     │   Reads: all phase handoffs, ADR register,    │
  │     │   evidence manifests, phase plan              │
  │     │   Writes: grc-report.json + grc-report.md     │
  │     │                                               │
  │     │ Paganini (Security Analyst)                   │
  │     │   Reads: all security reviews, threat model,  │
  │     │   supply chain policy, signing policy         │
  │     │   Writes: security-report.json + .md          │
  │     └───────────────────────────────────────────────┘
  │     ┌─ Pair 2 (parallel) ──────────────────────────┐
  │     │ Ravel (QA Architect)                          │
  │     │   Reads: all coverage audits, ATDD checklists,│
  │     │   test suites, Memtrace evolution             │
  │     │   Writes: qa-report.json + qa-report.md       │
  │     │                                               │
  │     │ Vivaldi (DevOps Architect)                    │
  │     │   Reads: all CI workflows, Containerfiles,    │
  │     │   runner configs, image publish logs          │
  │     │   Writes: devops-report.json + .md            │
  │     └───────────────────────────────────────────────┘
  │
  │     Fallback (if parallel unavailable): sequential dispatch.
  │
  ├─ 4. Bernstein synthesizes the summary:
  │     Produces: summary.json + summary.md, maintenance plan.
  │
  ├─ 5. Bernstein commits all outputs to the default branch.
  │     No PR is opened — these are documentation artifacts.
  │
  └─ 6. Bernstein updates the phase plan: "Post-Phase Complete".
        Produces post-phase handout (template: `maestro-templates/post-phase-handout.md`). Session ends.
```

---

## 4. Architect Report Structure

Every report follows this template:

### 4.1 Header (all reports)

```yaml
---
phase: "Phase N"
role: "<grc | qa | security | devops>"
architect: "<Haydn | Ravel | Paganini | Vivaldi>"
status: "complete"
task_count: <N>
findings_count: <N>
---
```

### 4.2 Body Sections

1. **Scope**: what was analyzed (phase tasks, artifacts, time window).
2. **Methodology**: how the analysis was performed.
3. **Findings**: numbered list with severity, location, detail, recommendation.
4. **Trends**: patterns observed across the phase.
5. **Recommendations**: concrete actions for maintenance or Phase N+1.
6. **Open Risks**: issues that cannot be resolved in the maintenance phase.

### 4.3 Role-Specific Questions

| Role | Key Questions |
|---|---|
| Haydn (GRC) | Are all architectural decisions recorded as ADRs? Any conflicts? Waivers valid? Evidence manifests complete? |
| Ravel (QA) | Coverage trend? Flaky tests? Untested paths? Memtrace synchronized? |
| Paganini (Security) | Security debt accumulated? Threat model current? Dependencies fresh? Signing keys healthy? |
| Vivaldi (DevOps) | CI debt? Runners healthy? Images stale? Pipeline efficient? Artifacts reproducible? |

---

## 5. Maintenance Plan Generation

Bernstein synthesizes the four reports into a prioritized maintenance plan:

### 5.1 Task Derivation

- Every `high` severity finding → at least one maintenance task.
- Every `medium` finding → assess; most become tasks.
- `low` findings → may be deferred to Phase N+1.
- `critical` findings → BLOCK Phase N+1.

### 5.2 Maintenance Plan Structure

```markdown
# Maintenance Phase Plan — Phase N

**Generated by**: Bernstein, from post-phase session reports.
**Phase**: M{N}
**Source reports**: grc-report.md, qa-report.md, security-report.md, devops-report.md

## Maintenance Tasks

| ID | Title | Source Report | Severity | Status | Depends On | Complexity |
|---|---|---|---|---|---|---|
| M1-001 | <task> | grc-report | high | Pending | — | S |

## Tasks Deferred to Phase N+1

| ID | Title | Source | Severity | Reason |
|---|---|---|---|---|
```

### 5.3 Task IDs

Maintenance tasks use `M{N}-NNN` where N matches the phase number.

---

## 6. Hard Rules

1. **Post-phase is BLOCKING** for Phase N+1.
2. **No PR for post-phase**: outputs are committed directly.
3. **Four architects minimum**: all four roles must produce reports.
4. **Maintenance plan is mandatory**: even if empty, the document must exist.
5. **Critical findings block the next phase**.

---

## 7. Quick Reference

| Situation | Action |
|---|---|
| Last phase task merged | Begin post-phase session |
| Pre-flight check fails | HALT, report to user |
| Parallel dispatch unavailable | Fall back to sequential |
| Architect returns empty | Retry once → Bernstein fills from phase records |
| No findings from an architect | Report still produced — states "No findings" |
| Critical finding surfaced | Add to maintenance plan with BLOCKING flag |
| User wants to skip post-phase | DENY. Post-phase is non-negotiable. |
