# Post-Phase Report — DevOps Architect Template

> The DevOps Architect's post-phase report. Reviews CI debt, pipeline health, runner
> utilization, container/image staleness, and infrastructure-as-code coverage across
> the whole phase. The companion JSON is `devops-report.json`.

**File location**: `.maestro-space/maestro-works/<phase-short-desc>/post-phase-<N>/devops-report.md`

---

```markdown
# Post-Phase Report — DevOps Architect — <Phase> (<YYYY-MM-DD>)

- **Phase**: <Phase N> — <phase short description>
- **Branch state**: <list of task branches, head SHAs, PR URLs>
- **Reviewer**: DevOps Architect (`devops-architect`)
- **Date**: <YYYY-MM-DD>
- **Dispatched by**: <orchestrator session id>

---

## 1. Scope

[All tasks in the phase, their CI/CD impact, the per-tier workflows exercised, the
container images built/published, the runners used.]

## 2. CI pipeline health

### Per-tier status
| Tier | Workflow file | Last green run | Failure rate (last 30 days) | MTTR | Notes |
|---|---|---|---|---|---|
| per-commit | `.github/workflows/ci.yml` | <run id> | <%> | <min> | ... |
| per-PR | `.github/workflows/pr.yml` | <run id> | <%> | <min> | ... |
| nightly | `.github/workflows/nightly.yml` | <run id> | <%> | <min> | ... |
| release-candidate | `.github/workflows/release.yml` | <run id> | <%> | <min> | ... |

### Required status checks
[List the checks required for merge to `moonlight-noir`. Verify each one is actually
gating. Flag any that are passing but not required, or required but not actually
running.]

## 3. Container/image staleness

| Image | Registry | Tag | Built | Last vulnerability scan | Action |
|---|---|---|---|---|---|
| <image> | ghcr.io | <tag> | <date> | <date> | rebuild / accept / monitor |

## 4. Runner utilization

| Runner | Type | Usage (last 30 days) | Queue time | Notes |
|---|---|---|---|---|
| <runner> | self-hosted | <hours> | <min> | ... |

## 5. IaC coverage

[Every infrastructure change in the phase: workflow file, container image, runner
config, signing config. Verify each is captured in a tracked file. Flag untracked
infrastructure (manual changes, env-only changes, etc.).]

## 6. Findings

### DO-NN — <title>
- **Severity**: <low/medium/high/critical>
- **Location**: <workflow file / image / runner config>
- **Detail**: ...
- **Evidence**: ...
- **Suggested route**: <patch / defer to maintenance / dismiss / decision-needed>

## 7. Summary

- Total findings: N
- By severity: ...
- Pipeline posture: <summary>
- Infrastructure debt: <one paragraph>
- Maintenance-phase recommendations: <list>

## Handoff to

[Orchestrator for synthesis into the post-phase summary.]
```
