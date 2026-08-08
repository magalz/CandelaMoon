---
name: "[Deferred.P{N}.NN] <one-line title>"
about: "Non-critical review finding deferred to a later phase"
title: "[Deferred.P{N}.NN] <one-line title>"
labels: ["Deferred"]
assignees: []
---

## Source

- **Origin**: Review finding from a task session in Phase N
- **Source file**: `<path to findings-phase-N.{json,md}>`
- **Finding ID**: `<e.g., PH1-005>`
- **Severity**: <low/medium/high>
- **Route**: defer (non-critical; not actionable in source task)

## Description

<One paragraph describing the finding, the impact, and why it was deferred rather than patched in-source.>

## Reproduction / Evidence

<How to reproduce or where the evidence lives. Reference logs, code snippets, test names, Memtrace symbol ids.>

## Suggested fix sketch

<One paragraph: the orchestrator's suggestion for how to address this in a future task. The assigned agent is not bound to this sketch.>

## Acceptance criteria

- [ ] <testable criterion>
- [ ] <testable criterion>

## References

- Spec section: `<docs/superpowers/specs/...md> §X`
- Plan task: `<docs/superpowers/plans/...md> Task N`
- ADRs: `<id list>`
- Related issues: `<#N>`

---
Filed by the orchestrator from a post-task triage. The issue is self-contained: an
individual agent in a new context can pick this up with no additional conversation
history.
