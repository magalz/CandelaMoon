# Brahms Blue-Team Review — P1-002 candelamoon-docs Containerfile

## Disposition summary

- **Total findings reviewed:** 7
- **apply-now:** 2 (SEC-01, SEC-02)
- **defer-to-CI:** 4 (SEC-03, SEC-04, SEC-05, SEC-06)
- **dismiss:** 1 (SEC-07; functional scope is explicitly deferred to P1-017)

The highest-priority mitigation is **SEC-02**: prevent pip from accepting source
distributions and executing build code as root. Move the builder account setup
before the pip block, download only hash-verified wheels as `builder`, and have
root install only those local wheels with `--only-binary=:all:` and `--no-index`.

## Findings

### SEC-01 — Workspace files can hijack Python imports (HIGH)

- **Red-team reference:** SEC-01 (HIGH), “Workspace files hijack Python version checks.”
- **Assessment:** Confirmed. `WORKDIR /workspace` is a bind-mounted repository,
  and `python3 -c` places the current directory on the import path. The checks at
  `validate-design` lines 126-127 therefore can import `/workspace/jsonschema.py`
  or `/workspace/yaml.py` before the installed packages. The malicious module
  runs as the `builder` user during the validator invocation.
- **Mitigation:** **apply-now.**
  1. Run the two import checks with isolated Python, for example:
     `python3 -I -c "import jsonschema; print(jsonschema.__version__)"` and
     `python3 -I -c "import yaml; print(yaml.__version__)"`.
  2. Add `cd /` before the checks so accidental relative-file behavior cannot
     use the repository as the process working directory. Any future P1-017
     document inputs must use an explicit path such as `/workspace/docs`.
  3. Use the same `python3 -I` rule for every future Python validator command;
     do not rely on `PYTHONPATH`, the current directory, or user site packages.
- **Side effects:** Isolated mode intentionally prevents local project modules,
  `PYTHONPATH`, and the user site from satisfying imports. That is appropriate
  for these checks because their contract is to test image-baked dependencies;
  future validator code must import its own trusted code from an image path.
  `cd /` requires future document validation to use explicit workspace paths.
  No new privilege or network capability is introduced.
- **Disposition:** **apply-now**.

### SEC-02 — pip can execute a source distribution as root (CRITICAL)

- **Red-team reference:** SEC-02 (CRITICAL), “pip executes untrusted
  distribution as ROOT.”
- **Assessment:** Confirmed. `--require-hashes` authenticates the selected
  artifact but does not require a wheel. The lock contains artifact hashes and
  `pip install` at Containerfile line 192 runs before the final `USER builder`.
  A permitted sdist can execute `setup.py` or a PEP 517 build backend as UID 0;
  `--no-deps` does not change that behavior.
- **Mitigation:** **apply-now.** Restructure the build as follows:
  1. Move the existing builder-account creation and identity checks above the
     Python dependency block. Create a builder-owned temporary wheelhouse.
  2. Temporarily switch to `USER builder` and run a network download using
     `python3 -m pip download --require-hashes --no-deps
     --only-binary=:all: -r /tmp/requirements.lock -d /tmp/...-wheelhouse`.
     Use `COPY --chown=builder:builder` for the lock and verify the wheelhouse
     contains only `.whl` files.
  3. Switch back to `USER root` and install only the staged artifacts with
     `python3 -m pip install --no-cache-dir --require-hashes --no-deps
     --only-binary=:all: --no-index --find-links=/tmp/...-wheelhouse
     -r /tmp/requirements.lock`, then remove the lock and wheelhouse.
     Keep the final `USER builder` directive unchanged.
  4. Regenerate or reject the lock if any target package lacks a compatible
     Linux x86_64 Python 3.11 wheel. `--only-binary=:all:` must remain in the
     install command so a future lock change fails closed instead of falling
     back to an sdist.
- **Side effects:** Wheel-only installation can fail when a newly selected
  version has no wheel for the image's target platform; that is a deliberate
  build failure and requires a reviewed lock refresh. The extra download layer
  consumes build space, but cleanup preserves the current image size goal.
  Installing from wheels leaves the final packages root-owned while all
  network retrieval and any package parsing occur as `builder`; no source build
  backend is given root execution. A malicious wheel can still contain runtime
  code, so SEC-04 and the runtime sandbox remain necessary.
- **Disposition:** **apply-now**.

### SEC-03 — Build-time network allowlist is only documentation (HIGH)

- **Red-team reference:** SEC-03 (HIGH), “Build-time network allowlist is
  documentation only.”
- **Assessment:** Confirmed. The allowlist in the Containerfile comments does
  not constrain DNS, redirects, proxy behavior, dependency code, or the network
  namespace. `apt`, `curl`, pip, npm, and any code they execute can attempt
  egress to destinations outside the four documented domains.
- **Mitigation:** **defer-to-CI.** Enforce the policy on the Linux build runner,
  not with comments or an untrusted build argument:
  1. Build on a dedicated default-deny network namespace. Permit only an
     approved HTTPS/package proxy or firewall destinations for
     `deb.debian.org`, `nodejs.org`, `pypi.org`,
     `files.pythonhosted.org`, and `registry.npmjs.org`; block direct IP,
     IPv6, host-network, loopback, and RFC1918 bypasses.
  2. Invoke Podman with a named restricted build network and fail the job if
     the build is run with `--network=host` or an unrestricted default network.
     If a proxy is used, block direct egress so `HTTP(S)_PROXY` is not merely
     advisory. Permit only reviewed redirect/CDN endpoints required by those
     repositories.
  3. Prefer a stronger CI mode that prefetches the Node archive, Python
     wheelhouse, npm cache, and apt snapshot through that proxy, then builds
     with `podman build --network=none` and local inputs. Record the artifact
     hashes in the job evidence.
- **Side effects:** A strict proxy/firewall can break legitimate repository
  redirects or Debian mirror changes, so the allowed endpoint set needs an
  owned update process. Prefetching increases cache/context management. A proxy
  must not become a broad trusted bypass; preserve TLS verification and keep
  its CA/configuration out of image layers.
- **Disposition:** **defer-to-CI**.

### SEC-04 — `npm --ignore-scripts` does not sandbox runtime JavaScript (HIGH)

- **Red-team reference:** SEC-04 (HIGH), “npm `--ignore-scripts` doesn't
  sandbox runtime code.”
- **Assessment:** Confirmed, but limited to runtime execution. The current
  `npm ci --ignore-scripts` prevents lifecycle hooks during installation and
  the lockfile integrity hashes constrain the selected tree. It does not stop
  JavaScript in `markdownlint` or `markdown-link-check` (or their transitive
  modules) from running when `validate-design` invokes `--version` at lines
  135-136, or when a caller runs either CLI.
- **Mitigation:** **defer-to-CI.** Keep `npm ci --ignore-scripts`, exact
  lockfile integrity, and root-owned `/opt/node` as install-time controls, and
  require every validation invocation to use a hardened runtime:
  `--network=none --read-only --cap-drop=ALL
  --security-opt=no-new-privileges --user=1000:1000`, a read-only
  `/workspace` bind mount, and small `tmpfs` mounts for `/tmp` or explicitly
  approved output. Do not mount the Podman/Docker socket, credentials, or host
  namespaces, and allowlist the command to `validate-design`/approved tools.
  Add a CI check that the lockfile is unchanged during `npm ci` and that no
  install script is enabled. If link checking is needed, run it in a separate
  job with a destination allowlist rather than treating `--ignore-scripts` as
  a runtime sandbox.
- **Side effects:** Read-only execution may require an explicit temporary
  directory or output mount; the current MVP version checks do not need more
  than that. `--network=none` prevents a legitimate networked link check, so
  that operation must be separated and governed by its own egress policy.
  The remaining third-party code still runs, but only as UID 1000 in a
  disposable, capability-free container.
- **Disposition:** **defer-to-CI**.

### SEC-05 — Runtime network isolation is not enforced (HIGH)

- **Red-team reference:** SEC-05 (HIGH), “Runtime network isolation not
  enforced.”
- **Assessment:** Confirmed. `CMD ["validate-design"]` and comments recommend
  `--network=none`, but an ordinary `podman run` gets the engine's default
  network and callers can override the command or entrypoint. A network-capable
  `markdown-link-check` can then be used to make requests to destinations
  selected by repository content or command arguments, creating SSRF exposure.
- **Mitigation:** **defer-to-CI.** Make the merge-gate invocation an exact,
  centrally owned command, for example:
  `podman run --rm --network=none --read-only --cap-drop=ALL
  --security-opt=no-new-privileges --user=1000:1000
  --mount type=bind,src="$WORKSPACE",dst=/workspace,ro
  --tmpfs /tmp:rw,nosuid,nodev,noexec candelamoon-docs:review
  validate-design`.
  Reject privileged mode, host networking, arbitrary entrypoints, secret
  mounts, and runtime socket mounts in the CI policy. Add a negative test that
  the docs-validation job cannot reach a known external endpoint. For any
  intentional link-check job, validate URLs before invocation and use a
  separate non-host network with an egress proxy that blocks loopback,
  link-local, RFC1918, metadata, and other internal destinations.
- **Side effects:** The default validation path becomes offline by design and
  may need `/tmp` or an explicit output directory. Networked link checking
  must be a separately authorized job, which adds orchestration but avoids
  weakening the normal file-validation boundary. A negative network test must
  use a controlled endpoint and not add credentials to the image.
- **Disposition:** **defer-to-CI**.

### SEC-06 — apt package versions drift (MEDIUM)

- **Red-team reference:** SEC-06 (MEDIUM), “Unversioned apt packages drift.”
- **Assessment:** Confirmed. `apt-get update` and unversioned installs at lines
  128-134 resolve the repository state at build time. A digest-pinned base
  pins the starting filesystem, not the later Debian package index or package
  revisions; the explanatory comment claiming otherwise is not an integrity
  control. This is the known cross-image issue shared with P1-001.
- **Mitigation:** **defer-to-CI** as the shared P1-001/P1-002 build policy:
  1. Build against a reviewed Debian snapshot or internal apt snapshot proxy
     selected by the base-image digest, while retaining Debian Release
     signature verification.
  2. Maintain an apt lock/manifest containing the exact versions of
     `ca-certificates`, `curl`, `git`, `xz-utils`, and required dependencies;
     install with `package=version` and assert with
     `dpkg-query -W -f='${Package}=${Version}\n'`.
  3. Make the CI gate fail if the snapshot identifier or installed manifest
     differs from the reviewed record. Refresh the snapshot and base digest
     together through the existing security-update process.
- **Side effects:** Snapshot maintenance adds an update task and can make a
  build fail when a package is removed or a dependency set changes. Pinning
  also delays security fixes until a reviewed refresh, so the refresh cadence
  must be explicit. Do not solve this by disabling apt signature checks or by
  allowing an unrestricted mirror.
- **Disposition:** **defer-to-CI**.

### SEC-07 — Default validator checks presence, not document semantics (MEDIUM)

- **Red-team reference:** SEC-07 (MEDIUM), “Default validator is tool-presence
  only.”
- **Assessment:** The observation is accurate as a capability statement, but
  it is not an exploitable container-security defect in this change. The
  Containerfile and script explicitly label P1-002 as MVP tool-presence scope
  and explicitly identify real `/workspace/docs` validation as P1-017 follow-up
  work (Containerfile lines 238-242; `validate-design` lines 9-14).
- **Mitigation:** No merge-blocking security change for P1-002. Preserve the
  fail-closed tool/version checks and create or retain the P1-017 work item for
  schema, ADR, capability-matrix, and evidence-manifest validation. P1-017
  should use the SEC-01 isolated-import rule and explicit `/workspace` paths
  when it begins parsing repository content.
- **Side effects:** Pulling full document validation into P1-002 would expand
  scope and add parser/input attack surface without addressing a current
  container escape. The follow-up should receive its own threat model and
  tests.
- **Disposition:** **dismiss** for the P1-002 security review; **deferred to
  P1-017** as an explicitly documented functional follow-up.
