---
id: "0005"
title: "New Application Identity, No Migration"
status: accepted
date: "2026-08-05"
context: "CandelaMoon inherits Artemis's application identity: package name, app label, pairing stores, settings databases, and host registrations. Spec section 2.3 defines product identity. The user decided during brainstorming on 2026-08-05 that CandelaMoon is a new product, not an Artemis upgrade."
decision: "CandelaMoon has a new application identity. No Artemis migration path exists: Artemis settings, pairings, and databases are never imported."
consequences: "Users start with a clean slate - no stale pairings or inherited mobile-era settings - but existing Artemis users must re-pair and reconfigure after installing."
alternatives:
  - name: "In-place Artemis upgrade"
    rejection_reason: "Preserves stale pairings and inherited state that contradicts the new identity and TV-only scope."
  - name: "New app with migration path"
    rejection_reason: "Adds import tooling scope to the MVP; the user chose a clean start."
evidence:
  - "Spec section 2.3."
  - "User decision during brainstorming on 2026-08-05."
---

# ADR 0005: New Application Identity, No Migration

## Context

CandelaMoon's source is inherited from Artemis, so it also inherits Artemis's application identity: the package name, app label, pairing stores, settings databases, and host registrations that identify an installation. Spec section 2.3 defines CandelaMoon as a new product with its own identity, and the user decided during brainstorming on 2026-08-05 that CandelaMoon is not an upgrade of Artemis but a clean start.

## Decision

CandelaMoon has a new application identity, and there is no Artemis migration path: Artemis settings, pairings, and databases are never imported. The alternatives were rejected: an in-place Artemis upgrade would preserve stale pairings and inherited state that contradict the new identity and TV-only scope, and a new app with a migration path would add import/export tooling to the MVP, which the user chose to avoid. The evidence is spec section 2.3 and the user's decision during brainstorming on 2026-08-05.

## Consequences

Users start with a clean slate: no stale pairings pointing at old hosts, no inherited settings that assume mobile form factors, no carryover database cruft. The cost is that anyone coming from Artemis must re-pair and reconfigure after installing CandelaMoon, and this is accepted as a feature, not a defect. The MVP also stays smaller because no migration tooling is built. App-store presence, signing keys, analytics attribution, and update channels all start fresh under the new identity, which makes the product's data story unambiguous from day one.

## Alternatives

### In-Place Artemis Upgrade

Upgrading an existing Artemis installation in place would carry stale pairings and inherited settings into a product with a different identity and scope. Rejected.

### New App with Migration Path

A migration path would make the transition smoother for Artemis users but adds import tooling scope to the MVP. The user chose a clean start. Rejected.
