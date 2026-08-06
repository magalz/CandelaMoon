---
id: "0009"
title: "Compose for TV Evaluation via Prototype"
status: accepted
date: "2026-08-05"
context: "CandelaMoon's UI could be built with Compose for TV or with modern Android Views. Compose promises a modern UI, but its TV-specific behaviors - D-pad focus, accessibility, streaming interop with the Java-based streaming activity - are unproven in this codebase. Spec section 2.5 defines the UI approach."
decision: "Compose for TV is evaluated through a bounded prototype in Phase 5. The prototype validates D-pad focus, accessibility, lifecycle, performance, and interop with the Java streaming activity. A follow-up ADR selects Compose or modern Views based on the evidence. Protected boundaries remain in place until evidence exists."
consequences: "The toolkit decision is deferred until evidence exists; interim UI work must not entrench either choice. The prototype scope must stay bounded."
alternatives:
  - name: "Compose selected without prototype"
    rejection_reason: "Unvalidated risk to D-pad focus, streaming interop, and performance."
  - name: "Modern Android Views only"
    rejection_reason: "Rejects modern UI tooling without evidence for or against it."
evidence:
  - "Spec section 2.5."
---

# ADR 0009: Compose for TV Evaluation via Prototype

## Context

CandelaMoon's user interface can be built with Compose for TV, the modern declarative Android UI toolkit, or with modern Android Views, the imperative toolkit the inherited Artemis code uses. Compose promises faster UI development and a modern look, but its TV-specific behaviors are unproven in this codebase: D-pad focus navigation, accessibility semantics, lifecycle behavior on TV, performance on constrained devices, and interop with the existing Java-based streaming activity. Spec section 2.5 defines the UI approach, and choosing a toolkit without evidence would bet the product's main surface on unvalidated assumptions.

## Decision

Compose for TV is evaluated through a bounded prototype in Phase 5. The prototype validates D-pad focus, accessibility, lifecycle, performance, and interop with the Java streaming activity, and a follow-up ADR selects Compose or modern Views based on the evidence. Protected boundaries - the seams between UI layers and the streaming activity - remain in place until evidence exists, so the choice is never forced prematurely. The alternatives were rejected: selecting Compose without a prototype accepts unvalidated risk on focus, interop, and performance, while committing to modern Views only rejects modern tooling without evidence for or against it. The evidence is spec section 2.5.

## Consequences

The toolkit decision is deferred to data rather than made by preference, keeping both doors open through Phase 5. The prototype must stay bounded - it exists to answer the five validation questions, not to build production UI on an unratified stack. Interim UI work must not entrench either choice, and the follow-up ADR is a committed step: the evaluation cannot silently lapse, and once selected, the winning toolkit is used consistently from that point forward.

## Alternatives

### Compose Selected Without Prototype

Adopting Compose for TV immediately risks unvalidated failure modes in D-pad focus, streaming interop, and performance that could force a late migration. Rejected.

### Modern Android Views Only

Choosing Views without a prototype rejects a modern, likely-faster UI stack without evidence either way. Rejected.
