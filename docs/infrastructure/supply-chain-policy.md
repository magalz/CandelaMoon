# Supply Chain Policy

This policy governs every third-party component that enters a CandelaMoon build: GitHub Actions, container base images, language/runtime dependencies, and the SBOM/provenance/vulnerability reporting that makes the chain auditable. The policy applies to the `main` branch and all release builds; any deviation requires an explicit, reviewed exception.

## Actions

- All GitHub Actions used in workflows are pinned by full commit SHA (`uses: <owner>/<repo>@<40-hex-sha>`), not by tag. Tags are mutable and a moved tag is a supply-chain attack vector.
- `uses: action@*` (floating major version) and `uses: action@main` are prohibited. A workflow that uses a floating reference fails review and, where possible, fails CI.
- Action updates are made only in dedicated PRs titled `chore(actions): <action> <old-sha> -> <new-sha>` and require review by a maintainer. The PR must link the upstream release notes for the new SHA.
- The set of pinned action SHAs is tracked in `workflows/pins.yml` (machine-readable) so changes are diffable in review.

## Base Images

- All container base images (including intermediate images such as the Gradle/JDK and NDK images) are referenced by digest: `FROM ...@sha256:<digest>`. Tag references in `Dockerfile`s are not permitted.
- Digests are refreshed quarterly in a dedicated PR that bumps all base image digests together and reruns the full build and scan matrix. The refresh is scheduled via a quarterly reminder issue.
- If a base image is compromised (CVE, injected content, or registry incident), the emergency replacement procedure applies: halt all builds using the image, replace with the nearest unaffected digest, rebuild, rescan, and re-sign affected releases (see incident-and-rollback-policy.md).

## Dependencies

- All Gradle, NDK, and Python dependencies are pinned to exact versions. No SNAPSHOT versions, version ranges (`1.2.+`), or dynamic resolution in any branch that feeds a build.
- Dependency updates happen via dedicated PRs (automated review or dependabot-style) that are scanned and reviewed before merge; emergency patches can skip the queue but not the review.
- Every new dependency (direct or newly introduced transitive) requires a license compatibility review before merge: the license must be compatible with distribution, and the dependency's project health (maintenance, provenance, known incident history) must be checked.
- Lockfiles (Gradle version catalogs, pip requirements, NDK toolchain manifests) are the source of truth; locked resolution is enforced in CI so the lockfile cannot drift silently.

## SBOM

- A software bill of materials is generated for every build: CycloneDX for container images and Gradle projects, SPDX for release artifacts where CycloneDX is not produced.
- The SBOM is stored as a build artifact alongside the build output and archived with the release.
- Between releases, the SBOM diff is reviewed: added, removed, and changed components are listed in the release notes, and any unexpected addition (a dependency not in a reviewed update PR) blocks the release.

## Provenance

- Build provenance attestations target SLSA Level 3: the attestation records the source commit, the builder image digest, the build environment (runner type, image digests), and the dependency set.
- Attestations are generated as build artifacts, stored alongside release artifacts, and published with the release.
- The attestation is verified before a release is marked published: the source commit must be an ancestor of `main` at release time and the builder image digest must match the recorded value.

## Vulnerability

- Every CI run executes automated vulnerability scanning (Trivy for containers, OSV/Gradle dependency scan for dependencies) over the full build.
- Severity policy: critical findings block the release and require immediate action; high findings block the release unless explicitly waived by a maintainer with a tracked ticket.
- SLAs from finding to remediation: critical 24 hours, high 72 hours, medium 1 week; low findings are tracked in the backlog.
- Dependency advisories (GitHub advisory database, OSV, vendor feeds) are monitored continuously; a new advisory for a component in the SBOM opens a triage item automatically.
