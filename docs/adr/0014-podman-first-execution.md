---
id: "0014"
title: "Podman-First Execution"
status: accepted
date: "2026-08-05"
context: "Builds, tests, docs, contract fixtures, and security scans must run in a reproducible environment. Spec section 9.2 defines the execution environment. The user specified Podman during brainstorming on 2026-08-05; Docker compatibility is not required."
decision: "Podman is the default execution boundary for builds, tests, docs, contract fixtures, and security scans. Rootless, non-root, minimal capabilities, images pinned by digest, same image locally and in CI. Audited host-bound exceptions exist for real device tests, emulator acceleration, Windows host validation, and release signing."
consequences: "Reproducible, rootless execution that is identical locally and in CI; host-bound exceptions are limited and audited."
alternatives:
  - name: "Docker"
    rejection_reason: "The user specified Podman; Docker compatibility is not required."
  - name: "All-container including devices"
    rejection_reason: "Containers cannot validate real hardware behavior or Windows host behavior."
evidence:
  - "Spec section 9.2."
  - "User specification of Podman during brainstorming on 2026-08-05."
---

# ADR 0014: Podman-First Execution

## Context

CandelaMoon's development pipeline - builds, tests, documentation generation, contract fixtures, and security scans - must run in an environment that is reproducible across machines, or failures become indistinguishable from environment drift. Spec section 9.2 defines the execution environment for the project, and the user specified Podman during brainstorming on 2026-08-05, noting that Docker compatibility is not required.

## Decision

Podman is the default execution boundary for builds, tests, docs, contract fixtures, and security scans. Execution is rootless and non-root with minimal capabilities, images are pinned by digest, and the same image runs locally and in CI. A small set of audited host-bound exceptions exists for real device tests, emulator acceleration, Windows host validation, and release signing. The alternatives were rejected: Docker was not chosen because the user specified Podman and compatibility with Docker is not required, and an all-container approach including devices was rejected because containers cannot validate real hardware or Windows host behavior. The evidence is spec section 9.2 and the user's specification during brainstorming on 2026-08-05.

## Consequences

Execution becomes reproducible and rootless: the same image, pinned by digest, runs identically locally and in CI, which removes environment drift as a failure class and keeps privilege minimal by default. Host-bound exceptions are limited in number and audited, so the containerized default is the norm and any exception must justify itself. Windows-specific validation happens outside containers by design, because only real hardware and OS behavior can validate it. Image pinning means every toolchain update is a deliberate, reviewable change rather than an accidental one.

## Alternatives

### Docker

Docker provides similar isolation, but the user specified Podman and Docker compatibility is not a requirement. Rejected.

### All-Container Including Devices

Containerizing everything, including device testing, is impossible in practice: containers cannot validate real hardware behavior or Windows host behavior. Rejected.
