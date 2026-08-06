---
id: "0003"
title: "Artemis Baseline Freeze"
status: accepted
date: "2026-08-05"
context: "CandelaMoon is derived from Artemis, itself a Moonlight fork, and upstream Artemis continues to evolve. CandelaMoon makes targeted changes - a new app identity, TV-only scope, and eventual mobile removal - that conflict with ongoing upstream movement. Spec section 2.2 defines how the upstream baseline is managed. The user chose during brainstorming on 2026-08-05 to treat Artemis strictly as a starting point."
decision: "Artemis is a frozen source baseline. No routine future Artemis merges. CandelaMoon owns protocol, decoder, platform, and security upkeep from this point forward."
consequences: "No merge conflicts with upstream drift, but CandelaMoon must own upstream fixes: protocol updates, decoder vulnerabilities, platform compatibility, and security patches."
alternatives:
  - name: "Selective upstream intake"
    rejection_reason: "The user chose a full freeze; selective intake reintroduces merge decisions and upstream drift."
  - name: "Regular upstream merges"
    rejection_reason: "Conflicts with the targeted changes and the mobile removal this project performs."
evidence:
  - "Spec section 2.2."
  - "User decision during brainstorming on 2026-08-05."
---

# ADR 0003: Artemis Baseline Freeze

## Context

CandelaMoon starts from Artemis, an open-source Android streaming client that is itself a fork of Moonlight, the NVIDIA GameStream client. Upstream Artemis continues to evolve with its own roadmap, but CandelaMoon applies targeted changes - a new application identity (ADR 0005), a TV-only scope with phased mobile removal (ADR 0006), and evidence-based deletions (ADR 0012) - that increasingly diverge from upstream. Merging upstream on a regular basis would mean repeatedly resolving conflicts between upstream movement and CandelaMoon's own direction. Spec section 2.2 defines how the upstream baseline is managed, and the user chose during brainstorming on 2026-08-05 to freeze the baseline.

## Decision

Artemis is a frozen source baseline: there are no routine future Artemis merges. CandelaMoon owns protocol, decoder, platform, and security upkeep from this point forward. The alternatives were rejected: selective upstream intake would reintroduce the very merge decisions and upstream drift the freeze eliminates, and regular upstream merges conflict directly with the targeted changes and the mobile removal this project performs. The evidence is spec section 2.2 and the user's choice during brainstorming on 2026-08-05.

## Consequences

The codebase no longer churns against upstream, which removes merge conflicts and drift as a recurring cost. The trade is a real maintenance obligation: when upstream Artemis fixes a decoder bug, a security vulnerability, or a platform compatibility issue, the fix is CandelaMoon's responsibility to identify, port, or re-implement itself. The freeze is not a wall - nothing forbids cherry-picking a specific upstream fix as a deliberate, reviewed act - but routine synchronization is off the table, and every upstream-related decision is made consciously and documented rather than absorbed automatically.

## Alternatives

### Selective Upstream Intake

Hand-picking upstream changes preserves some upstream value but reintroduces merge decisions, conflict resolution, and drift tracking for every candidate change. The user chose a full freeze instead. Rejected.

### Regular Upstream Merges

Synchronizing with upstream on a schedule conflicts with the targeted changes and the mobile removal CandelaMoon performs; conflict resolution would become a permanent tax on development. Rejected.
