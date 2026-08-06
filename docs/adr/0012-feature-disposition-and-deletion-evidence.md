---
id: "0012"
title: "Feature Disposition and Evidence-Based Deletion"
status: accepted
date: "2026-08-05"
context: "CandelaMoon's inherited codebase contains features that must be retained, adapted, or removed. Spec section 4.4 defines the feature disposition process. Deletion is destructive: callers may break, and removed features cannot be reinstated without archaeology."
decision: "Every feature gets a disposition from a fixed taxonomy: retain-client, adapt-to-luminal, consume-existing-host, drop-unsupported, drop-mobile, defer-host-dependent, or propose-client-only. No deletion happens without Memtrace impact and dead-code/relationship evidence, co-change data, timelines, characterization tests, a rollback strategy, and documentation updates."
consequences: "Deletion is slow and evidence-gated, which protects shared callers, but dead code persists until its disposition completes."
alternatives:
  - name: "Ad-hoc deletion"
    rejection_reason: "Risk of silently breaking callers and losing documented rationale."
  - name: "No deletion ever"
    rejection_reason: "Dead code accumulates and is maintained forever."
evidence:
  - "Spec section 4.4."
---

# ADR 0012: Feature Disposition and Evidence-Based Deletion

## Context

CandelaMoon inherits a large codebase whose features fall into different categories: some are kept as client-side features, some must be adapted to LuminalShine semantics, some map to capabilities the host already provides, and some are unsupported, mobile-only, or host-dependent. Spec section 4.4 defines the feature disposition process for the project. Deletion is the risky end of this spectrum: removing a feature can break callers elsewhere in the codebase, and once removed, a feature cannot be reinstated without archaeology, so deletion decisions need to be made on evidence rather than impulse.

## Decision

Every feature gets a disposition from a fixed taxonomy: retain-client, adapt-to-luminal, consume-existing-host, drop-unsupported, drop-mobile, defer-host-dependent, or propose-client-only. No deletion happens without Memtrace impact and dead-code/relationship evidence, co-change data, timelines, characterization tests, a rollback strategy, and documentation updates. The alternatives were rejected: ad-hoc deletion risks silently breaking callers and losing the documented rationale, while never deleting lets dead code accumulate and be maintained forever. The evidence is spec section 4.4.

## Consequences

Deletion becomes slow and evidence-gated - each removal is justified, documented, and reversible in principle, because characterization tests give the safety net that makes deletion safe and the rollback strategy means a deletion can be reverted without archaeology. The cost is that dead code persists until its disposition completes, so the repository stays larger for longer, and disposition work is real work that must be scheduled. The taxonomy also makes the project's intent legible: anyone reading the dispositions understands which features CandelaMoon owns, which the host provides, and which are deliberately gone.

## Alternatives

### Ad-Hoc Deletion

Deleting features as they appear irrelevant risks silently breaking callers and loses the rationale behind each removal. Rejected.

### No Deletion Ever

Retaining every inherited feature forever means dead code is compiled, linted, and maintained indefinitely. Rejected.
