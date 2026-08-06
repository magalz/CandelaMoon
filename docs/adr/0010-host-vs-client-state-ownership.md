---
id: "0010"
title: "Host vs. Client State Ownership"
status: accepted
date: "2026-08-05"
context: "A streaming client and its host share responsibility for state: sessions, libraries, capabilities, and settings live on the host, while navigation, profiles, and presentation live on the client. Spec section 2.5 defines the UI approach and, implicitly, what the client owns. The boundary decides which features are client-side and which must go through the host."
decision: "LuminalShine owns host, session, library, and capability semantics. CandelaMoon owns TV navigation, local profiles, presentation, accessibility, diagnostics, and client-side input - as long as it does not invent host state."
consequences: "Feature classification is deterministic: anything that invents host state is out of scope or deferred as host-dependent. Client-local UX proceeds without host contract changes."
alternatives:
  - name: "Host contract for everything"
    rejection_reason: "Every client feature, including client-local UX, would need a host counterpart."
  - name: "Full client autonomy"
    rejection_reason: "The client may add any behavior as long as the protocol works, which risks inventing host state."
evidence:
  - "Spec section 2.5."
---

# ADR 0010: Host vs. Client State Ownership

## Context

A streaming product is a pair: the client (CandelaMoon on Android TV) and the host (LuminalShine on a PC). State is split between them - the host owns sessions, libraries, capabilities, and host settings, while the client owns everything the user touches locally: navigation, profiles, presentation, and diagnostics. Spec section 2.5 defines the UI approach and, implicitly, what the client owns. Without an explicit boundary, feature work constantly asks the same question: does this feature live in the client, in the host, or in a contract change?

## Decision

LuminalShine owns host, session, library, and capability semantics. CandelaMoon owns TV navigation, local profiles, presentation, accessibility, diagnostics, and client-side input - as long as it does not invent host state. The alternatives were rejected: making the host contract cover everything would force every client feature, including client-local UX, to have a host counterpart, and granting the client full autonomy - any behavior as long as the protocol works - risks inventing host state that the host does not know about. The evidence is spec section 2.5.

## Consequences

Feature classification becomes deterministic: a feature that invents host state is either out of scope or deferred as host-dependent (the defer-host-dependent disposition in ADR 0012), while client-local UX work proceeds without host contract changes. Diagnostics and accessibility get a clear client-side home, which is unusual in Moonlight-derived code and must be designed deliberately rather than assumed. The boundary is reviewed whenever a new feature lands, and any feature that straddles it is escalated for a decision instead of silently placed.

## Alternatives

### Host Contract for Everything

Routing every feature through the host contract would make the host the bottleneck for client-local concerns like navigation and presentation. Rejected.

### Full Client Autonomy

Allowing the client any behavior that keeps the protocol working lets the client invent host state, creating inconsistency between what the host knows and what the client assumes. Rejected.
