---
id: "0001"
title: "LuminalShine-Only Host Compatibility"
status: accepted
date: "2026-08-05"
context: "CandelaMoon is a new Android TV streaming client derived from Artemis, itself a Moonlight/GameStream client fork. The open-source host ecosystem contains several mutually incompatible implementations - Apollo, Artemis, and generic Sunshine - whose behaviors differ from official LuminalShine releases. Spec section 2.1 frames host compatibility. During brainstorming on 2026-08-05 the user decided that CandelaMoon targets a single host."
decision: "CandelaMoon supports official LuminalShine releases only. No Apollo, Artemis, or generic-Sunshine host path is maintained or tested."
consequences: "One host means one test matrix and tailored features, but users on other hosts are out of scope. Supporting another host later requires a superseding ADR."
alternatives:
  - name: "Broad GameStream compatibility"
    rejection_reason: "Splits effort across divergent host behaviors and prevents tailoring to LuminalShine's actual semantics."
  - name: "LuminalShine-primary with graceful fallback"
    rejection_reason: "Fallback paths must still be maintained and tested, and their behavior is only guessable where host contracts diverge."
evidence:
  - "Spec section 2.1: host compatibility scope."
  - "User decision during brainstorming on 2026-08-05."
---

# ADR 0001: LuminalShine-Only Host Compatibility

## Context

CandelaMoon is a new Android TV streaming client for playing games and applications streamed from a PC host. It is derived from Artemis, which is itself a fork of Moonlight, the open-source NVIDIA GameStream client. On the host side the ecosystem is fragmented: Apollo, Artemis-as-a-host, and generic Sunshine builds coexist with the official LuminalShine releases, and their pairing flows, session behavior, and feature contracts differ from one another. Supporting every host would mean every feature must be tested against every host variant, and host-specific workarounds would accumulate wherever implementations diverge. Spec section 2.1 frames the host compatibility scope for the product, and during the brainstorming session on 2026-08-05 the user settled the direction: support a single host and support it well.

## Decision

CandelaMoon supports official LuminalShine releases only. No Apollo, Artemis, or generic-Sunshine host path is maintained or tested, so all compatibility work, contract probes, and test fixtures target official LuminalShine behavior. The alternatives were rejected deliberately: broad GameStream compatibility would split effort across divergent host behaviors and prevent tailoring features to the host's real semantics, while a LuminalShine-primary approach with graceful fallback would still require maintaining and testing every fallback path whose behavior can only be guessed wherever host contracts diverge. The evidence is spec section 2.1 and the user's explicit decision during brainstorming on 2026-08-05.

## Consequences

The main benefit is a deliberately small blast radius: one host means one test matrix, one set of contract fixtures, and one documented feature surface, which fits a solo-developed MVP. The cost is that users running Apollo, Artemis-host, or generic Sunshine fall outside the supported scope, and issues reported from those hosts are closed as unsupported rather than fixed. Supporting another host later requires a superseding ADR and a deliberate expansion of testing. This decision also anchors later ADRs: 0004 (the luminalshine-mirror integration lab) and 0011 (the MVP may not depend on mirror-only host capabilities).

## Alternatives

### Broad GameStream Compatibility

Targeting every GameStream-derived host multiplies the testing matrix and forces CandelaMoon to accommodate behaviors that contradict official LuminalShine semantics. The effort split prevents tailoring to any single host, so it was rejected.

### LuminalShine-Primary with Graceful Fallback

Treating LuminalShine as primary while degrading gracefully on other hosts still requires implementing, testing, and maintaining every fallback path. Because other hosts' behaviors are only observable rather than specified, fallbacks would be guesses - worse than a clear out-of-scope boundary.
