---
id: "0016"
title: "ATDD Red Phase Before Implementation"
status: accepted
date: "2026-08-05"
context: "Behavior must be specified before code exists. Spec section 15.2 defines the testing process. Tests written after implementation tend to be shaped by the implementation rather than by intent."
decision: "The QA Architect creates TDD red-phase test scaffolds before any implementation. No scaffold passes before code exists. Implementation activates tests one at a time (red to green). Refactoring happens only while green."
consequences: "Tests encode intent first, progress is measurable per test, and refactoring is safe because it only happens while green."
alternatives:
  - name: "Tests after implementation"
    rejection_reason: "Tests get shaped by the implementation instead of by the intended behavior."
  - name: "No TDD"
    rejection_reason: "No behavioral safety net for refactors and deletions."
evidence:
  - "Spec section 15.2."
---

# ADR 0016: ATDD Red Phase Before Implementation

## Context

Behavior should be specified before code exists, so that implementation is an act of making failing tests pass rather than an act of invention. Spec section 15.2 defines the testing process for the project. The failure mode this ADR prevents is familiar: when tests are written after implementation, they tend to reflect what the code happened to do rather than what the product was supposed to do, which quietly locks in implementation accidents as behavior.

## Decision

The QA Architect creates TDD red-phase test scaffolds before any implementation begins, and no scaffold passes before code exists. Implementation activates tests one at a time, each moving from red to green, and refactoring happens only while green. The alternatives were rejected: writing tests after implementation lets the tests be shaped by the implementation instead of by intent, and skipping TDD entirely leaves no behavioral safety net for the refactors and evidence-based deletions this project performs (ADR 0012). The evidence is spec section 15.2.

## Consequences

Tests encode intent first, so deviations from the intended behavior surface the moment they are introduced rather than at the end. Progress is measurable per test - a task is not done until its scaffolds are green, which gives the QA Architect and the human orchestrator a concrete definition of done. Refactoring is safe because it only happens in a green state, and the red-to-green activation order keeps each change small and attributable. The contract this creates: implementation does not start until the scaffolds exist, and scaffolds are not relaxed to fit the code - the code changes to satisfy the scaffolds.

## Alternatives

### Tests After Implementation

Tests written after the fact encode what the implementation does, including its accidents, instead of the intended behavior. Rejected.

### No TDD

Without a red phase, there is no behavioral safety net for the refactors and deletions CandelaMoon's disposition process requires. Rejected.

**Framework reference**: This ADR is operationalized in .maestro-space/maestro-docs/maestro-orchestrator-guide.md §2.2 (Handoff File Structure) and .maestro-space/maestro-templates/atdd-checklist.md (the ATDD checklist template). The red-phase requirement is encoded in the handoff frontmatter 	dd_artifacts.red_phase_verified: true.
