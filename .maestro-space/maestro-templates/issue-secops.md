---
name: "[SecOps.P{N}.NN] <one-line title>"
about: "Security finding from Red/Blue team review"
title: "[SecOps.P{N}.NN] <one-line title>"
labels: ["SecOps"]
assignees: []
---

## Source

- **Origin**: Red Team or Blue Team review (Phase 2) of a task in Phase N
- **Source file**: `<path to findings-phase-2.{json,md}>`
- **Finding ID**: `<e.g., SEC-001>`
- **Severity**: <low/medium/high/critical>
- **STRIDE category**: <Spoofing / Tampering / Repudiation / Information Disclosure / Denial of Service / Elevation of Privilege>
- **OWASP category**: <if applicable>

## Vulnerability

<One paragraph: what the issue is, what the attack scenario is, and what asset is
at risk.>

## Reproduction / Evidence

<How to reproduce. For a confirmed vulnerability, include the red-team reproduction
steps. Reference logs, code snippets, test names.>

## Mitigation

<The Blue Team's recommended mitigation. This is the starting point; the assigned
agent may refine.>

## Acceptance criteria

- [ ] Mitigation implemented and verified
- [ ] New test added (if applicable) that would have caught the vulnerability
- [ ] Threat model updated (if applicable)
- [ ] No regression in existing tests
- [ ] No new findings from the same STRIDE/OWASP category introduced

## References

- Spec section: `<docs/superpowers/specs/...md> §X`
- ADRs: `<id list>` (and any this issue may need to update or supersede)
- Related issues: `<#N>`
- Threat model entry: `<if any>`

---
Filed by the orchestrator from a Red/Blue team review. The issue is self-contained:
an individual agent in a new context can pick this up with no additional conversation
history.
