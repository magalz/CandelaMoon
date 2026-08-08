# Post-Phase Report — Security Analyst Template

> The Security Analyst's post-phase report. Reviews security debt, threat-model drift,
> dependency freshness, and signing key health across the whole phase. The companion
> JSON is `security-report.json`.

**File location**: `.maestro-space/maestro-works/<phase-short-desc>/post-phase-<N>/security-report.md`

---

```markdown
# Post-Phase Report — Security Analyst — <Phase> (<YYYY-MM-DD>)

- **Phase**: <Phase N> — <phase short description>
- **Branch state**: <list of task branches, head SHAs, PR URLs>
- **Reviewer**: Security Analyst (`security-analyst`)
- **Date**: <YYYY-MM-DD>
- **Dispatched by**: <orchestrator session id>

---

## 1. Scope

[All tasks in the phase, their security reviews (Phase 2), and the phase's overall
attack surface changes.]

## 2. Threat-model drift

[Every change to the trust boundaries, the data flow, or the persistent state in the
phase. For each: the original threat model entry, the change, the new residual risk,
the recommended action (update threat model / add mitigation / accept).]

## 3. Dependency freshness

| Dependency | Version pinned | Latest stable | CVEs since pin | Action |
|---|---|---|---|---|
| <dep> | <version> | <version> | <list> | <bump / accept / monitor> |

## 4. Signing and key health

- Signing keys: <list, age, rotation status>
- Image signatures: <list, verification status>
- GitHub App keys: <list, expiration, rotation status>
- Bot permissions: <list, least-privilege audit>

## 5. Per-task Phase 2 results

| Task | Red Team finding | Blue Team mitigation | Outcome |
|---|---|---|---|
| <task-id> | <summary> | <summary> | clean / patch applied / deferred |

## 6. Findings

### SEC-NN — <title>
- **Severity**: <low/medium/high/critical>
- **Location**: <file or threat-model surface>
- **Detail**: ...
- **Evidence**: ...
- **Suggested route**: <patch / defer to maintenance / dismiss / decision-needed>

## 7. Summary

- Total findings: N
- By severity: ...
- Security posture: <summary>
- Maintenance-phase recommendations: <list>

## Handoff to

[Orchestrator for synthesis into the post-phase summary.]
```
