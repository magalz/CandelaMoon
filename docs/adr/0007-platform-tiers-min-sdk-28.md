---
id: "0007"
title: "Platform Tiers with minSdk 28"
status: accepted
date: "2026-08-05"
context: "Android TV devices span Android 9 (API 28) through current releases. Spec section 2.4 defines platform support. The user decided during brainstorming on 2026-08-05 to set the floor at API 28 while making API 31+ the primary tier."
decision: "minSdk is API 28. API 31+ is the primary product tier; API 28-30 is a compatibility tier guaranteeing the core streaming journey. One adaptive UI serves both tiers, and unsupported enhancements are capability-gated."
consequences: "The largest install base is retained while the product optimizes for modern devices. Testing spans both tiers with a clear priority."
alternatives:
  - name: "Keep API 21"
    rejection_reason: "Highest maintenance cost, including four input capture providers to support."
  - name: "Require API 31"
    rejection_reason: "Excludes Android TV 9-11 devices; the user chose an API 28 floor with API 31 as primary."
evidence:
  - "Spec section 2.4."
  - "User decision during brainstorming on 2026-08-05."
---

# ADR 0007: Platform Tiers with minSdk 28

## Context

Android TV devices in the field span Android 9 (API 28) through the current platform releases. Choosing a single minimum SDK is a trade between install base and maintenance: a low floor reaches more devices but forces support for older platform quirks, while a high floor simplifies development but excludes older TVs. Spec section 2.4 defines platform support for the product, and the user decided during brainstorming on 2026-08-05 to set the floor at API 28 with API 31+ as the primary tier.

## Decision

minSdk is API 28. API 31+ is the primary product tier, fully featured and optimized. API 28-30 is a compatibility tier that guarantees the core streaming journey - the essential path from launching the app to streaming a session - but not every enhancement. One adaptive UI serves both tiers (ADR 0008), and unsupported enhancements are capability-gated rather than duplicated. The alternatives were rejected: keeping API 21 would impose the highest maintenance cost, including four input capture providers to support, and requiring API 31 would exclude Android TV 9-11 devices outright. The evidence is spec section 2.4 and the user's decision during brainstorming on 2026-08-05.

## Consequences

The largest possible Android TV install base is retained while the product optimizes for modern devices, and testing effort is prioritized: primary-tier devices are fully verified, compatibility-tier devices are verified on the core streaming journey. Capability gating keeps the product to a single UI rather than two codebases. One caveat: API 28-30 devices stop receiving platform security updates, so the compatibility tier's guarantee is scoped to the streaming journey, not to the platform's overall security posture.

## Alternatives

### Keep API 21

Supporting Android 5-era devices would reach the oldest hardware but at the highest maintenance cost, including four input capture providers and numerous platform workarounds. Rejected.

### Require API 31

A modern-only floor simplifies development but excludes Android TV 9-11 devices, which the user judged to be a significant part of the market. Rejected in favor of the 28-floor, 31-primary tiering.
