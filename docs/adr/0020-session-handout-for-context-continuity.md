---
id: "0020"
title: "Session Handout for Context Continuity"
status: accepted
date: "2026-08-05"
context: "Agent sessions lose context between runs. Spec section 15.4 defines session handoffs. Conversation history is not preserved across sessions, so each session would otherwise start blind."
decision: "The Tech Writer creates a self-contained session handout at the end of every task and phase. It contains: current state, artifacts produced, pending work, keys for the next session, known debt, and rollback strategy."
consequences: "Sessions resume without re-exploration; the handout is the continuity contract that production agents update and review agents never touch."
alternatives:
  - name: "Rely on conversation history"
    rejection_reason: "Context rot, especially across sessions where history is lost."
  - name: "No handout"
    rejection_reason: "The next session starts blind."
evidence:
  - "Spec section 15.4."
---

# ADR 0020: Session Handout for Context Continuity

## Context

CandelaMoon is developed through agent sessions that do not preserve conversation history between runs - each new session starts with no memory of the previous one. Spec section 15.4 defines session handoffs for the project. Without an explicit continuity mechanism, every session re-explores the codebase, re-derives decisions, and risks working from stale assumptions, which compounds across a long project.

## Decision

The Tech Writer creates a self-contained session handout at the end of every task and phase. The handout contains: current state, artifacts produced, pending work, keys for the next session, known debt, and rollback strategy. The alternatives were rejected: relying on conversation history fails because history is lost across sessions and rots even within them, and having no handout means the next session starts blind. The evidence is spec section 15.4.

## Consequences

Sessions resume without re-exploration, preserving continuity for a solo human orchestrating many agents (ADR 0015). The handout becomes the continuity contract: production agents receive and update it as work proceeds, review agents receive only need-to-know slices and never modify it, and the orchestrator can audit state at any point by reading it. Known debt and rollback strategy travel with the work, so a later session can finish or undo work rather than rediscover it. The cost is a writing obligation at every boundary - but it is a small, mechanical one compared with the cost of a session that starts blind.

## Alternatives

### Rely on Conversation History

Conversation history is not preserved across sessions and degrades within long ones, so it cannot serve as continuity. Rejected.

### No Handout

Without a handout, every session starts blind, re-exploring the codebase and re-deriving decisions that were already made. Rejected.

**Framework reference**: This ADR is operationalized in .maestro-space/maestro-docs/maestro-workflow.md §6 (Session Handout) and .maestro-space/maestro-templates/session-handout.md (the handout template). Every task's handout is recorded at .maestro-space/maestro-works/<phase>/<task>/session-handout.{md,json}. See also .maestro-space/maestro-conventions.md §7 (Session Handout Conventions).
