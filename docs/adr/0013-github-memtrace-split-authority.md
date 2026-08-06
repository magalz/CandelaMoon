---
id: "0013"
title: "GitHub and Memtrace Split Authority"
status: accepted
date: "2026-08-05"
context: "Two sources of truth exist in the project: the git repository (the source of accepted code) and Memtrace, the graph-based code intelligence index (the source of derived evidence such as symbol history, impact, decision provenance, and process provenance). Spec section 7.1 defines evidence and authority. Without an explicit split, the two can contradict each other with no rule for resolution."
decision: "GitHub PRs and commits are authoritative for accepted source. Memtrace is authoritative for derived architecture evidence: symbol history, impact, decision provenance, and process provenance. On conflict: stop, synchronize, regenerate evidence, and update normative records via PR. Memtrace never changes an approved decision alone; GitHub never declares graph facts current without matching Memtrace evidence."
consequences: "Both tools stay honest because each has authority over its own domain; conflicts become explicit escalation points rather than silent wins."
alternatives:
  - name: "Memtrace primary"
    rejection_reason: "The graph could contradict shipped code and there would be no rule to catch it."
  - name: "GitHub primary only"
    rejection_reason: "Memtrace becomes optional and the derived evidence trail degrades."
evidence:
  - "Spec section 7.1."
---

# ADR 0013: GitHub and Memtrace Split Authority

## Context

The project maintains two sources of truth. The git repository on GitHub holds the accepted source: every PR and commit is the authoritative record of what the code is. Memtrace maintains a graph-based index of the codebase that derives facts the repository does not directly state: symbol history, impact and blast radius, decision provenance, and process provenance. Spec section 7.1 defines how evidence and authority work in this project. Without an explicit authority split, the two can drift apart - a merged PR not reflected in the index, or an index fact contradicting the code - with no rule for which one wins.

## Decision

GitHub PRs and commits are authoritative for accepted source. Memtrace is authoritative for derived architecture evidence: symbol history, impact, decision provenance, and process provenance. When they conflict, the rule is to stop, synchronize, regenerate evidence, and update normative records via PR. Memtrace never changes an approved decision alone, and GitHub never declares graph facts current without matching Memtrace evidence. The alternatives were rejected: making Memtrace primary would let the graph contradict shipped code with no check, and making GitHub primary only would reduce Memtrace to an optional extra, letting the evidence trail degrade. The evidence is spec section 7.1.

## Consequences

Each tool holds a veto over its own domain, so both stay honest: code changes flow through PRs, and graph facts flow through evidence regeneration. Conflicts become explicit escalation points - an incident where the graph and the repo disagree triggers synchronization work rather than an argument about which tool wins. Regenerating evidence after rebases and merges becomes a standard step, not an exception. Decision provenance is recorded in Memtrace and mirrored into ADRs and PRs, so history survives whichever lens is used to read it.

## Alternatives

### Memtrace Primary

Treating the graph index as the source of truth lets it contradict shipped code, and there would be no rule to catch the contradiction. Rejected.

### GitHub Primary Only

Ignoring Memtrace as an authority makes it optional, and the derived evidence trail that supports deletions and impact claims degrades. Rejected.
