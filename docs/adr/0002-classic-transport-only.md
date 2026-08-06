---
id: "0002"
title: "Classic Moonlight/GameStream Transport Only"
status: accepted
date: "2026-08-05"
context: "LuminalShine exposes two streaming paths per its architecture documentation: an inherited classic Moonlight/GameStream transport and a WebRTC path. CandelaMoon inherits from Artemis, which is a classic-transport client. Spec section 2.1 scopes the streaming transport. The user decided during brainstorming on 2026-08-05 that the classic transport is the only one in product scope."
decision: "CandelaMoon uses the inherited classic Moonlight/GameStream transport only. WebRTC is outside product scope. Reconsidering requires a new product design and a superseding ADR."
consequences: "Streaming features rest on a proven transport inherited from Moonlight. WebRTC-dependent host features cannot be consumed and must be deferred or dropped."
alternatives:
  - name: "Both classic and WebRTC in v1"
    rejection_reason: "Doubles the transport scope, and no proven Android TV WebRTC client exists to build on."
  - name: "WebRTC replaces classic"
    rejection_reason: "Removes the only proven transport while no WebRTC client code exists to inherit."
evidence:
  - "Spec section 2.1."
  - "LuminalShine docs/architecture.md documenting the two streaming paths."
  - "User decision during brainstorming on 2026-08-05."
---

# ADR 0002: Classic Moonlight/GameStream Transport Only

## Context

A streaming client negotiates with its host over a transport that carries video, audio, and input. CandelaMoon's host, LuminalShine, documents two streaming paths in its architecture documentation: the inherited classic Moonlight/GameStream transport and a WebRTC path. CandelaMoon inherits its client implementation from Artemis, which is a classic-transport client, so the classic transport already exists, is proven in the wild, and has years of client code behind it. Spec section 2.1 scopes the streaming transport for the product, and the user decided during brainstorming on 2026-08-05 that WebRTC is not part of CandelaMoon's product scope.

## Decision

CandelaMoon uses the inherited classic Moonlight/GameStream transport only, and WebRTC is outside product scope. Reconsidering WebRTC requires a new product design and a superseding ADR, not an incremental change. The alternatives were rejected: shipping both classic and WebRTC in v1 doubles the transport scope and there is no proven Android TV WebRTC client to build on, while replacing classic with WebRTC removes the only proven transport at a point where no WebRTC client code exists to inherit. The evidence is spec section 2.1, the LuminalShine architecture documentation showing both paths, and the user's decision during brainstorming on 2026-08-05.

## Consequences

Streaming features sit on a battle-tested transport with an existing client implementation, which lowers MVP risk substantially. The cost is that any host features that depend on the WebRTC path cannot be consumed by CandelaMoon and must be classified as deferred or dropped under the disposition process (ADR 0012). If LuminalShine or the product strategy shifts toward WebRTC in the future, that becomes a fresh product decision requiring a new design effort, not an implementation detail that can be quietly added.

## Alternatives

### Both Classic and WebRTC in v1

Maintaining two transports in the first release doubles the scope of streaming work, and no proven Android TV WebRTC client exists to build on, so the risk is unquantified. Rejected.

### WebRTC Replaces Classic

Dropping the classic transport removes the only proven path while no WebRTC client code exists to inherit, leaving CandelaMoon without a working streaming stack. Rejected.
