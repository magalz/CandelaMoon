---
name: "[Tech Debt.P{N}.NN] <one-line title>"
about: "Architectural or structural item requiring careful, expert handling"
title: "[Tech Debt.P{N}.NN] <one-line title>"
labels: ["Tech Debt"]
assignees: []
---

## Source

- **Origin**: Review finding (typically GRC or QA) or architectural observation
- **Source file**: `<path to source>` (post-phase report, finding, ADR, or design doc)
- **Severity**: <low/medium/high/critical>
- **Route**: tech-debt (requires careful, expert handling — not a simple patch)

## Description

<One paragraph describing the architectural or structural concern, why it matters,
and the risk of leaving it unaddressed.>

## Why it is Tech Debt, not a regular task

<One paragraph: what makes this require expert handling — cross-cutting impact,
architectural decision required, multiple subsystems involved, etc.>

## Proposed approach

<One paragraph: the high-level approach. The assigned agent is not bound to this;
they should re-investigate and may propose a different approach.>

## Acceptance criteria

- [ ] <architectural criterion — e.g., "decision documented in an ADR">
- [ ] <testable criterion>
- [ ] <regression-prevention criterion>

## References

- Spec section: `<docs/superpowers/specs/...md> §X`
- ADRs: `<id list>` (and any that this issue may need to update or supersede)
- Related issues: `<#N>`
- Memtrace symbol ids: `<if applicable>`

---
Filed by the orchestrator from a post-phase review or a per-task finding. The issue
is self-contained: an individual agent in a new context can pick this up with no
additional conversation history.
