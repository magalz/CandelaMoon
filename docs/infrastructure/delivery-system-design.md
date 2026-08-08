# Delivery System Design

This document is the master integration reference for the CandelaMoon delivery system. Each section links to the detailed infrastructure document that owns the specifics; this document does not duplicate that content.

## Repository

- Owner: magalz
- Visibility: public
- Branch protection model: branch protection rulesets on the default branch
- Default branch: moonlight-noir (current)
- Protected: no direct pushes, required reviews, required statuses

## Branch

- Branch naming: `<type>/<phase>-<capability>-<short-purpose>`
- Draft PR opened after first meaningful commit
- Every phase ends with phase-audit PR
- Cross-repo changes use shared change ID and paired PRs

## CI

- Reference: ci-architecture.md
- Pipeline tiers: per-commit, per-PR, nightly, release-candidate
- Containerized (Podman): container jobs
- Host-bound: device tests (Google TV Streamer), Windows (LuminalShine), signing

## Synchronization

- GitHub/Memtrace split authority.
- Synchronization state tuple: repository + branch + base SHA + local HEAD + remote branch head + working-tree diff hash + Memtrace indexed commit + Memtrace overlay episode.
- Five gates: before work, during work, before review, before merge, after merge.
- Stop-work rule and repair mode.
- Reference: ADR 0013.

## TDD

- Red-green-refactor for features and bugs.
- Characterization tests for refactors.
- Reachability/contract tests for deletions.
- Documentation and infrastructure-policy changes exempt from synthetic failing tests.
- PR links red and green evidence.

## Review

- Seven-gate review stack: automated, Memtrace, acceptance, edge-case, blind, security, policy.
- Severity rules: critical/high cannot be self-waived.
- Waiver requires independent approval, rationale, compensating controls, owner, expiry.
- Reviewer independence definition: fresh context, no participation in authoring.

## Toolchain

- Reference: toolchain-pins.md
- Summary: JDK 17, Android SDK 36/34/28, NDK 27, Gradle 8.13, Podman, Python 3.11.

## Device Lab

- Reference: device-lab-architecture.md
- Summary: Google TV Streamer primary, API 28-30 compatibility tier, Windows host for LuminalShine.

## Supply Chain

- Reference: supply-chain-policy.md
- Summary: SHA-pinned actions, digest-pinned images, SBOMs, SLSA L3 target.

## Secrets and Signing

- Reference: secrets-and-signing-policy.md
- Summary: GitHub Secrets/Environments, offline signing.

## Operational

- Reference: retention-cache-cost-maintenance-policy.md
- Summary: retention, cache, cost, maintenance cadence.

## Incident

- Reference: incident-and-rollback-policy.md
- Summary: bad-release, compromised-dependency, stale-graph procedures.

## Agent Architecture

- Reference: spec section 15, `.maestro-space/maestro-docs/maestro-orchestrator-guide.md` (the framework operationalizes the agent architecture; this file is the product-side summary)
- Summary: 7 production agents (Senior Developer, QA Architect, DevOps Architect, Security Analyst, GRC Architect, Tech Writer, UX/UI Designer) and 5 review agents (Blind Hunter, Edge Case Hunter, Acceptance Analyst, Red Team, Blue Team). Handoff protocol connects agents. Session handouts prevent context rot.
- Orchestrator guide: `.maestro-space/maestro-docs/maestro-orchestrator-guide.md` defines the dispatch matrix, handoff file protocol, context scoping, review pipeline, and task execution flow. (The legacy `docs/infrastructure/orchestrator-guide.md` was removed in the 2026-08-07 restructure; the maestro version is authoritative.)
- ADRs: 0015 (multi-agent architecture), 0016 (ATDD red-phase), 0017 (two-phase review), 0018 (red/blue team), 0019 (coverage audit with Memtrace), 0020 (session handout). Each ADR's `## Framework reference` section points to the corresponding `.maestro-space/` doc.
