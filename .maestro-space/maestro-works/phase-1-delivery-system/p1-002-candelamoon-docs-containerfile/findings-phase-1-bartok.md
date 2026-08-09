# Findings Report — Bartók (Phase 1)

- **Reviewer**: Bartók (`edge-case-hunter`)
- **Task**: P1-002 — Create candelamoon-docs Containerfile
- **Branch**: not provided
- **Base SHA**: `86d3c216eb2539cec76556978cc7e36941dfaca8`
- **Head SHA**: `e37c8c189b2505b11e36093c629fe6430839031f`
- **Date**: 2026-08-09
- **Dispatched by**: not provided

---

## Scope

Reviewed only the requested diff (`git diff 86d3c216eb2539cec76556978cc7e36941dfaca8..e37c8c189b2505b11e36093c629fe6430839031f`), concentrating on `infra/containers/candelamoon-docs/Containerfile`, `requirements.txt`, and `validate-design`. The review did not use the handoff, plan, ADR context, author rationale, or conversation history. The scoped diff contains additions rather than deleted symbols; the `linkchecker` replacement is treated as a functional omission/deletion scenario.

## Method

Walked every shell branch, package-install path, user/volume lifecycle path, platform-dependent path, validation failure path, argument path, timestamp/rebuild path, offline path, and missing/unreadable-resource path in the three files. For each path, checked null/empty output, non-zero status, wrong version, disconnected network, alternate architecture, wall-clock variation, mount masking, and whether failure is logged and non-zero. No literal deletion hunk or dangling deleted symbol exists in the scoped diff.

## Findings

### BAR-001 — The Node installation is hard-coded to x86_64 while the base image is platform-selectable

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/Containerfile:97-100, 139-144`
- **Detail**: `NODE_SHA256_LINUX_X64` and the download URL always select `node-v${NODE_VERSION}-linux-x64.tar.xz`, but `FROM` has no `--platform=linux/amd64` and no `TARGETARCH` branch. On an `arm64`, `armv7`, `ppc64le`, or other native build, the Python base can resolve for the target architecture, the x64 tarball can still extract successfully, and the first `npm install` then fails with an executable-format error; an emulated build still produces an image that requires emulation at runtime. There is no architecture-specific failure message or recovery path.
- **Evidence**: The only architecture selector is the literal `linux-x64` URL and the matching x64 SHA variable.
- **Suggested route**: patch with per-architecture URLs and hashes keyed from `TARGETARCH`, or explicitly pin the whole image to `linux/amd64` and enforce/document that platform.

### BAR-002 — Digest-pinning the base does not pin the unversioned apt packages

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/Containerfile:112-123`
- **Detail**: With the same base digest, `apt-get update` reads the live Debian trixie indexes and `apt-get install` selects the current candidates for `ca-certificates`, `curl`, `git`, and `xz-utils`. A rebuild after a repository update, mirror change, package removal, or expired metadata can therefore install a different tree or fail, despite the comment claiming the pinned base prevents drift. This is an unlogged build-time variation and undermines the stated reproducibility contract.
- **Evidence**: Package names have no versions or snapshot source, and the command refreshes indexes on every build.
- **Suggested route**: patch to a dated Debian snapshot plus exact package versions/hashes, or explicitly classify the image as non-reproducible until apt snapshotting is supplied.

### BAR-003 — The pip dependency graph is not actually locked

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/requirements.txt:11-14, 34, 39, 45`; `infra/containers/candelamoon-docs/Containerfile:154-169`
- **Detail**: Only the three direct requirements are exact-pinned; `attrs`, `pathspec`, `rpds-py`, `referencing`, and other transitive packages are resolved from current PyPI metadata on each build. A later transitive release, yanked wheel, changed Python constraint, or platform-specific resolution changes the image or makes a rebuild fail. Recording `pip freeze` after one build is evidence, not a reproducible input.
- **Evidence**: The requirements file explicitly says transitive dependencies are resolved at build time, and the install uses only `-r requirements.txt`.
- **Suggested route**: patch with a fully resolved constraints/lock file and verify it in CI; include all transitive requirements in the lock.

### BAR-004 — PyPI artifacts are accepted without hash verification

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/requirements.txt:11-14, 34, 39, 45`; `infra/containers/candelamoon-docs/Containerfile:167-170`
- **Detail**: `pip install --no-cache-dir -r /tmp/requirements.txt` authenticates HTTPS but does not require hashes. If an index/mirror serves a modified wheel under an allowed version, or a different platform artifact is selected, pip accepts it; exact version syntax alone does not prove artifact identity. This is especially inconsistent with the Node tarball's explicit SHA-256 verification and leaves a root-run install path without a fail-closed integrity check.
- **Evidence**: There are no `--hash=sha256:...` entries and no `--require-hashes` option.
- **Suggested route**: patch the lock/requirements input with hashes for every resolved artifact and install with `--require-hashes` against an explicitly controlled index.

### BAR-005 — Global npm installs float transitive packages and execute install hooks as root

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/Containerfile:176-192`
- **Detail**: Exact top-level versions (`markdownlint-cli@0.45.0` and `markdown-link-check@3.13.7`) do not lock their transitive semver ranges, and no lockfile or package-integrity allowlist is supplied. A later registry resolution can change the installed graph, while npm lifecycle scripts run during both installs as root and may execute changed code or make additional network requests. `npm cache clean` only removes cache data; it does not make resolution deterministic or integrity-verified.
- **Evidence**: Both commands are `npm install -g <name>@<version>` with no lockfile, `npm ci`, hash verification, or script restriction.
- **Suggested route**: patch to a committed lock/integrity-checked install (or a verified offline package bundle) and restrict lifecycle scripts where the selected packages permit it.

### BAR-006 — Python checks verify distribution metadata, not package importability or behavior

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/validate-design:98-106`
- **Detail**: The comments promise an import check, but the commands only import `importlib.metadata` and query `m.version('jsonschema')` or `m.version('PyYAML')`. If a `.dist-info` directory remains while `jsonschema` or `yaml` files are missing, corrupt, or unusable, the command exits zero and the validator reports `OK`; the final “present and runnable” claim is false. The same path does not exercise any actual schema or YAML operation.
- **Evidence**: No `import jsonschema` or `import yaml` appears in either Python check.
- **Suggested route**: patch each check to import the actual module and perform a minimal API smoke operation, then assert the expected distribution version.

### BAR-007 — Version regexes can accept the wrong tool or an unrelated warning

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/validate-design:61, 86, 91, 95, 105-106, 109, 115-116`
- **Detail**: Most checks accept any unanchored `[0-9]+\.[0-9]+` fragment; npm accepts any three-component number, and Node accepts any `v22.x` patch. If a wrong executable is earlier on a runtime-overridden `PATH`, or a command exits zero after printing a warning containing a dotted number, the check can pass without proving the pinned tool/version. This also allows a changed direct dependency version to pass the guard.
- **Evidence**: The expected patterns do not encode `4.23.0`, `6.0.2`, `1.37.1`, `0.45.0`, `3.13.7`, or `10.9.8`, and matching is not anchored to the complete version line.
- **Suggested route**: patch to exact expected versions (allow only a narrowly defined product prefix) and invoke critical binaries by absolute path or a controlled PATH.

### BAR-008 — Unknown command-line arguments are silently ignored

- **Severity**: low
- **Location**: `infra/containers/candelamoon-docs/validate-design:30-33`
- **Detail**: Only the first argument equal to `--verbose` has an effect; every other argument, including a typo such as `--verbsoe`, a path, or an extra option after `--verbose`, is ignored. The command can therefore return zero while the caller believes it requested a mode or target that was never applied, violating the script's fail-closed behavior.
- **Evidence**: There is no argument-count check, `case` default, or rejection branch.
- **Suggested route**: patch with explicit parsing for the supported forms and exit non-zero with usage text for every unknown or extra argument.

### BAR-009 — The sudoers guard fails open on missing/unreadable files and has blind spots

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/Containerfile:242-244`
- **Detail**: `grep` returns status 2 for a missing path, permission/I/O error, or other read failure; the leading `!` converts that error into status 0, so the `||` error branch is skipped. The common case where `/etc/sudoers.d/` is absent therefore does not prove the check passed, and a matching `/etc/sudoers` rule can be masked by an error on the second path. The anchored expression also misses indented rules, aliases, and some included/symlinked configurations. The advertised “fail closed” postcondition is not achieved.
- **Evidence**: `2>/dev/null` hides the diagnostic and the command tests both paths in one negated invocation.
- **Suggested route**: patch to distinguish grep status 1 (no match) from status 2 (check failure), inspect only existing regular files, and use a syntax-aware sudoers check when sudoers is present.

### BAR-010 — Timestamp normalization runs before `/workspace` is created and skips other generated paths

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/Containerfile:266-281, 283-289`
- **Detail**: The `find` command normalizes only `/opt/node`, `/usr/local`, and `/home/builder`; the next `RUN` creates `/workspace`, whose directory mtime is wall-clock dependent. Apt also changes metadata under `/etc` and `/var`, which is never normalized. Two ordinary builds at different times can therefore differ in layer metadata even with the same `SOURCE_DATE_EPOCH`; the acknowledged gzip variation is not the only source of non-reproducibility.
- **Evidence**: `RUN mkdir -p /workspace` appears after the only `touch` pass, and the touch roots exclude `/etc`, `/var`, `/tmp`, and `/workspace`.
- **Suggested route**: create all image-owned directories before the final normalization pass and normalize every generated path, or use an engine-level timestamp rewrite as a required build invariant.

### BAR-011 — Replacing `linkchecker` with `markdown-link-check` can break existing callers

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/requirements.txt:16-23`; `infra/containers/candelamoon-docs/Containerfile:172-192`
- **Detail**: The pip `linkchecker` executable is intentionally omitted and no compatibility wrapper is installed. If a docs job, developer command, or future validator invokes `linkchecker` or relies on its flags/output format, the image fails with command-not-found or a semantic CLI mismatch even though a differently named npm package is present. This is the functional deletion/skip path in the scoped diff.
- **Evidence**: The requirements comments explicitly say `linkchecker` is not in the file, while only `markdown-link-check` is installed globally.
- **Suggested route**: update every consumer in the same change, or provide a documented compatibility wrapper and tests for the expected link-check invocation.

### BAR-012 — The installed link checker conflicts with the documented network-none runtime path for remote links

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/validate-design:19-22, 111-116`; `infra/containers/candelamoon-docs/Containerfile:172-192`
- **Detail**: `markdown-link-check` normally resolves HTTP(S) targets, while the runtime contract says validation runs with `--network=none`. When the eventual docs validation invokes it on an external link, DNS/connect attempts fail or wait for client timeouts; the current MVP only checks `--version`, so this incompatibility is not exercised. A disconnected environment therefore turns valid remote links into failures or slow CI rather than a controlled offline result.
- **Evidence**: The script says it must make no network calls, but the image installs a network-oriented link checker and exposes no offline mode, URL classification, or timeout policy.
- **Suggested route**: separate local/offline link validation from a network-enabled job, or explicitly configure the checker to skip remote links and bound each request timeout.

### BAR-013 — The advertised pip cache volume is disabled by a runtime-persistent environment variable

- **Severity**: low
- **Location**: `infra/containers/candelamoon-docs/Containerfile:57-60, 66-75, 253-264`
- **Detail**: `PIP_NO_CACHE_DIR=1` is an `ENV`, so it remains set after `USER builder`; pip will neither read nor populate the `/home/builder/.cache/pip` cache under its default behavior. If a follow-up validator or developer runs pip in the offline container expecting the documented cache mount to supply artifacts, the install cannot reuse that cache and fails rather than recovering from the mounted data.
- **Evidence**: The file simultaneously exports `PIP_NO_CACHE_DIR=1` and describes `/home/builder/.cache/pip` as the runtime cache.
- **Suggested route**: scope no-cache behavior to the build install, unset it in the runtime environment, or remove the cache contract and test the intended runtime behavior.

### BAR-014 — Image-time ownership does not protect bind mounts or pre-existing cache volumes

- **Severity**: low
- **Location**: `infra/containers/candelamoon-docs/Containerfile:253-264, 283-301`
- **Detail**: The image chowns `/home/builder` and `/workspace` before runtime mounts exist. A host bind mount at `/workspace`, or an existing `pip-cache`/`npm-cache` volume owned by another UID or mode 0700, masks those image paths; uid 1000 then cannot read the source or write the cache. `--userns=keep-id` helps only when the host identity and mount ownership line up, and there is no runtime permission diagnostic.
- **Evidence**: The only `chown` operations are build-time `RUN` steps, followed by a fixed `USER builder` and a documented mount-over path.
- **Suggested route**: add a runtime mount/permission preflight with a clear error, document required ownership/read-only modes, or use an entrypoint that safely initializes owned volumes.

### BAR-015 — A hung tool can hang the validator indefinitely

- **Severity**: low
- **Location**: `infra/containers/candelamoon-docs/validate-design:52-80`
- **Detail**: `check` invokes each executable synchronously and has no per-command timeout. A broken filesystem, a runtime PATH override, or a tool that waits on a stalled configuration/cache can leave the whole docs job waiting forever instead of recording an error; the `--network=none` policy does not bound a local process. The caller's outer CI timeout is the only escape.
- **Evidence**: The function captures `out=$([command])` directly and contains no timeout, alarm, or cancellation path.
- **Suggested route**: patch each probe through a bounded timeout and report timeout distinctly from ordinary command failure.

## Summary

- Total findings: **15**
- By severity: **2 high, 9 medium, 4 low, 0 critical, 0 info**
- Top concerns: The x64-only Node payload breaks non-amd64 builds, live/unhashed apt/Python/npm dependency resolution undermines reproducibility and supply-chain integrity, and the metadata/regex-only validator can report corrupted or wrong tools as healthy.
- Out-of-scope items: Other files in the larger commit, CI workflow callers, handoff/plan/ADR context, and author rationale were not used; any caller compatibility issue is reported only as an explicitly conditional edge case.
