---
id: "0008"
title: "Single Adaptive UI"
status: accepted
date: "2026-08-05"
context: "With two platform tiers (ADR 0007), one option is to build two UIs: a modern one and a legacy one for constrained devices. Spec section 2.5 defines the UI approach. The user decided during brainstorming on 2026-08-05 that one UI must serve both tiers."
decision: "One adaptive UI serves both platform tiers. Constrained devices use reduced effects within the same component tree. There is no separate legacy UI."
consequences: "Single source of truth for UI behavior and theming; degradation is capability gating, not code duplication. A solo developer maintains one component tree."
alternatives:
  - name: "Modern plus legacy UIs"
    rejection_reason: "Doubles UI maintenance for a solo developer."
  - name: "Modern UI only with no degradation"
    rejection_reason: "Some API 28-30 devices may lack the hardware or platform features the modern UI assumes."
evidence:
  - "Spec section 2.5."
---

# ADR 0008: Single Adaptive UI

## Context

ADR 0007 establishes two platform tiers: API 31+ as the primary tier and API 28-30 as a compatibility tier. A natural but costly response is to build two user interfaces - a modern UI for new devices and a legacy UI for constrained ones - but that doubles every layout, theme, and interaction change. Spec section 2.5 defines the UI approach for the product, and the user decided during brainstorming on 2026-08-05 that a single adaptive UI must serve both tiers.

## Decision

One adaptive UI serves both platform tiers. Constrained devices receive reduced effects - fewer animations, lower-resolution textures, simpler rendering - within the same component tree, and there is no separate legacy UI. The alternatives were rejected: a modern-plus-legacy UI pair doubles maintenance for a solo developer, and a modern-UI-only approach without degradation would ship visual features that some API 28-30 devices cannot render acceptably. The evidence is spec section 2.5.

## Consequences

There is a single source of truth for navigation, theming, and interaction behavior, so every visual feature is defined once and degraded once. Degradation is expressed as capability gating and reduced effects rather than duplicated layouts, which keeps the component tree maintainable. The risk is that degradation must be designed, not bolted on: each visual feature needs a defined constrained-device fallback at design time, and performance measurements must confirm that the compatibility tier actually delivers the core streaming journey promised by ADR 0007.

## Alternatives

### Modern Plus Legacy UIs

Two complete UI implementations would double layout, theme, and interaction maintenance for a solo developer and let behavior drift between tiers. Rejected.

### Modern UI Only with No Degradation

Shipping the modern UI unchanged on API 28-30 assumes those devices can render it; some lack the hardware or platform features it depends on. Rejected.
