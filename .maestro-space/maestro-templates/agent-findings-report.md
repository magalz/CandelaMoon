# Findings Report Template

> Every review agent emits this for each Phase 1 and Phase 2 review. The companion
> JSON (`findings-phase-N.json`) conforms to `agent-output.schema.json`
> `artifact_type: findings`. This file is the human narrative.

**File location**: `.maestro-space/maestro-works/<phase-short-desc>/<task-id>-<short-desc>/findings-phase-N.md` (N is 1 or 2)

---

```markdown
# Findings Report — <Reviewer Name> (Phase <N>)

- **Reviewer**: <agent name> (`<subagent_type>`)
- **Task**: <task-id> — <task short title>
- **Branch**: `<task branch>`
- **Base SHA**: `<40-char hex>`
- **Head SHA**: `<40-char hex>`
- **Date**: <YYYY-MM-DD>
- **Dispatched by**: <orchestrator session id>

---

## Scope

[What was reviewed. The diff (`git diff <base>..<head>`) and any context the reviewer
was given (spec, acceptance criteria for acceptance-analyst; red-team findings for
blue-team). Explicitly note what was NOT given: the handoff, the plan, ADRs, author
rationale.]

## Method

[How the review was conducted. For blind-hunter: at least 10 issues sought, cynical
adversarial lens. For edge-case-hunter: every branching path walked. For
acceptance-analyst: AC-by-AC walkthrough. For red-team: STRIDE / OWASP checklist. For
blue-team: re-review of red-team findings with mitigations designed.]

## Findings

[Numbered list. Each finding has: id (agent-local), title, severity, detail, location
(file:line or symbol), suggested route, evidence.]

### <id> — <title>

- **Severity**: <low/medium/high/critical/info>
- **Location**: `<file>:<line>` or `<symbol>`
- **Detail**: <what the issue is, why it matters>
- **Evidence**: <log line, spec section, AC id, test name>
- **Suggested route**: <patch / defer / dismiss / decision-needed>

[Repeat for each finding.]

## Summary

- Total findings: <N>
- By severity: <N critical, N high, N medium, N low, N info>
- Top concerns: <1-3 sentences>
- Out-of-scope items: <anything the reviewer noticed but considers out of scope for this task>
```
