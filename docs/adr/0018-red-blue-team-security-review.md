---
id: "0018"
title: "Red Team and Blue Team Security Review"
status: accepted
date: "2026-08-05"
context: "Security review that only finds weaknesses produces no fixes; review that only designs defenses misses attack surface. Spec section 15.2 defines the security review process. CandelaMoon handles credentials, pairing, and network traffic, so both attack discovery and mitigation design must be first-class."
decision: "The Red Team Analyst finds exploitable weaknesses using STRIDE and OWASP with concrete attack scenarios. The Blue Team Analyst then receives the red team findings and designs concrete implementable mitigations, assesses exploitability, confirms or rejects each finding, and checks whether mitigations introduce new risks."
consequences: "Findings arrive with attack scenarios and leave with implementable mitigations or explicit rejections; independent confirmation reduces false positives."
alternatives:
  - name: "Only offensive review"
    rejection_reason: "Findings without actionable mitigations are unactionable."
  - name: "Only defensive review"
    rejection_reason: "Less creative attack discovery without an adversarial pass."
evidence:
  - "Spec section 15.2."
---

# ADR 0018: Red Team and Blue Team Security Review

## Context

CandelaMoon is a network client: it stores pairing credentials, connects to hosts, and exchanges control and media traffic, which makes it a meaningful security surface. Spec section 15.2 defines the security review process. Security review has two halves that need different temperaments - discovering weaknesses requires an adversarial mindset, while designing fixes requires a defensive one - and both halves are needed for findings to be actionable.

## Decision

The Red Team Analyst finds exploitable weaknesses using STRIDE and OWASP with concrete attack scenarios. The Blue Team Analyst then receives the red team's findings and designs concrete, implementable mitigations; assesses each finding's exploitability; confirms or rejects it; and checks whether the mitigations introduce new risks. The pair runs sequentially inside Review Phase 2 (ADR 0017). The alternatives were rejected: offensive-only review produces findings without actionable mitigations, and defensive-only review lacks the creativity of an adversarial attack-discovery pass. The evidence is spec section 15.2.

## Consequences

Every finding arrives with an attack scenario and leaves with an implementable mitigation or an explicit rejection with reasons, so security review output is directly actionable for the Senior Developer. Independent confirmation by the blue team reduces the false positives reaching development, and the mitigation-risk check prevents fix-induced vulnerabilities - the classic case where the fix creates the next bug. The red/blue split also leaves an audit trail: each finding's lifecycle - discovered, assessed, confirmed or rejected, mitigated - is explicit.

## Alternatives

### Only Offensive Review

An offensive pass alone finds weaknesses but produces no fixes, leaving the developer to invent mitigations without guidance. Rejected.

### Only Defensive Review

A defensive pass alone is less creative at discovering attacks, so the surface is explored from only one direction. Rejected.

**Framework reference**: This ADR is operationalized in .maestro-space/maestro-docs/maestro-orchestrator-guide.md §4 (Phase 2: Sequential Security Review) and the post-phase templates in .maestro-space/maestro-templates/post-phase-{grc,qa,security,devops,summary}.md.
