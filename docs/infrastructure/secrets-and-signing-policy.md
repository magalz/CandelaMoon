# Secrets And Signing Policy

This policy defines where secrets may live, how signing keys are handled, and what the release procedure requires. It complements the threat model (threat-model.md) and the supply chain policy (supply-chain-policy.md); in case of conflict, the stricter policy wins.

## Secret Stores

- **GitHub Secrets** are the store for CI secrets (build-time tokens, test-host credentials). Secrets are referenced by name in workflows and injected at runtime; they never appear in source, configuration files, or workflow text.
- **GitHub Environments** are the store for deployment and release secrets (registry push credentials, release-publish tokens, signing-enrollment material). Release workflows run against the `release` environment with required reviewers and protection rules.
- **No secrets in code, container images, or CI logs.** A secret found in any of these is an incident: rotate immediately, remove it, and record the incident in the audit.
- **Short-lived OIDC tokens** are used wherever the provider supports workload identity (cloud providers, registries with OIDC). Static long-lived credentials exist only where OIDC is impossible, are scoped to the narrowest permission, and have rotation dates tracked in the secrets inventory.
- **Memtrace daemon credentials** are stored locally on the machine running the daemon — never in CI, never in the repository. CI never receives Memtrace credentials or exports Memtrace data (see threat-model.md).

## Signing

- Release signing keys are stored offline or in a restricted environment: the signing box is air-gapped or on a restricted network, and the key material lives on hardware (HSM or smartcard) with PIN protection.
- Signing is performed only in the restricted environment. General CI never has access to the signing key, the keystore, or the signing passphrase.
- The key's exposure window is minimized: the key is engaged only for the signing operation and disengaged immediately after; the signing box is powered off when not in use.
- Key rotation is a documented procedure: generate a new key in the restricted environment, sign the migration release with both keys, publish the new public key, retire the old key after the grace period. Rotation is scheduled yearly and on any suspected exposure.
- Keys are never in the repository, container images, CI caches, or logs. The key fingerprint, not the key material, is the only key data allowed in CI metadata.

## Release

- APK/AAB artifacts are signed with the release key (v2/v3 scheme); unsigned artifacts are never uploaded to the release channel.
- Checksums (SHA-256) are generated for every artifact, signed with the release key, and published alongside the artifacts.
- Provenance attestation (SLSA Level 3 target) is attached to every release, covering source commit, builder image digest, build environment, and dependency set (see supply-chain-policy.md).
- Artifacts are retained per the retention policy: releases are retained indefinitely, intermediate build artifacts 90 days, and fault-injection/evidence bundles 30 days unless attached to a release.
- Rollback: the rollback procedure is defined in incident-and-rollback-policy.md. In short, a bad release is halted within 1 hour, distribution is pulled, and a patched release is shipped through the same signed pipeline.
