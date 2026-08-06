# Threat Model

This document is the security threat model for the CandelaMoon delivery pipeline: from developer machines, through CI, the device lab, release signing, and public distribution. Each section lists trust boundaries, then threat/control pairs per subsystem. The model follows the principle: trust nothing you did not build, control everything you ship.

## Trust Boundaries

Trust boundaries are the edges across which data or execution passes between entities with different trust levels. Every boundary below defines what is trusted on each side and the controls that police it.

| Boundary | Trusted side | Untrusted side | Controls |
|----------|--------------|----------------|----------|
| Local dev machine | The developer's machine and its tools (IDE, git, adb) | Anything fetched at build time (registries, dependencies) | Pinned versions/digests, dependency review, builds happen in CI rather than on dev machines |
| Podman container | The container image as built from our Dockerfile plus pinned base | The network, package registries, any runtime-injected data | Rootless Podman, non-root execution, read-only mounts, restricted egress, digest-pinned base images |
| CI runner | GitHub Actions execution environment and job isolation | Third-party actions, checked-out repository content (fork PRs), the network | Actions pinned by SHA, no secrets on fork PRs, ephemeral runners, no token persistence |
| GitHub Actions | GitHub's platform isolation and OIDC token issuance | Job steps (a compromised action can run as the workflow identity) | Least-privilege permissions per job, no blanket token scopes, SHA pinning, dependency review |
| Device lab | The runner plus device LAN, the reference device as our controlled endpoint | The test host's network behavior, any malformed media the test host emits | Isolated VLAN, per-job pairing, fault-injection harness as the only outside input, no secrets on devices |
| Windows runner | The pinned LuminalShine install and the Windows host config | The device-lab network (by design it is reachable from the device) | Firewall allow-list of the device subnet, pinned LuminalShine version, runner used for one suite only |
| Memtrace daemon | The local daemon and its local graph store | CI/log exports that could leak indexed data, other machines on the dev LAN | `.memtrace/` gitignored, no Memtrace output in CI logs, privacy review of exported evidence |
| Release signing environment | The offline/restricted signing box and its key material | Everything else — the signing key never leaves this boundary | Air-gapped or restricted network, key on hardware (HSM/smartcard), no general-CI access |
| Public release artifacts | Artifacts as produced by the build pipeline with provenance | Any party that can replace or modify artifacts after signing (registry, mirrors, users' caches) | Signatures, provenance attestations, published checksums, reproducible builds |

## CI

The CI pipeline is the highest-value attack surface: it combines third-party code (actions, dependencies), untrusted input (fork PRs), and secrets.

- **Threat: malicious PR with poisoned cache.** A fork PR can manipulate build caches (Gradle, dependency caches, action caches) to inject behavior into subsequent builds. **Controls:** caches are keyed by immutable inputs and validated before use; cache restore happens only for trusted branches, never for fork PRs into mainline builds.
- **Threat: compromised GitHub Action.** A third-party action, once compromised (repo takeover or tag move), executes with the workflow's identity. **Controls:** all actions pinned by full commit SHA (see supply-chain-policy.md); action updates are dedicated PRs with review; `permissions:` blocks are minimized per job; `GITHUB_TOKEN` is read-only or absent where not needed.
- **Threat: insufficient runner isolation.** A shared runner could leak state across jobs. **Controls:** self-hosted runners are single-purpose per label and recycled; every job gets a clean workspace; no persistent secrets on runners; container jobs isolate via rootless Podman.
- **Threat: secret exfiltration via build artifacts or logs.** A poisoned step can print or embed secrets in logs or artifacts. **Controls:** secrets are injected as runtime environment (never baked into images or build files); secret masking on logs; a guard step scans artifacts for secret patterns; logs are retained short-term and scrubbed.
- **Threat: fork-branch workflow bypasses.** A fork PR could invoke workflows with excessive permissions or trigger release paths. **Controls:** fork PRs run only `pull_request` with no secrets, no environment access, and no cache-restore privileges; release/signing workflows run only from the protected default branch or tagged releases by maintainers.

## Secrets

- **Threat: secret baked into a container image.** A secret written into the image layer at build time is recoverable by anyone with image access. **Controls:** no secrets in `Dockerfile` ARG/ENV/COPY layers; build secrets are mounted at build time via Podman `--secret` and never land in the image; image layers are scanned for secret patterns in CI.
- **Threat: secret in an environment dump or CI log.** `env` dumps, debug outputs, or echo steps can leak injected secrets. **Controls:** GitHub's built-in secret masking on all secrets; steps that dump the environment are banned; the guard step fails the job if a known secret name or value appears in logs.
- **Threat: secret in Memtrace data.** Indexed code or exported evidence can contain credentials (connection strings, tokens in source). **Controls:** `.memtrace/` is gitignored; Memtrace output never enters CI artifacts or logs; a privacy review is required before any evidence export leaves the lab (see Memtrace Data).
- **Threat: secret in a release artifact.** A keystore, signing key, or API token shipped inside the APK/AAB. **Controls:** the release pipeline runs a secret scan over the assembled artifact before signing; keystores live only in the signing environment.
- **Cross-cutting controls:** secrets are stored only in GitHub Secrets and GitHub Environments; injection happens at runtime into the job environment; OIDC tokens (short-lived, workload identity) are preferred over long-lived credentials wherever the provider supports it; long-lived credentials have rotation dates and are absent from all runners and images; fork PRs never receive secrets of any kind.

## Signing

- **Threat: signing key compromise.** If the release key leaks, an attacker can sign arbitrary APKs as CandelaMoon. **Controls:** the signing key lives only in the restricted signing environment (see Trust Boundaries); the key is stored on hardware (HSM or smartcard) with PIN; the key never appears in the repository, CI, containers, or caches; suspected compromise triggers immediate key rotation and a security advisory.
- **Threat: unsigned release.** An unsigned artifact is indistinguishable from tampered third-party builds. **Controls:** the release gate fails if the artifact's signature does not verify; checksums are published and signed; provenance attestation references the signed artifact digest.
- **Threat: signing in an untrusted environment.** If signing runs in general CI, the signing step shares the runner with everything else in the job. **Controls:** signing happens only in the restricted environment on a dedicated job with no third-party steps; the signing job runs from the protected branch with no fork path; the key's exposure window is limited to the signing operation itself.

## Dependencies

- **Threat: compromised upstream dependency.** A malicious or hijacked library version enters the dependency graph. **Controls:** all Gradle, NDK, and Python dependencies are pinned to exact versions (no SNAPSHOT or ranges); automated dependency review opens a review PR for any change; OSV/dependabot alerts are monitored with SLA (see supply-chain-policy.md); the per-build SBOM enables tracing a CVE to affected releases.
- **Threat: malicious base image.** A base image is the trust root of every container. **Controls:** base images pinned by digest; images pulled through the registry proxy; image signatures verified where the registry supports it; emergency replacement procedure for compromised base images (incident-and-rollback-policy.md).
- **Threat: transitive vulnerability.** A vulnerability in a transitive dependency is the hardest to notice. **Controls:** the SBOM includes transitive components; every CI run runs vulnerability scanning over the full dependency tree; critical findings block the release; advisories are monitored and triaged within SLA.

## Release Artifacts

- **Threat: tampered APK.** Someone replaces the distributed APK with a malicious one. **Controls:** artifacts are signed with the release key; signatures are verified on download; published checksums let users verify independently.
- **Threat: missing provenance.** Without provenance it is impossible to say what produced an artifact. **Controls:** SLSA Level 3 target provenance attestations are generated per release, stored alongside the artifacts, and reference the source commit, builder image digest, build environment, and dependency set.
- **Threat: unsigned checksums.** Unsigned checksum files are as trustworthy as the page hosting them. **Controls:** checksum files are signed with the release key and published with the artifacts; release notes link both.

## Containers

- **Threat: container escape.** A compromised process inside the container breaks into the host. **Controls:** rootless Podman (no root daemon), non-root execution inside the container, minimal capabilities (`--cap-drop=ALL` plus a whitelist), no `--privileged`, default seccomp/apparmor profiles.
- **Threat: poisoned container image.** An image built from tampered layers runs attacker code. **Controls:** base images pinned by digest, images scanned (Trivy) in CI, signature verification, and an SBOM for every image.
- **Threat: supply-chain attack on the base image registry.** The registry itself (or its credentials) is compromised. **Controls:** images are pulled via the registry proxy with digest pinning; registry credentials are short-lived and restricted; image digests are recorded in provenance so a swapped tag never matches a release.

## Memtrace Data

- **Threat: sensitive data in the graph.** The Memtrace knowledge graph indexes file paths, symbol names, IP addresses, and other strings from the codebase; exported evidence bundles can carry the same content plus screenshots and logs. **Controls:** the `.memtrace/` store is gitignored and never committed; Memtrace output (queries, exports, graphs) is never placed in CI logs or artifacts; any evidence exported from the device lab or dev machines for external review requires a privacy review pass that scrubs device identifiers, LAN IPs, and user data; the Memtrace daemon runs on the local machine only, with credentials stored locally and never in CI.
