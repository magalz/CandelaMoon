# Phase 1 Implementation Backlog

## Work Items

Ordered list of work items. Dependencies refer to prior IDs (P1-xxx).

### **P1-001: Create candelamoon-android Containerfile**

Description: Defines the containerized Android build environment (JDK 17, Android SDK, NDK, Gradle 8.13) used by all containerized CI tiers. Enables reproducible local and CI builds.

Dependencies: none. Complexity: M. Related ADR: 0014.

### **P1-002: Create candelamoon-docs Containerfile**

Description: Defines the containerized documentation build and validation environment, including the design validator. Used by the docs validate job in CI.

Dependencies: none. Complexity: S. Related ADR: 0014.

### **P1-003: Create candelamoon-security Containerfile**

Description: Defines the containerized security-scanning environment covering secret scan, dependency audit, and SBOM generation. Used by per-commit and per-PR security gates.

Dependencies: none. Complexity: M. Related ADR: 0014.

### **P1-004: Create luminal-contract Containerfile**

Description: Defines the containerized contract-testing environment for Luminal contract fixtures. Provides a stable runtime for contract validation jobs.

Dependencies: none. Complexity: S. Related ADR: 0014.

### **P1-005: Build and publish images to GHCR with signatures**

Description: Builds all four images, publishes them to GitHub Container Registry, and signs them for supply-chain verification. Establishes the image release baseline for every CI tier.

Dependencies: P1-001 through P1-004. Complexity: M. Related ADR: 0014.

### **P1-006: Configure GitHub branch protection rulesets**

Description: Configures branch protection rulesets for the default branch moonlight-noir: no direct pushes, required reviews, required statuses. Enforces the delivery-model commit gates.

Dependencies: none. Complexity: S. Related ADR: 0013.

### **P1-007: Add PR template with task/phase/capability/evidence fields**

Description: Adds a pull-request template carrying task, phase, capability, and evidence fields. Standardizes the evidence and review documentation in every PR.

Dependencies: none. Complexity: S. Related ADR: 0015.

### **P1-008: Add issue and milestone templates**

Description: Adds issue and milestone templates aligned with the phase/capability model. Provides structured intake for phase planning and audit tracking.

Dependencies: none. Complexity: S. Related ADR: 0015.

### **P1-009: Create evidence-manifest YAML template**

Description: Creates the evidence-manifest YAML template used to link red/green TDD evidence in PRs. Forms the machine-readable contract for the evidence gates.

Dependencies: none. Complexity: S. Related ADR: 0013.

### **P1-010: Add per-commit CI workflow (lint, format, fast tests, docs validate, secret scan, Codecov)**

Description: Adds the per-commit CI workflow running lint, format, fast tests, docs validate, secret scan, and JaCoCo coverage upload to Codecov. Provides fast feedback on every commit. GitHub Actions workflow YAML at `.github/workflows/ci.yml`.

Dependencies: P1-001 through P1-005. Complexity: L. Related ADR: 0014.

### **P1-011: Add per-PR CI workflow (full tests, API-tier matrix, Memtrace sync check)**

Description: Adds the per-PR CI workflow running full tests, the API-tier matrix, and the Memtrace synchronization check. Serves as the required status gate for PR merge.

Dependencies: P1-010. Complexity: L. Related ADR: 0013, 0014.

### **P1-012: Add nightly CI workflow (emulator compat, dependency freshness, contract fixtures)**

Description: Adds the nightly CI workflow covering emulator compatibility, dependency freshness, and contract fixtures. Detects regressions the per-PR pipeline does not cover.

Dependencies: P1-010. Complexity: M. Related ADR: 0014.

### **P1-013: Add release-candidate CI workflow (device tests, signing, provenance)**

Description: Adds the release-candidate CI workflow running device tests, signing, and provenance generation. Produces the auditable release artifact trail.

Dependencies: P1-010. Complexity: L. Related ADR: 0014.

### **P1-014: Configure self-hosted runner for Google TV Streamer**

Description: Configures the self-hosted runner for the Google TV Streamer device. Enables host-bound device tests off GitHub-hosted runners.

Dependencies: none. Complexity: M. Related ADR: 0014.

### **P1-015: Configure self-hosted Windows runner for LuminalShine host integration**

Description: Configures the self-hosted Windows runner for LuminalShine host integration. Enables host-bound Windows tests off GitHub-hosted runners.

Dependencies: none. Complexity: M. Related ADR: 0014.

### **P1-016: Integrate Memtrace synchronization check into CI**

Description: Integrates the Memtrace synchronization check into CI, verifying the sync state tuple and gates. Prevents graph/commit drift from reaching review or merge.

Dependencies: P1-011. Complexity: M. Related ADR: 0013, 0019.

### **P1-017: Integrate design validator into candelamoon-docs image and CI**

Description: Integrates the design validator into the candelamoon-docs image and the per-commit CI docs validate job. Enforces design-doc validation on every commit.

Dependencies: P1-002, P1-010. Complexity: S. Related ADR: 0014.

### **P1-018: Canary PR proving all paths (containerized + device + Windows + evidence + sync)**

Description: Runs a canary PR exercising every pipeline path: containerized jobs, device tests, Windows host integration, evidence manifests, and synchronization gates. Proves the delivery system end to end.

Dependencies: P1-005 through P1-017. Complexity: M. Related ADR: 0014.

### **P1-019: Remove AppVeyor configuration (appveyor.yml)**

Description: Removes the legacy AppVeyor configuration once the new pipeline covers all its responsibilities. Completes the CI migration.

Dependencies: P1-018. Complexity: S. Related ADR: 0014.

### **P1-020: Phase 1 audit PR**

Description: Opens the phase-audit PR required at the end of every phase per the branch policy. Audits the delivery system against the phase plan and records the outcome.

Dependencies: P1-018. Complexity: S. Related ADR: 0015.

### **P1-021: Fix baseline unit test failures surfaced by Phase 0 CI (theme inflation + startup NPEs)**

Description: Fixes the pre-existing unit test failures first surfaced by the Phase 0 CI run on PR #3 (ci/github-app-bot, run 31125842788). Failing tests: `LayoutInflationTest.allLayoutsInflateSuccessfully` (InflateException on `app/src/main/res/layout/activity_app_view.xml` line 45 — component style requires `Theme.MaterialComponents` or a descendant, but the app theme does not derive from it); `SimpleStartupTest.testApplicationOnCreate` and `StartupCrashTest.testUiHelperCrash` (NullPointerException: `Cannot invoke "android.content.Context.getFilesDir()" because "this.mBase" is null` — app startup code touches Context in a mocked environment). Repair approach is at the orchestrator's discretion: fix the app theme/layout to satisfy MaterialComponents, harden the startup path against null Context, or replace the baseline tests with Robolectric-backed ones that exercise the startup path properly. Acceptance: `./gradlew testNonRoot_gameDebugUnitTest` (or the CI `test` job) is green on the default branch.

Dependencies: none. Complexity: M. Related ADR: 0014. Priority: HIGH — unblocks the CI gate for all subsequent P1 items (P1-010, P1-011, P1-017).
