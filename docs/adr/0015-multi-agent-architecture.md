---
id: "0015"
title: "Multi-Agent Development Architecture"
status: accepted
date: "2026-08-05"
context: "CandelaMoon is developed by a solo human using an agentic workflow. Spec section 15.1 defines the development process. Single-agent execution cannot provide independent review, and a human cannot review everything at scale."
decision: "Development runs on a multi-agent architecture with seven production agents (Senior Developer, QA Architect, DevOps Architect, Security Analyst, GRC Architect, Tech Writer, UX/UI Designer) and five review agents (Blind Hunter, Edge Case Hunter, Acceptance Analyst, Red Team, Blue Team). Production agents receive and update the handoff file; review agents receive only need-to-know information and never update it."
consequences: "Review is independent of development, and context flows through the handoff file. The human orchestrates and audits."
alternatives:
  - name: "Single agent does everything"
    rejection_reason: "No independence for review, context rot, and no specialization."
  - name: "Human does all review"
    rejection_reason: "Not scalable for a solo developer."
evidence:
  - "Spec section 15.1."
---

# ADR 0015: Multi-Agent Development Architecture

## Context

CandelaMoon is developed by a solo human working through an agentic workflow, which raises two problems. First, independence: the agent that writes code cannot also be the agent that reviews it, because it is anchored to its own assumptions. Second, scale: a human cannot personally review every change across a large inherited codebase. Spec section 15.1 defines the development process for the project.

## Decision

Development runs on a multi-agent architecture with seven production agents - Senior Developer, QA Architect, DevOps Architect, Security Analyst, GRC Architect, Tech Writer, and UX/UI Designer - and five review agents - Blind Hunter, Edge Case Hunter, Acceptance Analyst, Red Team, and Blue Team. Production agents receive and update the handoff file (ADR 0020); review agents receive only need-to-know information and never update it. The alternatives were rejected: a single agent doing everything provides no independent review, suffers context rot, and has no specialization, and a human reviewing everything is not scalable for a solo developer. The evidence is spec section 15.1.

## Consequences

Review is genuinely independent because review agents do not see the developer's full context and cannot modify the handoff file, which also prevents review findings from contaminating development state. The handoff file is the shared memory production agents maintain, making sessions continuous (ADR 0020). The human orchestrator triages review findings (ADR 0017), audits the agents' work, and remains the accountable integrator - the architecture multiplies the human, it does not replace them.

## Alternatives

### Single Agent Does Everything

One agent writing and reviewing its own work lacks independence, accumulates context rot over long sessions, and cannot specialize across security, UX, and testing. Rejected.

### Human Does All Review

A solo human reviewing every change at scale is not sustainable and would bottleneck development. Rejected.

**Framework reference**: This ADR is operationalized in .maestro-space/maestro-docs/maestro-orchestrator-guide.md §1 (Agent Dispatch Matrix) and .maestro-space/maestro-agents/agent-manifest.json (the agent registry mapping logical names to subagent_type). The full production+review agent roster is defined there. Conventions: .maestro-space/maestro-docs/maestro-conventions.md.
