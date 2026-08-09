# Findings Report — Verdi (Phase 1)

- **Reviewer**: Verdi (`verdi-acceptance-analyst`)
- **Task**: P1-002 — candelamoon-docs Containerfile
- **Branch**: `phase1/p1-002-candelamoon-docs-containerfile`
- **Base SHA**: `86d3c216eb2539cec76556978cc7e36941dfaca8`
- **Head SHA**: `e37c8c189b2505b11e36093c629fe6430839031f`
- **Date**: 2026-08-09
- **Dispatched by**: not provided

---

## Scope

Reviewed the requested base-to-head diff, `ci-architecture.md` lines 53–58 and
69–76, and AC1–AC10. The handoff, plan, ADR context, author rationale, and
conversation history were not used; ADR 0014 was considered only where the
Containerfile itself cites it, as required by AC10.

## Method

Performed an AC-by-AC walkthrough, then built the image with Podman and ran the
runtime checks under `--network=none`. Two `--no-cache` builds were compared for
the AC8 measurements and for image-level reproducibility.

## Acceptance-criteria walkthrough

- **AC1 — Pass:** `infra/containers/candelamoon-docs/Containerfile` is added.
- **AC2 — Pass:** line 51 uses the required `docker.io/library/python:3.11-slim@sha256:...` form.
- **AC3 — Partial:** the requested packages and `/usr/local/bin/validate-design` are present, but the validator does not implement the schema/ADR/capability/evidence validation required by the spec; see A-01.
- **AC4 — Pass:** `USER builder` is the final USER directive; builder is uid/gid 1000 and both cache directories are chowned to builder.
- **AC5 — Gap:** the build reaches Debian mirrors and `nodejs.org`, beyond the three-host allowlist; see A-02.
- **AC6 — Pass for the tested invocation:** the image runs with `podman run --network=none`; the Containerfile cannot itself force a caller's runtime network flag.
- **AC7 — Pass:** a fresh build succeeded and Python, Node, markdownlint, yamllint, and `validate-design` all passed under `--network=none`.
- **AC8 — Partial:** pip freeze and file counts matched, but the inputs are not fully locked and the two image manifests/digests differed; see A-03.
- **AC9 — Pass:** the root `.containerignore` excludes the relevant metadata, handoff, build, cache, and secret paths; the two COPY sources remain reachable and the build context worked.
- **AC10 — Pass:** the Containerfile contains inline citations to `ci-architecture.md`, `toolchain-pins.md`, and ADR 0014.

## Findings

1. **A-01 — `validate-design` is only a tool-presence smoke test**

   - **Severity**: high
   - **Location**: `infra/containers/candelamoon-docs/validate-design:5-16,94-124`; `infra/containers/candelamoon-docs/Containerfile:194-206`
   - **Detail**: The spec defines this entrypoint as performing schema validation for architecture schemas, the ADR register, capability matrix, and evidence manifest, and calls for ADR/capability-matrix validation scripts. The delivered script only runs version/import-metadata checks and never reads `/workspace/docs`, validates a schema, or invokes any design-validation script. Its own comments defer the required behavior to P1-017, so AC3 is only satisfied at the pathname/tool-presence level.
   - **Evidence**: `ci-architecture.md:72` lists the required validation behavior; the script's checks are limited to `python3`, `node`, `npm`, package metadata, `yamllint`, `markdownlint`, and `markdown-link-check`.
   - **Suggested route**: patch

2. **A-02 — Build-time network is not limited to the AC5 allowlist**

   - **Severity**: high
   - **Location**: `infra/containers/candelamoon-docs/Containerfile:117-144`
   - **Detail**: The build performs `apt-get update/install`, which reaches Debian mirrors, and downloads the Node.js tarball from `https://nodejs.org`. Neither endpoint is in AC5's exact allowlist of `pypi.org`, `files.pythonhosted.org`, and `registry.npmjs.org`. Comments documenting the extra endpoint do not enforce a network policy, and the Containerfile has no allowlisted proxy or equivalent restriction.
   - **Evidence**: The fresh `podman build --no-cache` log showed `deb.debian.org` traffic at the apt step and `curl https://nodejs.org/dist/...` at the Node step; the source explicitly says `nodejs.org` was added to the allowlist, which contradicts AC5 as written.
   - **Suggested route**: decision-needed

3. **A-03 — Reproducibility is demonstrated only by coarse metrics, not by a locked image build**

   - **Severity**: medium
   - **Location**: `infra/containers/candelamoon-docs/Containerfile:117-123,168-192,266-281`; `infra/containers/candelamoon-docs/requirements.txt:30-45`
   - **Detail**: Direct Python and npm versions are pinned, but apt package versions, pip transitives, and npm transitives are resolved from mutable repositories at build time. The Containerfile also explicitly acknowledges that the image digest is not reproducible. In review, the two no-cache builds did have matching `pip freeze` output and file counts, but their image sizes were `770379222` and `770379221` bytes and their digests were `sha256:812c30e1...` and `sha256:a4c8b8d5...`. Thus the stated probes pass, but they do not prove stable image content or bit-reproducible rebuilds.
   - **Evidence**: The two builds' per-file content manifests matched, while `podman image inspect` reported different image IDs, sizes, and digests; the source comments at lines 276–279 call the digest difference a known debt. Unhashed transitive and apt inputs remain in the build.
   - **Suggested route**: patch

## Summary

- Total findings: **3**
- By severity: **0 critical, 2 high, 1 medium, 0 low, 0 info**
- Top concerns: The image contains a placeholder validator rather than the required design validation, and its build accesses endpoints outside the explicit network allowlist. AC8's narrow comparison metrics pass, but the dependency and image-level reproducibility contract is not fully met.
- Out-of-scope items: No findings were raised for the existing root `.containerignore`, the npm choice of `markdown-link-check` (explicitly permitted by the spec), or the runtime network flag when the caller supplies `--network=none`.
