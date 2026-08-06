---
id: "0006"
title: "TV-Only Scope with Phased Mobile Removal"
status: accepted
date: "2026-08-05"
context: "Artemis inherited a large mobile-only surface: touch input code paths, mobile activities, and mobile preferences. CandelaMoon's product scope is TV-only (spec section 2.3). Removing mobile code is risky because shared paths may serve TV flows, so removal must be evidence-driven rather than a blanket sweep."
decision: "TV is the only supported form factor. Mobile-only behavior is classified first, then removed in controlled phases after dependency analysis. Removal is not conflated with decoder, controller, or protocol removal."
consequences: "The codebase shrinks in controlled increments with evidence, but mobile code persists during classification and removal is slow."
alternatives:
  - name: "Unsupported but retained indefinitely"
    rejection_reason: "Dead code accumulates and keeps being maintained and compiled."
  - name: "Remove in foundation phase"
    rejection_reason: "Deleting before dependency analysis risks breaking shared paths used by TV flows."
evidence:
  - "Spec section 2.3."
---

# ADR 0006: TV-only Scope with Phased Mobile Removal

## Context

The inherited Artemis codebase contains a large mobile-only surface: touch input code paths, mobile-specific activities, and mobile-oriented preferences. CandelaMoon's product scope is TV-only per spec section 2.3, so that mobile surface is out of scope by definition. The risk is that mobile code is not cleanly separable - some of it sits in shared modules that TV flows also use - so removing it as one blanket sweep could silently break the TV journey. Removal must therefore be evidence-driven.

## Decision

TV is the only supported form factor. Mobile-only behavior is classified first, then removed in controlled phases after dependency analysis, and mobile removal is not conflated with decoder, controller, or protocol removal - each of those is a separate disposition under ADR 0012. The alternatives were rejected: retaining mobile code indefinitely as "unsupported" lets dead code accumulate while still being maintained and compiled, and removing it in the foundation phase would delete code before dependency analysis, risking shared paths used by TV flows. The evidence is spec section 2.3.

## Consequences

The codebase shrinks in controlled increments, each backed by dependency analysis, impact evidence, and characterization tests (ADR 0012), which protects shared paths and makes each removal reversible in principle. The cost is that mobile code persists during classification, so the repository stays larger for longer and some churn is visible before value lands. TV-only focus also means touch-specific code is never maintained or tested once removed, and any accidental reuse of mobile paths is caught by the dependency analysis that precedes each deletion.

## Alternatives

### Unsupported but Retained Indefinitely

Keeping mobile code around as "unsupported" means it keeps being compiled, linted, and maintained, while its existence obscures what the product actually is. Rejected.

### Remove in Foundation Phase

A blanket removal early in the project deletes code before dependency analysis shows what TV flows share with it. The risk of breaking the core streaming journey is unacceptable. Rejected.
