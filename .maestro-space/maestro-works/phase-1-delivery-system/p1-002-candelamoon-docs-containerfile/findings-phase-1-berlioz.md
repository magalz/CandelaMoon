# Findings Report — Berlioz (Blind Hunter) (Phase 1)

- **Reviewer**: Berlioz (Blind Hunter) (`berlioz-blind-hunter`)
- **Task**: P1-002 — candelamoon-docs Containerfile
- **Branch**: `not provided`
- **Base SHA**: `86d3c216eb2539cec76556978cc7e36941dfaca8`
- **Head SHA**: `e37c8c189b2505b11e36093c629fe6430839031f`
- **Date**: 2026-08-09
- **Dispatched by**: not provided

---

## Scope

Reviewed `git diff 86d3c216eb2539cec76556978cc7e36941dfaca8..e37c8c189b2505b11e36093c629fe6430839031f`, focusing on the candelamoon-docs Containerfile, its requirements and validator script, and the toolchain pin updates. Compared the implementation with `ci-architecture.md` § “candelamoon-docs” (lines 69-76) and § “Common conventions” (lines 53-58). The handoff, plan, ADR context, author rationale, and conversation history were not used.

## Method

Cold, adversarial review of every declared image requirement and every runtime/build-time boundary. I specifically checked for missing tools, false-green validation, mount and user-contract violations, unpinned inputs, network-policy gaps, architecture assumptions, reproducibility claims, and absent negative-path evidence.

## Findings

### B-01 — `validate-design` is a tool-presence smoke test, not design validation

- **Severity**: critical
- **Location**: `infra/containers/candelamoon-docs/validate-design:9-13,83-123`
- **Detail**: The specification requires validation of architecture schemas, the ADR register, the capability matrix, and the evidence manifest. This script only probes command versions and explicitly does not read or parse `/workspace/docs`; invalid or missing design documents therefore still produce exit 0 and a false-green docs gate.
- **Evidence**: `docs/infrastructure/ci-architecture.md:72`; the script's own scope and checks at lines 9-13 and 83-123.
- **Suggested route**: patch

### B-02 — Required ADR/capability-matrix validation scripts are absent

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/Containerfile:194-206`
- **Detail**: The image contract separately names ADR/capability-matrix validation scripts, but the diff only copies `requirements.txt` and the version-probe `validate-design` script. No validator implementation is installed or invoked, so the required scripts cannot run in this image.
- **Evidence**: `docs/infrastructure/ci-architecture.md:72`; the only validator copy is at Containerfile line 205.
- **Suggested route**: patch

### B-03 — Node download escapes the declared build-time network policy

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/Containerfile:136-140`
- **Detail**: The spec documents PyPI and the npm registry as the candelamoon-docs build-time network. The build additionally fetches a binary from `nodejs.org`; a comment acknowledging the expansion does not make the Containerfile compliant or enforce an approved proxy/allowlist.
- **Evidence**: `docs/infrastructure/ci-architecture.md:74` versus the `curl https://nodejs.org/...` command at Containerfile line 140.
- **Suggested route**: decision-needed

### B-04 — APT mirror access is also outside the documented build network

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/Containerfile:117-123`
- **Detail**: `apt-get update` and `apt-get install` require live Debian repository endpoints, none of which are listed in the image's build-time network declaration. A build restricted to the documented PyPI/npm hosts will fail before installing Node or the validators.
- **Evidence**: `docs/infrastructure/ci-architecture.md:74`; the unqualified APT update/install at Containerfile lines 117-123.
- **Suggested route**: decision-needed

### B-05 — The digest-pinned base does not pin the APT package set

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/Containerfile:112-123`
- **Detail**: A digest freezes the base filesystem and its repository configuration, not the package versions returned by a later `apt-get update` against a moving Debian suite. `ca-certificates`, `curl`, `git`, and `xz-utils` can change between builds, undermining both supply-chain review and reproducibility; the comment claiming the base pins package revisions is not a control.
- **Evidence**: The code installs packages without versions at lines 117-123 and claims they cannot drift at lines 112-116.
- **Suggested route**: patch

### B-06 — Transitive Python dependencies float despite the “pinned” dependency claim

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/requirements.txt:11-14`
- **Detail**: Only the three direct requirements are exact-pinned; the file explicitly delegates all transitive resolution to current PyPI metadata, and the Containerfile installs without hashes or a constraints/lock file. A fresh build can therefore contain a different dependency tree from the recorded `pip freeze`, including a changed or compromised transitive package.
- **Evidence**: Dynamic-resolution statement at requirements lines 11-14 and un-hashed `pip install` at Containerfile lines 167-170.
- **Suggested route**: patch

### B-07 — npm pins only top-level packages and leaves their dependency trees mutable

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/Containerfile:188-192`
- **Detail**: `npm install -g package@version` fixes the two requested package versions but does not use a lockfile or frozen integrity-checked dependency tree. Transitive npm dependencies are resolved anew from the registry on each build, so the image is not reproducibly pinned by the versions shown in the ENV block.
- **Evidence**: Two global installs with no lock/constraint input at Containerfile lines 188-192; only top-level pins are recorded in `toolchain-pins.md:125-127`.
- **Suggested route**: patch

### B-08 — The Node payload assumes Linux x86-64 without declaring or handling the platform

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/Containerfile:91,140`
- **Detail**: The image always downloads `node-v...-linux-x64.tar.xz`, with no `TARGETARCH` handling and no explicit `linux/amd64` platform contract. On an arm64 build the subsequent npm RUN step can fail with an exec-format error; on an arm64 runtime a successfully copied x64 binary cannot execute.
- **Evidence**: Hard-coded `linux-x64` URL at Containerfile line 140; no architecture selection in the surrounding build steps.
- **Suggested route**: patch

### B-09 — The required report output mount contract is missing

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/Containerfile:253-289`
- **Detail**: Common conventions require writable `/workspace-out/reports` and `/workspace-out/artifacts` output mounts, with mount points created/chowned for `builder`. The image creates only cache directories and `/workspace`; it provides no `/workspace-out` hierarchy or ownership postcondition, so report generation can fail or fall back toward the read-only source mount.
- **Evidence**: `docs/infrastructure/ci-architecture.md:55-57`; the only runtime directories created are shown at Containerfile lines 253-289.
- **Suggested route**: patch

### B-10 — `USER builder` is not the final Containerfile directive

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/Containerfile:295-308`
- **Detail**: The common convention says `USER builder` is the final directive, but `WORKDIR` and `CMD` follow it. The implementation weakens the wording to “last USER directive,” which is not the stated contract and leaves a straightforward structural acceptance check failing.
- **Evidence**: `docs/infrastructure/ci-architecture.md:54`; `USER builder` at line 295 followed by `WORKDIR` and `CMD` at lines 301 and 308.
- **Suggested route**: patch

### B-11 — Global `PIP_NO_CACHE_DIR=1` disables the required runtime pip cache

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/Containerfile:57-70`
- **Detail**: The environment variable is baked into the runtime image, not scoped to the build-only pip command. Consequently, a `pip-cache:/home/builder/.cache/pip` mount cannot cache runtime pip operations, contradicting the stated cache convention and causing offline runtime installs to miss an otherwise declared cache.
- **Evidence**: Required pip cache mount at `docs/infrastructure/ci-architecture.md:56`; global `PIP_NO_CACHE_DIR=1` at Containerfile lines 57-70.
- **Suggested route**: patch

### B-12 — `/workspace` is created after timestamp normalization

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/Containerfile:280-289`
- **Detail**: The reproducibility pass touches `/opt/node`, `/usr/local`, and `/home/builder`, then a later RUN creates `/workspace`. The new directory retains the current build timestamp, so otherwise identical builds differ in filesystem metadata and layer content whenever the source mount is absent.
- **Evidence**: `find ... touch` at lines 280-281 precedes `mkdir -p /workspace` at line 289.
- **Suggested route**: patch

### B-13 — Reproducibility normalization and verification omit the APT-modified filesystem

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/Containerfile:266-281`
- **Detail**: The normalization pass excludes `/etc`, `/var/lib/dpkg`, `/var/log`, certificate outputs, and other paths changed by APT. The accompanying evidence checks only selected directory counts/bytes, not the complete root filesystem or a deterministic image digest, so it cannot substantiate the broad reproducibility claim.
- **Evidence**: The pass is restricted to three paths at lines 280-281, while APT mutates the image at lines 117-123 and the comments claim reproducibility at lines 266-279.
- **Suggested route**: patch

### B-14 — Validator version checks do not enforce the pinned versions

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/validate-design:86-116`
- **Detail**: The checks accept any Python 3.11 patch, any Node 22 patch, any npm semver, and any output containing two dotted numbers for every package. Versions such as a future/broken `jsonschema`, `markdownlint`, or `markdown-link-check` release would pass even though the image's toolchain pins specify concrete versions.
- **Evidence**: Broad patterns at lines 86, 91, 95, 105-109, and 115-116; exact pins are recorded in `requirements.txt:34-45` and `toolchain-pins.md:121-127`.
- **Suggested route**: patch

### B-15 — Python dependency checks never import the checked packages

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/validate-design:105-106`
- **Detail**: The `jsonschema` and `pyyaml` checks import only `importlib.metadata` and read distribution metadata. A missing or corrupted `jsonschema`/`yaml` module can leave its `.dist-info` metadata intact and still produce a passing result, contradicting the script's “present and runnable” contract.
- **Evidence**: The commands at lines 105-106 never execute `import jsonschema` or `import yaml`.
- **Suggested route**: patch

### B-16 — Unknown validator arguments are silently accepted

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/validate-design:30-33`
- **Detail**: Only an exact first argument of `--verbose` is recognized; every typo or extra argument is ignored and the normal checks still return 0. This contradicts the stated fail-closed behavior and allows a misspelled CI invocation to appear successful rather than rejecting invalid input.
- **Evidence**: Argument parsing at lines 30-33 and the fail-closed claim at lines 15-17.
- **Suggested route**: patch

### B-17 — The default command bypasses the required validator and can false-green

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/Containerfile:303-308`
- **Detail**: The image has no `ENTRYPOINT` and defaults to `CMD ["bash"]`. A non-interactive `podman run image` therefore runs a shell rather than `validate-design` and can exit successfully without validating anything; correctness depends on every caller remembering an explicit command.
- **Evidence**: The required validator is installed at Containerfile lines 194-206, but the default runtime command is `bash` at lines 303-308; the image purpose is docs validation in `ci-architecture.md:72-73`.
- **Suggested route**: patch

### B-18 — No negative-path tests or CI integration evidence were added

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/validate-design:52-80`
- **Detail**: The diff contains no automated test or workflow assertion for invalid design documents, missing/broken tools, malformed arguments, read-only source mounts, writable report mounts, or offline execution. The only demonstrated behavior is the happy path, leaving the fail-closed and mount/network contracts unverified.
- **Evidence**: The checker implementation has no test companion, and the diff adds no test file; only the success-oriented `check` helper is present at lines 52-80.
- **Suggested route**: patch

## Summary

- **Total findings**: 18
- **By severity**: 1 critical, 8 high, 9 medium, 0 low, 0 info
- **Top concerns**: The required design validator is effectively a version smoke test, the output-mount and default-runtime contracts are incomplete, and the build consumes unpinned/unlisted external inputs despite claiming a pinned reproducible image.
- **Out-of-scope items**: Generated coordination artifacts and unrelated phase-plan edits were not assessed as product implementation.
