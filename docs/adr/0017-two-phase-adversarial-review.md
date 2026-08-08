---
id: "0017"
title: "Two-Phase Adversarial Review"
status: accepted
date: "2026-08-05"
context: "Independent review needs isolation: reviewers who see the developer's full context anchor to the developer's assumptions. Spec section 15.2 defines the review process. Security review additionally needs an ordering: mitigations are designed after attacks are discovered."
decision: "Review Phase 1 runs Blind Hunter, Edge Case Hunter, and Acceptance Analyst in parallel with no handoff access and need-to-know information only. Review Phase 2 runs Red Team then Blue Team sequentially for security. The orchestrator triages findings between phases."
consequences: "Functional and acceptance issues surface independently and early; security gets its own ordered pass; the orchestrator prevents finding fatigue."
alternatives:
  - name: "Single monolithic review"
    rejection_reason: "Reviewer fatigue and no independence between review roles."
  - name: "All reviewers in parallel including security"
    rejection_reason: "The blue team needs the red team's findings before designing mitigations."
evidence:
  - "Spec section 15.2."
---

# ADR 0017: Two-Phase Adversarial Review

## Context

Review quality depends on independence: a reviewer who sees the developer's full context tends to share the developer's assumptions and miss the same blind spots. Spec section 15.2 defines the review process for the project. Security review adds a second constraint: some findings only become actionable in order - attack discovery precedes mitigation design - so a flat all-at-once review cannot serve both goals.

## Decision

Review Phase 1 runs Blind Hunter, Edge Case Hunter, and Acceptance Analyst in parallel, with no handoff access and need-to-know information only, so each reviewer works from the specification rather than the developer's mental model. Review Phase 2 runs Red Team then Blue Team sequentially for security (ADR 0018). The orchestrator triages findings between phases, deciding what reaches the developer and what is dismissed with reasons. The alternatives were rejected: a single monolithic review produces reviewer fatigue and no independence between roles, and running all reviewers in parallel including security breaks the ordering the blue team needs. The evidence is spec section 15.2.

## Consequences

Functional, edge-case, and acceptance findings surface independently and early, before security work begins, which keeps the phases composable. Security gets its own ordered pass in which attack discovery and mitigation design are never mixed. Triage prevents finding fatigue - the orchestrator merges duplicates, rates severity, and routes only actionable findings to development, so review volume does not become noise.

## Alternatives

### Single Monolithic Review

One review pass covering all roles causes reviewer fatigue and destroys independence, because each role sees the others' conclusions. Rejected.

### All Reviewers in Parallel Including Security

Running security in parallel with everything else breaks the red-team-to-blue-team ordering; blue team cannot design mitigations before red team's attack scenarios exist. Rejected.

**Framework reference**: This ADR is operationalized in .maestro-space/maestro-docs/maestro-orchestrator-guide.md §4 (Review Pipeline Orchestration) and the review-templates in .maestro-space/maestro-templates/ (gent-findings-report.md, gent-activity-report.md). The two-phase structure (Phase 1 parallel + Phase 2 sequential) is defined there.
