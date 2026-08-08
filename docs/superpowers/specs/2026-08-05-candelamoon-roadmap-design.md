# CandelaMoon Architecture And Delivery Roadmap Design

Status: Stakeholder-approved design; delivery-system reviews pending

Date: 2026-08-05

Repositories:

- CandelaMoon: `https://github.com/magalz/CandelaMoon`
- LuminalShine integration lab: `https://github.com/magalz/luminalshine-mirror`
- LuminalShine authority: `https://github.com/NortheBridge/luminalshine`

Initial evidence baselines:

- CandelaMoon branch: `moonlight-noir`
- CandelaMoon commit: `3397ec7750969466ad8983364ee1a33182bbffa1`
- LuminalShine branch: `main`
- LuminalShine commit: `3a4b94e6441c9ef988547d3eac9579b131c571aa`
- Memtrace repository IDs: `CandelaMoon`, `luminalshine`

## 1. Objective

CandelaMoon will become a TV-only Android client tailored to official LuminalShine releases. It starts from Artemis, which is itself derived from Moonlight Android, but it will not remain a general Artemis, Apollo, or Sunshine client.

The program will first establish two evidence-backed architecture spines and a complete host-to-client capability contract. Feature development begins only after that foundation defines what CandelaMoon can adapt, retain independently, drop, defer, or add later.

The program is designed for one developer. Work proceeds through small, dependency-ordered pull requests with explicit evidence and exit gates rather than calendar promises.

## 2. Product Boundaries

### 2.1 Host And Transport

- CandelaMoon supports official LuminalShine releases only.
- CandelaMoon uses the inherited classic Moonlight/GameStream-compatible transport.
- LuminalShine's browser-oriented WebRTC path is outside CandelaMoon's product scope. Reconsidering it requires a new product design and superseding ADR, not an ordinary roadmap change.
- MVP functionality may consume only capabilities already available in official LuminalShine.
- No MVP feature may depend on behavior that exists only in `luminalshine-mirror`.
- Host-dependent future ideas may be explored in the mirror after MVP, but they remain unavailable to the official-host product until the required host capability ships upstream.

### 2.2 Artemis Inheritance

- Artemis is a frozen source baseline. CandelaMoon will not perform routine future Artemis merges.
- CandelaMoon assumes ownership of protocol compatibility, decoder and device behavior, Android platform evolution, security fixes, native dependencies, and maintenance.
- Existing TV-relevant client-only Artemis features are retained unless evidence shows that they do not fit the product, architecture, maintainability standard, or MVP value.
- Apollo-specific features and unsupported host assumptions must be dispositioned explicitly rather than carried forward accidentally.

### 2.3 Application And Form Factor

- CandelaMoon uses a new application identity.
- Existing Artemis installations, pairings, databases, and settings are not migrated.
- Android TV is the only supported form factor.
- Phone, tablet, touch-first, portrait, foldable, DeX, and external-display-controller behavior will be classified first and removed in controlled phases.
- Removing mobile behavior must not be conflated with removing decoder, controller, protocol, or hardware compatibility code.

### 2.4 Android Platform Tiers

- `minSdk` remains API 28 so Android TV 9-11 devices can install the app.
- API 31 and newer form the primary product tier.
- API 28-30 form a compatibility tier.
- API 28-30 must support the core journey: discover, pair, browse, launch, stream, control, recover, and disconnect.
- API 31+ may receive richer controller, performance, visual, and platform capabilities without being limited by the compatibility tier.
- Unsupported enhancements are capability-gated. Hide irrelevant controls; show a disabled control with a clear reason when discoverability matters.
- Every capability records its minimum API, fallback, test tier, and whether loss affects an enhancement or core streaming.

### 2.5 UI Direction

- CandelaMoon will replace the inherited UI with modern TV components.
- One adaptive UI serves both platform tiers. The project will not maintain separate modern and legacy screen trees.
- Constrained devices may use reduced effects, motion, density, or other presentation enhancements.
- Compose for TV is evaluated through an architecture decision and a bounded prototype before selection.
- The prototype must validate D-pad focus, focus restoration, accessibility, lifecycle, performance, and interoperability with the existing Java streaming activity.
- Streaming, JNI, MediaCodec, service, persistence, and input boundaries remain protected until separate evidence justifies changing them.

## 3. Repository Ownership

### 3.1 CandelaMoon

CandelaMoon owns:

- The client architecture spine.
- Architecture decision records.
- The LuminalShine integration profile.
- The cross-product capability contract.
- The inherited feature inventory and disposition ledger.
- The MVP product specification.
- The visual-system integration contract.
- The delivery roadmap and phase evidence.

The existing untracked `new-design/` material is non-authoritative local reference input for the future visual design system. It is not required to reproduce any architecture or product conclusion and is not authority for host semantics, protocol behavior, architecture, or implementation status. Every adopted decision must be restated with its rationale and evidence in tracked `DESIGN.md`, while every rejected or unresolved claim is recorded in a tracked visual-reference disposition ledger; downstream work may cite only those tracked artifacts.

### 3.2 LuminalShine Integration Lab

`magalz/luminalshine-mirror` is an integration lab that may contain:

- A commit-pinned observed host architecture spine.
- Documentation improvements.
- Contract probes and deterministic fixtures.
- Feasibility experiments for post-MVP host-dependent ideas.

The integration lab tracks official LuminalShine but does not replace it as product authority. Its code is never an implicit CandelaMoon runtime requirement.

The local checkout uses this remote safety model:

```text
origin    -> https://github.com/magalz/luminalshine-mirror.git
upstream  -> https://github.com/NortheBridge/luminalshine.git (fetch only)
```

Pushes to `upstream` must remain disabled locally to prevent accidental maintainer branches or pull requests.

### 3.3 Official LuminalShine

`NortheBridge/luminalshine` is the authority for official host behavior. Every host claim must identify the upstream release and commit from which it was observed. CandelaMoon does not assume that upstream will accept documentation or code contributions.

MVP support is an explicit allowlist of verified official releases, never `main`, `latest`, or an inferred version range. Phase 2 selects at least one tagged official release and records its immutable commit; a release is unsupported until its capability contract and required tests pass. A previously verified release remains supported only while it stays on the allowlist and continues to pass the compatibility suite.

## 4. Documentation Architecture

The architecture foundation is a connected evidence system rather than independent narrative documents.

### 4.1 CandelaMoon Artifacts

- `architecture-spine`: context, runtime containers, components, state ownership, trust boundaries, persistence, build variants, deployment, protected native boundaries, and maintenance risks.
- `feature-inventory`: every inherited Artemis behavior, including mobile-only and Apollo-specific behavior.
- `luminalshine-integration-profile`: commit-pinned observations of official host behavior relevant to a classic client.
- `capability-contract`: authoritative mapping from verified host capability to CandelaMoon behavior.
- `ADR set`: accepted decisions, alternatives, consequences, and supersession history.
- `product-spec`: MVP journeys, requirements, non-functional requirements, exclusions, and acceptance gates.
- `delivery-roadmap`: dependency-ordered implementation phases and PR units.
- `DESIGN.md`: tracked visual tokens, components, states, focus, accessibility, and accepted visual debt derived from `new-design/`.

### 4.2 LuminalShine Mirror Artifacts

The mirror augments, rather than blindly duplicates, LuminalShine's existing `architecture.md` and `docs/architecture.md`. Its client-relevant spine covers:

- NVIDIA HTTP discovery, pairing, capabilities, app catalog, and launch control.
- RTSP and session lifecycle.
- Stream negotiation.
- Capture, encode, audio, and input replay boundaries.
- Virtual-display orchestration that affects client-visible behavior.
- Client-visible configuration, state, version behavior, and errors.
- Authentication and trust boundaries.

Installer, WebRTC, web administration, Playnite, driver, and unrelated host internals receive only enough context to explain classic-client effects.

### 4.3 Shared Capability Taxonomy

Both spines use these domains:

1. Identity, install, and trust.
2. Discovery and pairing.
3. Host metadata and capability negotiation.
4. App catalog and artwork.
5. Launch, resume, quit, and session ownership.
6. Stream configuration and transport.
7. Video, audio, HDR, codec, and display behavior.
8. Controller, keyboard, mouse, touch protocol, and feedback.
9. In-stream controls and recovery.
10. Local profiles and settings.
11. Diagnostics, logs, and compatibility reporting.
12. Android TV launcher, focus, lifecycle, and updates.

### 4.4 Capability Contract Schema

Every capability row contains:

- Stable capability ID and domain.
- User value.
- Official upstream release and commit evidence.
- Host contract or protocol evidence.
- Current CandelaMoon implementation and source evidence.
- State owner.
- Disposition and rationale.
- MVP status.
- Minimum API and platform tier.
- Fallback and degraded behavior.
- Error states and recovery.
- Security and privacy notes.
- Test evidence.
- Confidence and evidence status.
- Related ADR, task, branch, PR, commit, and Memtrace records.

Allowed dispositions are:

- `retain-client`
- `adapt-to-luminal`
- `consume-existing-host`
- `drop-unsupported`
- `drop-mobile`
- `defer-host-dependent`
- `propose-client-only`

No inherited or proposed feature may be silently omitted.

Completeness uses machine-readable source inventories as denominators. At minimum, the reconciliation covers tracked source-defined features, activities and services, settings and preference keys, build variants, manifest capabilities, UI routes, resources tied to supported behavior, protocol operations and extensions, host API or control routes, test fixtures, and every feature claimed by tracked product documentation. Each inventory item maps to exactly one capability row or to an explicitly justified non-capability exclusion; duplicate, missing, and orphan mappings fail the documentation checks.

## 5. Evidence And Decision Flow

### 5.1 Capability Evidence Packet

Each capability area is processed in this order:

```text
pin upstream version
-> map LuminalShine behavior and protocol evidence
-> map inherited CandelaMoon behavior and dependencies
-> identify state owner and semantic mismatch
-> assign feature disposition
-> define API-tier fallback and errors
-> attach verification evidence
-> approve the row or create an ADR
```

### 5.2 Evidence Hierarchy

Use evidence in this order:

1. Executable protocol behavior and tests.
2. Source symbols and call relationships.
3. Configuration and default definitions.
4. Current official documentation.
5. Existing `new-design/` claims.
6. Explicitly labeled inference.

Every claim is marked `verified`, `inferred`, `stale`, or `unknown`. An unknown may defer a capability, but it cannot justify deleting code.

### 5.3 Mapping Discipline

- Pin official LuminalShine before every compatibility mapping cycle.
- Record mirror branch and upstream base.
- Exclude vendored and generated trees from architecture scoring before relying on community, centrality, dead-code, or complexity analysis.
- Produce C4-style context, container, and component views plus sequence diagrams for core runtime journeys.
- Trace every architecture component to source paths, symbols, tests, capability IDs, and Memtrace evidence.
- Treat discovery, pairing, app enumeration, launch, negotiation, active stream, input and feedback, failure recovery, and shutdown as primary runtime flows.
- Map paired hosts, identity and certificates, preferences, local profiles, artwork cache, and host-owned session/app state separately.
- Document trust boundaries because a paired client controls a host capable of launching processes and injecting input.

### 5.4 Initial ADR Register

The initial register covers:

- LuminalShine-only compatibility.
- Classic transport and WebRTC exclusion.
- Frozen Artemis baseline.
- Integration-lab mirror role.
- New application identity and no migration.
- TV-only scope and phased mobile removal.
- API 31+ primary tier with API 28-30 core fallback.
- Single adaptive UI.
- Compose for TV evaluation criteria.
- Host-state and client-state ownership.
- MVP prohibition on mirror-only host capabilities.
- Feature disposition and deletion evidence policy.
- GitHub and Memtrace split authority and synchronization gate.
- Podman-first execution and audited host-bound exceptions.
- Multi-agent architecture and handoff protocol.
- ATDD red-phase-before-implementation.
- Two-phase adversarial review (adversarial then security).
- Red/blue team security review approach.
- Coverage audit with Memtrace reconciliation as exit gate.
- Session handout for context continuity.

### 5.5 Upstream Movement

A capability contract applies only to its pinned official LuminalShine baseline. A later release triggers a compatibility refresh:

1. Pin and index the new upstream release.
2. Diff client-visible host behavior.
3. Update affected capability rows and ADR assumptions.
4. Run contract and integration tests.
5. Publish a compatibility note.

This is an ongoing maintenance process rather than a full remap.

## 6. Error Model

Errors are classified by owner:

- `client-platform`: Android, UI, device, controller, decoder, storage, or lifecycle failure.
- `network`: discovery, reachability, TLS, timeout, loss, or interruption.
- `pairing-trust`: PIN, certificate, identity, concurrent pairing, rejection, or stale trust.
- `host-capability`: official LuminalShine does not expose or permit the behavior.
- `host-session`: launch, active-session conflict, process exit, display preparation, or host failure.
- `stream-negotiation`: codec, HDR, resolution, frame rate, audio, or protocol mismatch.
- `compatibility-contract`: unrecognized host version, response, or behavior that contradicts the pinned contract.
- `internal`: invariant violation or otherwise unknown client state.

Rules:

- Preserve host evidence in diagnostics while presenting concise, client-owned recovery text.
- Never silently substitute behavior that changes semantics.
- Automatic fallback is permitted only when the capability contract declares the alternatives equivalent.
- A core-journey failure offers one safe recovery action and one deterministic route back.
- Unknown host behavior fails closed for destructive actions and degrades safely for read-only metadata.
- Logs are local, structured, privacy-reviewed, and exportable only after secrets, certificates, tokens, addresses, and personal paths are redacted.

## 7. Split Authority And Synchronization

### 7.1 Authority Model

- GitHub pull requests and commits are authoritative for accepted source state.
- Tracked ADRs, capability records, specifications, and architecture documents in GitHub are normative decisions.
- Memtrace is authoritative for derived architecture evidence, symbol history, change impact, decision provenance, and process provenance.
- Documentation links both authorities.

Required provenance includes repository, branch, PR, commit SHA, Memtrace `repo_id`, indexed SHA, episode IDs, analysis time, affected symbols, impact rating, and verification results.

When normative GitHub records and derived Memtrace evidence conflict, neither silently overwrites the other. Work stops, the source and index are synchronized, the derived evidence is regenerated, and then a new PR updates any normative record that the corrected evidence disproves. Memtrace never changes an approved decision by itself; GitHub never declares graph-derived facts current without matching Memtrace evidence.

### 7.2 Stop-Work Rule

All product development halts whenever local Git, GitHub, and Memtrace do not describe the same intended branch state. A stale, partial, failed, ambiguous, or mismatched graph is a blocking incident, not a warning.

The mismatch must be diagnosed, repaired, reindexed, and revalidated before reading the graph for decisions or changing code.

Only synchronization repair work may proceed while stopped. Repair mode permits read-only Git diagnostics, Memtrace diagnostics, index/watch configuration, reindexing, and a dedicated infrastructure fix branch when code is required to restore the control itself. Repair work cannot change product behavior, must preserve raw diagnostics, requires independent review, and ends only when the synchronization canary passes. If Memtrace is unavailable, product work waits; no waiver or substitute reference search may authorize code changes.

### 7.3 Synchronization Gates

The synchronized state is a tuple, not one SHA:

```text
repository + branch + base SHA + local HEAD + remote branch head
+ working-tree diff hash + Memtrace indexed commit + Memtrace overlay episode
```

Clean states require matching local, remote, and indexed heads and an empty diff/overlay. Active-edit states require matching base and committed heads plus a working-tree diff whose changed files and symbols agree with the current Memtrace overlay. A commit advances local HEAD; a push advances remote head; indexing advances the indexed commit or overlay. Each transition must converge before dependent work continues.

Before work:

1. The local branch base equals the intended GitHub base.
2. The branch is registered in GitHub.
3. Memtrace indexing is complete for the repository and branch.
4. The Memtrace indexed commit equals local HEAD and the registered remote branch head.
5. Memtrace watching is active for the working directory.

During work:

1. Working-tree episodes correspond to intentional saves.
2. Scope expansion triggers a new impact check and evidence update.
3. Indexing failure or drift triggers the stop-work rule.

Before PR review:

1. The branch is pushed.
2. GitHub PR head, local HEAD, and Memtrace indexed branch head agree.
3. The working tree has no unrepresented changes.
4. The PR diff and Memtrace-detected symbol set agree.

Before merge:

1. Tests and review evidence apply to the current PR head.
2. Documentation, capability rows, ADRs, and evidence manifest agree with the diff.
3. No required review is stale or unresolved.

After merge:

1. The default branch is reindexed.
2. Its graph is verified against the GitHub merge SHA.
3. The phase evidence records the merged PR and Memtrace episodes.

## 8. Branch, PR, TDD, And Review Policy

### 8.1 Branch And PR Units

- Every leaf roadmap task uses a new branch pushed to GitHub.
- Branch naming follows `<type>/<phase>-<capability>-<short-purpose>`.
- A draft PR opens after the first meaningful commit.
- Every leaf task has one focused PR.
- Every roadmap phase ends with a phase-audit PR that links all task PRs, capability rows, ADRs, tests, known debt, and exit-gate evidence.
- Direct development on the protected default branch is prohibited.
- PRs stay small enough to review one capability or infrastructure concern at a time.

Cross-repository changes use a shared change ID and paired leaf tasks, branches, and PRs. Each PR declares its peer, merge dependency, compatibility state before and after each merge, rollback order, and owning phase-audit PR. An MVP CandelaMoon PR cannot merge while depending on unmerged mirror behavior; documentation-only paired PRs may merge independently when their tracked evidence remains truthful.

### 8.2 Mandatory Memtrace Workflow

Before touching existing code:

1. Verify Git, GitHub, and Memtrace synchronization.
2. Recall relevant decisions and governing rules.
3. Locate exact target symbols.
4. Run preflight, relationship, impact, timeline, and co-change analysis.
5. Record planned symbols and the generated verification checklist in the task and PR.

During work:

1. Keep live indexing active.
2. Re-run impact if scope changes.
3. Record new decisions and changed assumptions.

After work:

1. Review evolution since task start.
2. Detect changed symbols from the actual diff.
3. Re-run impact against the final graph.
4. Review the editing session for risk.
5. Attach Memtrace evidence to the PR.

### 8.3 Refactoring And Deletion Gate

No refactor or deletion proceeds without:

- Decision-memory and governing-rule checks.
- Dead-code, typed-relationship, or exact reachability evidence as applicable.
- Upstream and downstream impact.
- Bridge and centrality analysis when structurally relevant.
- Co-change and timeline review.
- Passing characterization tests for affected behavior and contract tests when a host/client contract is involved.
- A rollback strategy, normally a clean revert for an isolated change, with a more detailed recovery procedure for data, protocol, build, or release changes.
- Updates to capability rows, architecture docs, and disposition records when their tracked facts change; the PR must explicitly state when no such artifact is affected.

### 8.4 TDD

Feature and bug behavior follows red, green, refactor:

- Red: a focused test fails for the intended reason before implementation.
- Green: the minimum implementation makes the test pass.
- Refactor: structure improves while all tests remain green.
- The PR links evidence of the red state and final green state.
- Behavior-preserving refactors start with passing characterization tests.
- Deletions start with reachability and contract tests.
- Documentation and infrastructure-policy changes do not require synthetic failing tests, but executable infrastructure behavior is tested when practical.

### 8.5 Required PR Review Stack

Every PR passes:

1. Automated build, tests, lint, dependency, and security checks.
2. Memtrace GitHub PR review against the synchronized graph.
3. Acceptance audit against task requirements and capability rows.
4. Edge-case hunt covering boundaries, failure states, concurrency, lifecycle, and platform tiers.
5. Blind hunt by an independent fresh reviewer that receives the specification, diff, and tests but not the author's rationale.
6. Security review covering trust boundaries, secrets, parsing, network and IPC input, persistence, dependencies, and realistic exploitability.
7. Final policy check for documentation, ADRs, evidence, rollback, and known debt.

For a solo developer, independent agent or automated review checks provide separation. Findings are fixed or explicitly dispositioned before merge; the author does not silently self-approve.

Critical and high-severity findings cannot be waived by the author. A waiver requires a separate tracked decision, independent approval, rationale, compensating controls, owner, and expiry; security-critical findings also require the security review gate to approve the treatment. Expired waivers block merge and release. Reviewer independence means a fresh context and no participation in authoring the change; automated checks must identify their tool, version, ruleset, and analyzed commit.

## 9. Podman-First DevOps And DevSecOps Design

### 9.1 Delivery-System Design Phase

The first phase designs the development infrastructure without changing product code. It defines:

- Repository, branch, PR, and phase traceability.
- GitHub rulesets, required checks, ownership, merge, and rollback policy.
- CI architecture for Android, LuminalShine mirror validation, documentation, contract fixtures, and security.
- GitHub/Memtrace synchronization protocol and evidence-manifest schema.
- TDD and independent review execution.
- Supported development environments and pinned toolchains.
- Device-lab architecture for Google TV Streamer, API 28-30 compatibility, official LuminalShine, controllers, network faults, and artifact capture.
- Threat models for source, CI, secrets, signing, dependencies, release artifacts, Memtrace data, containers, and self-hosted runners.
- Supply-chain policy for actions, base images, dependencies, SBOMs, provenance, checksums, signatures, licenses, and vulnerability response.
- Secrets, signing, incident, retention, cache, cost, and maintenance policies.
- Infrastructure ADRs and an implementation backlog.

The design itself receives acceptance, edge-case, blind, and security reviews.

### 9.2 Podman Execution Boundary

Podman is the default execution boundary for reproducible builds, tests, documentation tools, contract fixtures, and security scans.

Planned image roles:

- `candelamoon-android`: JDK, Android SDK, NDK, Gradle/AGP prerequisites, native build tools, and unit/Robolectric tooling.
- `candelamoon-docs`: architecture schemas, Markdown, links, diagrams, ADRs, capability matrices, and evidence validation.
- `candelamoon-security`: static analysis, dependency and license review, secret scanning, SBOM, and artifact verification.
- `luminal-contract`: protocol fixtures, host-response simulation, parsers, and integration support.

Container policy:

- Rootless Podman by default.
- Versioned `Containerfile`s live with infrastructure code.
- Base images and CI actions are pinned by digest or immutable revision.
- Containers run non-root with minimal capabilities.
- Source mounts are read-only where possible; writable cache and output paths are explicit.
- Network access is denied or restricted when the task does not require it.
- Secrets are injected at runtime through approved stores and never baked into layers, environment dumps, artifacts, or caches.
- Images receive SBOMs, vulnerability scans, signatures, and provenance before promotion.
- Local and CI runs use the same image digest.
- Cache keys include image digest, lockfiles, toolchain versions, and target architecture.
- Commands are documented for Podman. Docker compatibility is not required.

### 9.3 Audited Host-Bound Exceptions

Containers must not create false confidence about hardware or Windows behavior.

Host-bound validation includes:

- Google TV Streamer and controller testing through real ADB/device access.
- Hardware decoder, HDR, frame-rate, audio, rumble, HDMI, and thermal testing on physical devices.
- Android emulator acceleration on a dedicated runner when nested virtualization is unreliable.
- Official LuminalShine Windows service, driver, display, capture, GPU, signing, and end-to-end streaming tests on Windows.
- Release signing in a restricted environment rather than a general build container when required.

A thin audited host orchestrator may launch approved Podman jobs, perform only the required OS or hardware action natively, and return artifacts to the common evidence pipeline.

### 9.4 Delivery Foundation Implementation

The second phase implements the approved delivery design before product mapping or product code changes:

- Protect default branches and prohibit direct pushes.
- Add PR, task, phase, and evidence templates.
- Add machine-readable architecture, capability, ADR, and evidence schemas.
- Add documentation and traceability checks.
- Add Android build, unit, lint, and emulator jobs.
- Add mirror and host-contract validation.
- Add static analysis, CodeQL, dependency review, secret scanning, license checks, SBOM, signatures, and provenance.
- Pin JDK, Gradle, AGP, Android SDK, NDK, CMake, Ninja, clang, Node, Podman, runner, and action versions.
- Establish signing and reproducible artifact procedures.
- Integrate Memtrace synchronization and PR review.
- Run a harmless end-to-end canary PR through all required checks.

The canary proves both the containerized pipeline and the explicit device/Windows handoff. Product code work does not begin until it passes.

### 9.5 Pipeline Tiers

- Per commit: formatting, lint, fast unit tests, docs/schema, secret, and dependency checks.
- Per PR: full tests, API-tier matrix, Memtrace review, acceptance, edge, blind, and security reviews, SBOM delta, and evidence audit.
- Nightly: emulator/device compatibility, dependency freshness, contract fixtures, and extended stream/reconnect tests.
- Release candidate: real Google TV Streamer and compatibility hardware, official host integration, long-session/fault testing, signed artifacts, provenance, SBOM, checksums, and rollback rehearsal.

## 10. Verification Strategy

### 10.1 Documentation And Contract

- Validate links, source references, upstream pins, ADR status, capability completeness, and feature IDs.
- Store versioned official LuminalShine fixtures for discovery, pairing, app list, launch, resume, quit, negotiation, and errors.
- Reject orphan architecture components, capability rows, tasks, PRs, or Memtrace evidence.

### 10.2 Client Tests

- Unit-test capability classification, API-tier policy, fallback selection, parsers, persistence, and UI state models.
- Test D-pad traversal, initial and restored focus, Back behavior, dialogs, long labels, accessibility semantics, lifecycle recreation, and adaptive effects.
- Test classic transport startup, decoder selection, audio, controller input, rumble, reconnect, and shutdown.
- Run contract integration against official LuminalShine and deterministic fixtures.
- Keep mirror-only behavior in a separate non-MVP lane.

### 10.3 Device And Fault Matrix

- Google TV Streamer is the API 31+ primary reference device.
- API 28-30 uses emulation plus at least one representative hardware device before public release.
- The primary tier is bounded by a tracked support matrix rather than the phrase `API 31+`: it includes API 31, the current Google TV Streamer OS, and the newest Android TV API supported by the current toolchain, with representative Google/AOSP and at least one non-Google OEM codec path when public release scope includes it.
- Every supported device row records OS/API, SoC, decoder and codec capabilities, HDR, frame-rate behavior, controller and rumble support, network path, test date, and result. A device or newer API is not release-supported until its row passes the required suite.
- Faults include host offline/reboot, network loss, certificate mismatch, invalid PIN, pairing conflict, busy session, unsupported codec/HDR, decoder failure, no artwork, malformed response, and low-memory recreation.

### 10.4 Performance And Deletion Evidence

- Measure startup, host-grid response, focus latency, stream handoff, dropped frames, decoder latency, memory, and thermal behavior.
- Set numeric budgets from measured baselines in the MVP specification before implementation.
- Verify each deletion with Memtrace impact, characterization and contract tests, build/test results, resource reachability, and documentation updates.
- Keep one deletion category per reviewable change.

### 10.5 Release Evidence

Each phase closes with capability rows, PR links, Memtrace episodes, tests, visual evidence where relevant, performance deltas, known debt, and ADR compliance.

MVP release requires:

- No unresolved critical compatibility mismatch.
- No unclassified inherited feature.
- Official LuminalShine passes all MVP journeys.
- API 28-30 core and API 31+ full-tier contracts pass.
- The default GitHub branch and Memtrace graph are synchronized.

## 11. Phased Roadmap

Phases are evidence-gated. Every leaf task has a branch and PR, and every phase ends with a phase-audit PR.

### Phase 0: Delivery-System Design

Design the Podman-first DevOps/DevSecOps system, GitHub/Memtrace synchronization, branch/PR workflow, review stack, device lab, supply chain, signing, secrets, incidents, and maintenance.

Exit gate: the delivery design passes acceptance, edge-case, blind, and security reviews.

### Phase 1: Delivery Foundation

Implement repository protections, Podman images, CI, evidence schemas, security controls, signing, Memtrace integration, and the complete canary PR.

Exit gate: the canary proves all automated, independent-review, container, device, Windows, evidence, and synchronization paths.

### Phase 2: Repositories And Baselines

- Select and pin the initial supported official LuminalShine release tag and commit; the current `main` snapshot is evidence input only until that selection.
- Establish mirror tracking and branch rules.
- Establish documentation paths, vocabulary, IDs, and ADR template.
- Configure Memtrace exclusions for vendored and generated code.
- Inventory local `new-design/` visual decisions and contradictions into a tracked disposition ledger without making the local directory a reproducibility dependency.

Exit gate: both repositories have reproducible, synchronized baselines and no architecture claim depends on a moving branch.

### Phase 3: Two Architecture Spines

Map both repositories by shared capability area while producing complete repo-specific spines.

CandelaMoon coverage includes activities, services, discovery, pairing, app grid, profiles, preferences, streaming/JNI, decoder/audio, input, persistence, TV integration, build variants, tests, and debt.

LuminalShine coverage includes classic client-facing control, trust, catalog, process/session lifecycle, negotiation, stream/input paths, virtual display effects, client-visible settings/errors, and version behavior.

Exit gate: every spine component has source, graph, and test evidence; all core journeys trace end to end.

### Phase 4: Contract, Dispositions, And MVP Spec

- Complete the capability contract with no silent omission.
- Classify every inherited feature.
- Define official-host support and capability detection.
- Write MVP requirements, non-functional requirements, device tiers, performance budgets, and acceptance tests.
- Normalize the visual system into tracked `DESIGN.md`.
- Approve the initial ADRs and phased deletion ledger.

Exit gate: unknown rows are resolved or explicitly deferred, and MVP contains no mirror-only dependency.

### Phase 5: Platform Foundation And UI Evaluation

- Establish CandelaMoon identity and branding without migration code.
- Add a platform and capability service for API tier, device, codec, and official host capabilities.
- Prototype Compose for TV with host grid, D-pad restoration, pairing, app library, accessibility, recreation, and native stream handoff.
- Benchmark API 28-30 compatibility and API 31+ primary tiers.
- Decide Compose or modern Views by ADR.
- Build one adaptive component layer.

Exit gate: deterministic navigation, no focus traps, acceptable performance, correct accessibility, lifecycle recovery, and clean native-stream interop.

### Phase 6: Core Host Journey

Replace discovery, manual add, pairing, host status, and host actions while preserving verified underlying services where appropriate.

Exit gate: a fresh install can pair with an official host entirely through D-pad on both platform tiers.

### Phase 7: Library And Session Journey

Replace app catalog, artwork, loading, launch, resume, quit, busy-session, unavailable-app, and disconnect behavior. Preserve host ownership of catalog and session state and hand off to the classic native stream.

Exit gate: paired host to active stream and back completes without inherited UI.

### Phase 8: Stream Configuration And In-Stream TV UX

Rebuild settings and profiles around verified negotiation. Capability-gate codec, HDR, resolution, frame rate, audio, and display options. Replace the in-stream menu, HUD, warnings, keyboard invocation, and recovery while protecting native boundaries.

Exit gate: configuration is truthful for the connected official host and device, and recovery is deterministic.

### Phase 9: Controllers And Retained Client Features

Validate controller mapping, rumble, TV-relevant keyboard/mouse behavior, shortcuts, diagnostics, and every retained client-only capability. Use API 31+ enhancements without regressing API 28-30 core control.

Exit gate: every MVP `retain-client` and `adapt-to-luminal` row has acceptance evidence.

### Phase 10: Controlled Deletion And Simplification

Remove approved mobile UI and behavior, Apollo-specific integration, Artemis branding, root build flavor, pre-O input capture paths, obsolete API branches, dormant flags, and orphan resources in isolated changes.

Exit gate: no unsupported UI route, feature flag, host control, or orphan resource remains, and every deletion satisfies the Memtrace gate.

### Phase 11: Hardening And Release

Complete device, codec, controller, long-session, reconnect, lifecycle, network, update, performance, memory, thermal, accessibility, localization, security, dependency, license, signing, and rollback validation.

Exit gate: all official-host MVP journeys and both Android platform-tier contracts pass with synchronized GitHub and Memtrace state.

### Phase 12: Maintenance And Post-MVP Innovation

- Refresh compatibility for official LuminalShine releases.
- Maintain Android target compliance, dependencies, security, codecs, devices, Podman images, and runners.
- Evaluate client-only ideas through lightweight ADRs and capability rows.
- Prototype host-dependent ideas in the mirror without making them official-product dependencies.
- Keep WebRTC excluded from CandelaMoon; changing that boundary requires a separately brainstormed product design and superseding ADR.

## 12. Bootstrap Exception

The delivery controls cannot enforce themselves before Phase 1 exists. Phase 0 design and initial Phase 1 pipeline PRs therefore use documented manual equivalents for missing automated gates. This bootstrap exception does not override the synchronization stop-work rule; if Memtrace itself requires repair, the narrowly defined repair mode in Section 7.2 applies.

The exception is narrow:

- Branches and PRs are still required.
- Memtrace synchronization and review are required; repair mode is used when the control is unavailable or inconsistent.
- Acceptance, edge-case, blind, and security reviews are performed manually or by independent agents.
- Missing automation is recorded and implemented in Phase 1.
- No product code begins under the bootstrap exception.

## 13. Success Criteria

The architecture and mapping milestone is complete when:

- Both architecture spines are complete and evidence-backed.
- The official-host integration profile is pinned and reproducible.
- Every inherited feature has a disposition.
- The capability contract has no silent omissions.
- MVP scope, API tiers, fallbacks, errors, and acceptance tests are explicit.
- ADRs capture all consequential product, architecture, repository, process, and infrastructure decisions.
- The phased roadmap is decomposable into focused branch-and-PR tasks.
- GitHub and Memtrace synchronization controls are operational.
- The Podman-first delivery foundation has passed its canary.

Only then does product feature implementation begin.

## 15. Agent Architecture And Task Workflow

### 15.1 Agent Roster

The program uses a multi-agent architecture with split responsibilities. Production agents receive the handoff file and update it. Review agents receive only need-to-know information and never update the handoff.

**Production Agents:**

- **Senior Developer**: Implements code per task spec and TDD suite. Java/Android, Kotlin/Compose for TV, NDK/JNI, streaming protocol. Activates tests one at a time (red to green), refactors while green, updates handoff with implementation evidence.
- **QA Architect**: Creates TDD red-phase test scaffolds before implementation. Runs coverage audits with Memtrace reconciliation after implementation. Gates tasks between development and UAT.
- **DevOps Architect**: Podman-first container design, GitHub Actions CI, self-hosted runners, device lab, signing, release engineering.
- **Security Analyst**: Threat modeling, supply chain policy, secrets management, signing policy, incident response, DevSecOps design.
- **GRC Architect**: ADR governance, compliance checks, waiver management, policy enforcement, audit trails. Ensures no undocumented decision affects the product boundary.
- **Tech Writer**: Documents every artifact, creates session handouts to prevent context rot, maintains handoff file with finalized information.
- **UX/UI Designer**: Visual design system, TV UX patterns, accessibility, D-pad flows, Compose for TV evaluation.

**Review Agents (no handoff access, need-to-know only, never update handoff):**

- **Blind Hunter**: Cynical adversarial reviewer with zero context. Finds what is missing. Receives only: spec, diff, tests. No author rationale.
- **Edge Case Hunter**: Exhaustive path enumeration, boundary conditions, deletion check. Method-driven, not attitude-driven. Receives only: diff.
- **Acceptance Analyst**: Reviews diff against spec and acceptance criteria. Finds deviations from spec intent. Receives only: spec and diff.
- **Red Team Analyst**: Offensive security reviewer. Finds exploitable weaknesses with concrete attack scenarios using STRIDE and OWASP. Receives: diff and spec for context.
- **Blue Team Analyst**: Defensive security reviewer. Receives red team findings and designs concrete, implementable mitigations. Assesses exploitability, confirms or rejects findings, checks for new risks introduced by mitigations.

The orchestrator (the main session agent) acts as Product Owner: creates task breakdowns with acceptance criteria, maintains the handoff file, dispatches agents, triages review findings, gates transitions, opens PRs using Memtrace code-review, and manages the phase-audit cycle.

### 15.2 Task Workflow

Every leaf task flows through this pipeline:

1. **Orchestrator creates task handoff**: Detailed to-do with acceptance criteria, need-to-know context scoped per agent, evidence manifest initialized.
2. **QA Architect creates TDD red-phase suite**: Test scaffolds (failing or skipped), ATDD checklist with implementation guide, test artifacts in handoff.
3. **Senior Developer implements solution**: Activates tests one at a time (green), refactors while green, updates handoff with implementation evidence.
4. **Review Phase 1 (parallel, no handoff access)**: Blind Hunter, Edge Case Hunter, and Acceptance Analyst receive only need-to-know info. They run in parallel without prior conversation context.
5. **Orchestrator triages Phase 1 findings**: Normalize, deduplicate, assign severity, route (decision-needed, patch, defer, dismiss). Add decision-needed and patch findings to handoff. Decision-needed findings require user input.
6. **Senior Developer implements Phase 1 fixes**: Updates handoff with fix evidence.
7. **Review Phase 2 (security, sequential)**: Red Team Analyst runs first (offensive). Blue Team Analyst runs second (defensive, acts on red team findings).
8. **Orchestrator triages Phase 2 findings**: Add to handoff. Patch findings go to developer.
9. **Senior Developer implements security fixes**: Updates handoff with fix evidence.
10. **QA Architect runs coverage audit**: Risk-weighted score per AC, Memtrace reconciliation (detect_changes, get_evolution), coverage rating (pass/conditional/fail). If fail, back to step 3 with coverage tasks.
11. **UAT (user)**: When applicable, user tests the implementation.
12. **Tech Writer documents everything**: Architecture docs, ADRs, capability rows, session handout. Updates handoff with all finalized artifacts.
13. **Orchestrator opens PR using Memtrace code-review**: review_github_pr against the synchronized graph.
14. **Tech Writer creates session handout**: All paths, artifacts, and state for the next phase/task to be started in a new session (prevents context rot).

Every step must produce the documentation expected from that agent so the tech writer has every artifact to create the final documentation.

### 15.3 Handoff File Structure

Every task has a handoff file (YAML frontmatter + markdown body) containing:

- Task metadata: task_id, phase, title, status, branch, base_sha, current_sha, pr_url
- Acceptance criteria: list of testable criteria
- TDD artifacts: ATDD checklist path, test files, red-phase verification
- Implementation artifacts: files created/modified, green-phase verification
- Review Phase 1: blind/edge/acceptance findings, triaged findings, fixes applied
- Review Phase 2: red/blue team findings, triaged findings, fixes applied
- Coverage audit: rating, risk-weighted score, Memtrace reconciliation, coverage gaps
- UAT: status, user decision
- Documentation: tech writer artifacts, session handout path
- Memtrace evidence: repo_id, indexed_sha, episode_ids, detect_changes summary
- Known debt and rollback strategy

The handoff file is the single source of truth for task state. Every agent that participates updates it. Review agents do not see or update it.

### 15.4 Session Handout

At the end of every task or phase, the Tech Writer creates a session handout document that contains everything needed to continue work in a new session without conversation history:

- Current state: branch, commit SHA, PR URL, Memtrace indexed SHA
- Artifacts produced: file paths and descriptions
- Pending work: next task description and dependencies
- Keys for next session: handoff file path, spec path, ADR register path, evidence manifest path, test artifact paths
- Known debt: deferred or incomplete items
- Rollback strategy: how to undo this work if needed

---

> **Post-restructure note (2026-08-07)**: Section 15.1's agent roster and the per-task 14-step cycle are operationalized in the tracked .maestro-space/ framework. See:
> - .maestro-space/index.md (framework entry point)
> - .maestro-space/maestro-docs/maestro-orchestrator-guide.md (dispatch matrix, handoff protocol, review pipeline)
> - .maestro-space/maestro-docs/maestro-workflow.md (14-step cycle + post-phase + maintenance)
> - .maestro-space/maestro-docs/maestro-conventions.md (JSON+MD output, naming, agent contracts)
> - .maestro-space/maestro-agents/agent-manifest.json (the agent registry)
