# Findings Report — Stravinsky (Phase 2)

- **Reviewer**: Stravinsky (`stravinsky-red-team-analyst`)
- **Task**: P1-002 — candelamoon-docs Containerfile
- **Branch**: `phase1/p1-002-candelamoon-docs-containerfile`
- **Base SHA**: `86d3c216eb2539cec76556978cc7e36941dfaca8`
- **Head SHA**: `0c80776971c86ddbfe60232cdfe9cdb4ebd42331`
- **Date**: 2026-08-09
- **Dispatched by**: not provided

---

## Scope

Reviewed `git diff 86d3c216eb2539cec76556978cc7e36941dfaca8..HEAD`, focusing on:

- `infra/containers/candelamoon-docs/Containerfile`
- `infra/containers/candelamoon-docs/validate-design`
- `infra/containers/candelamoon-docs/requirements.txt`
- `infra/containers/candelamoon-docs/requirements.lock`
- `infra/containers/candelamoon-docs/package.json`
- `infra/containers/candelamoon-docs/package-lock.json`

No handoff, plan, ADR, author rationale, or conversation history was used.

## Method

Applied STRIDE to the build boundary, runtime command, bind-mounted workspace, and
dependency supply chains. Applied container/CI OWASP checks for uncontrolled search
paths, dependency confusion/supply-chain execution, SSRF, build-time egress, secret
exposure, privilege boundaries, and validation bypass. The review specifically tested
the claimed network and non-root boundaries against the actual instructions rather than
their comments.

## Findings

### SEC-01 — Workspace files hijack the Python version checks

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/validate-design:126-127`
- **Detail**: The script runs `python3 -c` while the image `WORKDIR` is the
  bind-mounted `/workspace`. Python places the current directory ahead of installed
  site-packages for `-c` execution. A repository file named `jsonschema.py` or `yaml.py`
  therefore replaces the package that the check claims to verify. The module executes
  arbitrary Python during import and can report the expected `__version__`, so the
  check both executes attacker code and still returns a green result.
- **Attack scenario**: An attacker submits an otherwise ordinary pull request that
  adds `jsonschema.py` at the repository root. The CI runner mounts the checkout at
  `/workspace` and starts the default `validate-design` command. The first import runs
  the attacker's code as `builder`; it reads the checkout and any credentials exposed
  to the container, modifies writable workspace files, and sets
  `__version__ = "4.23.0"`. The validator prints success, masking the tampering. A
  `yaml.py` file provides the same path for the second check.
- **Exploitability**: Remote authenticated/untrusted-PR attacker; automatic CI run
  is sufficient, with no physical access. Impact is limited to the container's
  `builder` privileges when `--network=none` is actually enforced, but CI environment
  variables, cache mounts, and the source checkout remain reachable.
- **Evidence**: `Containerfile:311-350` makes `/workspace` the runtime workdir and
  bind-mount target; `validate-design:126-127` imports unqualified module names.
- **Suggested route**: patch

### SEC-02 — Pip can execute an untrusted distribution as root while building the image

- **Severity**: critical
- **Location**: `infra/containers/candelamoon-docs/Containerfile:190-193`
- **Detail**: The dependency install occurs before `USER builder`, and the command
  does not require wheels. A hash-locked source distribution is still executable code:
  pip may run its `setup.py`/PEP 517 build backend and install hooks as UID 0. The
  SHA-256 requirement authenticates the selected bytes, not the intent of the package,
  and `--no-deps` does not disable build-backend execution.
- **Attack scenario**: A dependency maintainer, compromised package account, or
  compromised dependency-update process introduces a malicious source distribution and
  its hash into the reviewed lock. A routine image rebuild runs `pip install` as root;
  the package build hook writes a backdoor into `/usr/local` or `/opt`, alters the
  validator, and captures any build credentials or artifacts available to the build.
  Every consumer of the resulting image then executes the poisoned toolchain.
- **Exploitability**: Remote supply-chain attacker or attacker able to land an
  approved lock refresh; the normal automated image build triggers it. No physical
  access is required. The resulting code runs with build-time root privileges and can
  affect the published image, although host escape still depends on the container
  builder.
- **Evidence**: `PIP_ROOT_USER_ACTION=ignore` documents root installation at
  `Containerfile:76-77`; `USER builder` is not set until line 344. The lock contains
  source-compatible artifact hashes, while the install has no binary-only constraint.
- **Suggested route**: patch

### SEC-03 — The build-time network allowlist is documentation only

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/Containerfile:36-43,189-193`
- **Detail**: The file lists an endpoint allowlist, but no `RUN` instruction or other
  image-level mechanism constrains build egress. Package build code executes inside a
  normal networked build step, so it can connect to destinations outside PyPI, npm,
  Debian, or nodejs.org. The runtime `--network=none` convention does not protect the
  build phase.
- **Attack scenario**: During a rebuild, a malicious Python build backend from the
  locked dependency set opens a socket to `169.254.169.254`, a private `10.0.0.0/8`
  service, or an attacker-controlled collector. It probes internal services and sends
  back build environment data while the build still has network access; the build
  completes and produces an image containing any payload written by the hook.
- **Exploitability**: Remote supply-chain attacker plus an automated build on a runner
  with unrestricted egress; no physical access. Exploitation fails only if the external
  builder independently supplies an effective egress firewall, which this image does
  not establish.
- **Evidence**: The only allowlist is comments at `Containerfile:36-43`; the pip
  install is an ordinary network-capable `RUN` at lines 191-192.
- **Suggested route**: patch

### SEC-04 — `npm ci --ignore-scripts` does not sandbox runtime dependency code

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/Containerfile:203-231`
- **Detail**: `--ignore-scripts` suppresses npm lifecycle hooks during installation,
  but the image then exposes the complete third-party tree as executable global CLI
  tools. Running a CLI or even its version path loads JavaScript from the package and
  its transitive dependencies. Lock integrity proves that the bytes match the locked
  release; it does not make a compromised or maliciously published release safe.
- **Attack scenario**: An attacker compromises an npm maintainer account or gets a
  backdoored dependency accepted in a lock refresh. The build succeeds because install
  hooks are ignored. On the next CI run, `validate-design` executes
  `markdownlint --version` and `markdown-link-check --version`, or the docs job runs
  those CLIs over the checkout. The malicious module runs as `builder`, reads the
  `/workspace` checkout and CI environment, alters reports, and exfiltrates data when
  runtime networking is available.
- **Exploitability**: Remote supply-chain attacker; the ordinary CI startup or docs
  validation command supplies the trigger. No physical access is required. The
  process is non-root, but it can access all files and environment data available to
  the builder and can tamper with the mounted workspace.
- **Evidence**: `package.json:7-8` selects the CLIs; `package-lock.json:1049-1067`
  and `1101-1124` show their executable entries; `validate-design:135-136` invokes
  them after installation.
- **Suggested route**: patch

### SEC-05 — Runtime network isolation is not enforced, enabling link-checker SSRF

- **Severity**: high
- **Location**: `infra/containers/candelamoon-docs/Containerfile:195-217,352-358`
- **Detail**: The image contains a network-capable Markdown link checker and its
  proxy/HTTP stack, but `--network=none` exists only in comments and an example
  invocation. Any caller that omits the flag gives the checker normal network access.
  Markdown links are repository-controlled input, so the tool becomes an SSRF and
  internal-network request primitive.
- **Attack scenario**: An attacker adds a Markdown link such as
  `http://169.254.169.254/latest/meta-data/` or
  `http://127.0.0.1:2375/containers/json` to a pull request. A networked docs-validate
  job invokes `markdown-link-check`; it fetches the attacker-selected endpoint (and
  can follow an attacker-controlled redirect), probing or triggering internal HTTP
  services and exposing response-derived status/data through the validation report.
- **Exploitability**: Remote authenticated/untrusted-PR attacker with automatic CI
  execution, provided the job or developer grants the container network access. No
  physical access is required; the image itself provides no enforcement when the
  launcher is misconfigured.
- **Evidence**: `package-lock.json:828-839` wires `link-check`, and
  `1884-1897` wires proxy-capable clients; `Containerfile:353-354` presents
  `--network=none` as caller convention rather than an image property.
- **Suggested route**: patch

### SEC-06 — Unversioned apt packages drift into a privileged build and runtime image

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/Containerfile:123-134`
- **Detail**: The base image is digest-pinned, but `ca-certificates`, `curl`, `git`,
  and `xz-utils` are selected from the live Debian repository with no package version
  or snapshot pin. A base digest therefore does not make the installed build tools
  immutable; a later rebuild can silently consume a newly compromised or vulnerable
  signed package.
- **Attack scenario**: An upstream Debian package or signing/repository supply chain
  is compromised and publishes a malicious `xz-utils` or `curl` update. A scheduled
  rebuild accepts the signed, newest package, and the root build executes it while
  extracting Node or downloading dependencies. The package can poison `/opt/node`, the
  validator, or the published image without any source-code change in this repository.
- **Exploitability**: Remote supply-chain attacker; exploitation requires control of
  an upstream signed distribution path and a subsequent automated rebuild. No physical
  access is required. A normal external repository signature check does not address
  malicious code legitimately shipped in a trusted release.
- **Evidence**: `apt-get update` and unversioned package names are at
  `Containerfile:128-134`; the comment at lines 123-127 incorrectly treats the base
  digest as pinning the apt package set.
- **Suggested route**: patch

### SEC-07 — The default validator is a tool-presence check, not design validation

- **Severity**: medium
- **Location**: `infra/containers/candelamoon-docs/validate-design:9-14,101-143`
- **Detail**: The default command never opens `/workspace/docs`, schemas, ADRs,
  capability matrices, or evidence manifests. It returns success after checking tool
  versions only. If the CI result is treated as the design-integrity gate, the named
  validator can be satisfied while all governed design content is absent, malformed, or
  tampered with.
- **Attack scenario**: A pull-request author changes an architecture schema or removes
  evidence required by the delivery policy. CI starts the image's default
  `validate-design` command; every installed tool reports its expected version, no
  design file is examined, and the command exits 0. The pipeline therefore accepts or
  publishes a tampered design as if it had passed validation.
- **Exploitability**: Remote authenticated/untrusted-PR attacker; automatic CI is the
  only trigger. No physical access is required. The impact is conditional on this exit
  status being used as an authorization or release gate; the file itself labels the
  missing validation as a follow-up.
- **Evidence**: The explicit placeholder statement is at `validate-design:9-14`, and
  the only executable checks are the version checks at lines 101-136 followed by an
  unconditional success summary at lines 138-144.
- **Suggested route**: defer

## Summary

- **Total findings**: 7
- **By severity**: 1 critical, 4 high, 2 medium, 0 low, 0 info
- **Top concerns**: The build executes dependency-controlled Python code as root with
  build network access, allowing a supply-chain compromise to poison every produced
  image. Separately, a repository-controlled Python module can execute on every CI
  validation run despite the non-root runtime user and can spoof the green version
  result.
- **Out-of-scope items**: No direct shell command injection or path traversal was
  found in the current quoted argument handling. No secret is copied by the six
  production files themselves; the lock/manifests are not credentials. The final
  `USER builder` boundary and npm's install-time script suppression reduce, but do not
  eliminate, the runtime and supply-chain attack paths above.
