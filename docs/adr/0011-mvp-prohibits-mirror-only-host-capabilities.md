---
id: "0011"
title: "MVP Prohibits Mirror-Only Host Capabilities"
status: accepted
date: "2026-08-05"
context: "The integration lab (ADR 0004) experiments with host behavior that may not exist in official LuminalShine releases. Spec section 2.1 frames host compatibility for the MVP. If MVP features depended on mirror-only behavior, users would need a custom host fork to run the product."
decision: "The MVP may consume only capabilities available in official LuminalShine releases. No MVP feature depends on luminalshine-mirror-only behavior."
consequences: "Every MVP feature is reproducible for users on official releases. Mirror experiments are documented as future work rather than silently shipped."
alternatives:
  - name: "Allow mirror capabilities in MVP"
    rejection_reason: "Creates a dependency on a custom fork that is not reproducible for users."
  - name: "No mirror at all"
    rejection_reason: "Prohibits feasibility testing of future features, defeating the integration lab's purpose."
evidence:
  - "Spec section 2.1."
  - "ADR 0004 (integration lab mirror)."
---

# ADR 0011: MVP Prohibits Mirror-Only Host Capabilities

## Context

ADR 0004 establishes magalz/luminalshine-mirror as an integration lab for probing and experimenting with host behavior. Some of what the lab learns may describe behavior that exists only in the mirror - features CandelaMoon itself added there for testing - and not in official LuminalShine releases. Spec section 2.1 frames host compatibility for the MVP. If an MVP feature depended on such mirror-only behavior, every user would need a custom host fork to run the product, which is not reproducible and not a product.

## Decision

The MVP may consume only capabilities available in official LuminalShine releases, and no MVP feature depends on luminalshine-mirror-only behavior. The alternatives were rejected: allowing mirror capabilities into the MVP creates a dependency on a custom fork that users cannot reproduce, and having no mirror at all prohibits the feasibility testing that future features depend on. The evidence is spec section 2.1 and ADR 0004.

## Consequences

Every MVP feature is reproducible for any user running an official LuminalShine release, which keeps the product honest and testable in the wild. Mirror experiments are documented as future work and tracked through the disposition process (ADR 0012, defer-host-dependent) instead of silently shipping. The validation discipline follows: anything proven in the mirror must be re-confirmed against an official release before it can enter MVP scope, and the mirror remains valuable for post-MVP feasibility studies where mirror-only findings are expected inputs to future ADRs.

## Alternatives

### Allow Mirror Capabilities in MVP

An MVP that requires mirror-only host behavior ships a product that only works with a custom fork. Rejected.

### No Mirror at All

Without an integration lab, host-dependent features could not be feasibility-tested at all, and their ADRs would rest on speculation. Rejected.
