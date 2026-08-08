---
id: "0019"
title: "Coverage Audit with Memtrace Reconciliation"
status: accepted
date: "2026-08-05"
context: "A task is not done when code is written; it must be verified. Spec section 15.2 defines exit gates. Coverage auditing must reconcile what changed against what was documented, which requires more than counting tests."
decision: "The QA Architect runs a coverage audit with Memtrace reconciliation (detect_changes, get_evolution, get_episode_replay) as the exit gate per task. The rating is pass, conditional-pass, or fail. A fail returns the work to development with coverage tasks."
consequences: "Every task has a verifiable exit gate; coverage claims are reconciled against actual graph changes; conditional-pass is explicit and tracked."
alternatives:
  - name: "No coverage audit"
    rejection_reason: "No gate between development and UAT."
  - name: "Coverage audit without Memtrace"
    rejection_reason: "No reconciliation of what changed versus what was documented."
evidence:
  - "Spec section 15.2."
---

# ADR 0019: Coverage Audit with Memtrace Reconciliation

## Context

A task is not done when the code compiles; it is done when the change is verified and documented. Spec section 15.2 defines exit gates for the project. The problem with a naive coverage check is that it cannot tell whether the tests actually cover what changed - a task can report 100 percent coverage on the wrong surface, or documentation can claim behavior that was never shipped.

## Decision

The QA Architect runs a coverage audit as the exit gate for every task, using Memtrace reconciliation - detect_changes, get_evolution, and get_episode_replay - to compare what actually changed in the graph against what the task claims to have changed and tested. The audit rating is pass, conditional-pass, or fail; a fail returns the work to development with concrete coverage tasks. The alternatives were rejected: having no coverage audit leaves no gate between development and UAT, and auditing coverage without Memtrace cannot reconcile what changed against what was documented. The evidence is spec section 15.2.

## Consequences

Every task has a verifiable, repeatable exit gate, so "tested" cannot silently mean "untested code shipped". Memtrace reconciliation grounds the audit in the actual graph - symbol changes, episode history, and impact - rather than in self-reported test counts, and it keeps coverage claims honest under ADR 0013's split authority: the audit cites the same evidence trail the project trusts elsewhere. Conditional-pass is an explicit, tracked state with named follow-up tasks rather than an informal gray zone, and a fail loops back with actionable coverage tasks, making the gate corrective rather than punitive.

## Alternatives

### No Coverage Audit

Without an exit gate, work flows straight from development to UAT with no verification checkpoint. Rejected.

### Coverage Audit Without Memtrace

An audit that cannot reconcile what changed versus what was documented misses gaps where tests and documentation describe different surfaces. Rejected.

**Framework reference**: This ADR is operationalized in .maestro-space/maestro-docs/maestro-orchestrator-guide.md §5 step 10 (Coverage Audit) and .maestro-space/maestro-templates/coverage-audit.md (the audit template). Every task's coverage audit is recorded at .maestro-space/maestro-works/<phase>/<task>/coverage-audit.{md,json}.
