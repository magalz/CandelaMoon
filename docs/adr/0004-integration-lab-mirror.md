---
id: "0004"
title: "luminalshine-mirror as Integration Lab"
status: accepted
date: "2026-08-05"
context: "CandelaMoon's MVP may only depend on official LuminalShine behavior (ADR 0011), but some features need to be probed against host behavior before they can be specified. Spec section 3.2 defines the integration-lab role of magalz/luminalshine-mirror, a private fork used for documentation, contract probes, and experiments."
decision: "magalz/luminalshine-mirror is an integration lab for documentation, contract probes, and experiments. It never replaces official LuminalShine. Push to upstream is disabled locally so experimental changes cannot leak upstream."
consequences: "Host-dependent features can be feasibility-tested before specification, but findings must be re-validated against official releases before they count as evidence."
alternatives:
  - name: "Documentation mirror only"
    rejection_reason: "Prohibits feasibility testing of host-dependent features, which is the mirror's main purpose."
  - name: "Upstream PR first"
    rejection_reason: "Cannot assume upstream acceptance; experiments must not block on upstream review."
evidence:
  - "Spec section 3.2."
---

# ADR 0004: luminalshine-mirror as Integration Lab

## Context

CandelaMoon's MVP may only depend on capabilities that exist in official LuminalShine releases (ADR 0011), yet some planned features depend on host behavior that is undocumented or uncertain. Specifying such features requires probing the host: reading its code, testing contract behavior, and running experiments. Spec section 3.2 assigns this role to magalz/luminalshine-mirror, a private fork of LuminalShine that CandelaMoon's development can use without touching the official project.

## Decision

magalz/luminalshine-mirror is an integration lab for documentation, contract probes, and experiments. It never replaces official LuminalShine, and push to upstream is disabled locally so experimental changes cannot leak into the official project. The alternatives were rejected: a documentation-only mirror would prohibit the feasibility testing that is the mirror's main purpose, and an upstream-PR-first workflow cannot be assumed to succeed - experiments must not block on upstream review. The evidence is spec section 3.2.

## Consequences

Host-dependent features can be feasibility-tested before specification, which makes later ADRs and dispositions (ADR 0012) evidence-based instead of speculative. The discipline this creates: anything learned in the mirror must be re-validated against an official LuminalShine release before it counts as evidence, because the mirror may drift from official behavior; anything that remains mirror-only is kept out of the MVP by ADR 0011 and tracked as future work. The mirror also becomes the shared reference for contract fixtures, so both CandelaMoon and its test suite can point at concrete host behavior.

## Alternatives

### Documentation Mirror Only

A mirror that only carries documentation cannot answer feasibility questions about host behavior. It was rejected because probing and experimenting are the integration lab's core value.

### Upstream PR First

Submitting every probe or experiment as an upstream pull request assumes upstream acceptance and makes CandelaMoon's specification work depend on someone else's review queue. Rejected.
