---
change_id: "P1-002"
phase: "Phase 1"
task: "Create candelamoon-docs Containerfile — containerized docs validation environment (Python 3.11 slim, jsonschema, yamllint, markdown-link-check, Node.js 22 LTS + markdownlint-cli, design validator)"
status: "done"
repository: "magalz/CandelaMoon"
branch: "phase1/p1-002-candelamoon-docs-containerfile"
base_sha: "86d3c216eb2539cec76556978cc7e36941dfaca8"
head_sha: "91bd8403ad75a8d8b410ca4c48a172549f382302"
pr_url: ""
acceptance_criteria:
  - "AC1: Containerfile exists at `infra/containers/candelamoon-docs/Containerfile`."
  - "AC2: Base image is digest-pinned `docker.io/library/python:3.11-slim@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` (resolved via `podman pull` + `podman image inspect`; recorded in toolchain-pins.md § `Container Base Images` and § `Python`)."
  - "AC3: Installed tools match toolchain-pins.md: Python 3.11 (from base) + pinned pip deps (jsonschema 4.23.0, pyyaml 6.0.2, yamllint 1.37.1; link checker provided by npm `markdown-link-check@3.13.7` — see Deviations §1); Node.js 22 LTS resolved to 22.23.2 + markdownlint-cli 0.45.0; design validator entrypoint at `/usr/local/bin/validate-design` (MVP: asserts all tools are present and runnable; real validation logic against docs/ content is P1-017 follow-up); ADR/capability-matrix validation scripts deferred to P1-017."
  - "AC4: Non-root `builder` user (uid 1000, gid 1000) is the final USER directive. All pip/node caches (/home/builder/.cache/pip, /home/builder/.npm) chown'd to builder:builder."
  - "AC5: Build-time network limited to pypi.org / files.pythonhosted.org (pip), registry.npmjs.org (npm), nodejs.org (Node.js binary tarball), deb.debian.org (apt). All five domains are documented in the Containerfile's consolidated build-time network allowlist comment (header) and inline at each install step (B-03/B-04/A-02 fix)."
  - "AC6: Run-time network is `--network=none` (verified: `podman run --rm --network=none` cannot resolve DNS or open TCP connections)."
  - "AC7: `podman build` succeeds from repo root; `podman run --rm --network=none candelamoon-docs:test python3 --version` reports `Python 3.11.15`; `podman run --rm --network=none candelamoon-docs:test node --version` reports `v22.23.2`; `podman run --rm --network=none candelamoon-docs:test markdownlint --version` reports `0.45.0`; `podman run --rm --network=none candelamoon-docs:test yamllint --version` reports `yamllint 1.37.1`; `podman run --rm --network=none candelamoon-docs:test markdown-link-check --version` reports `3.13.7`."
  - "AC8: Image content is reproducible: two `--no-cache --source-date-epoch=1735689600 --rewrite-timestamp` builds produce identical pip freeze (10 entries), identical file counts (/opt/node 9532, /usr/local 2440, /home/builder 0), and identical total bytes (/opt/node 232233887, /usr/local 45961513, /home/builder 0). Image size matches exactly: 770379387 bytes. Image digest differs (sha256:a1090f0f... vs sha256:38a604f5...) due to Podman layer-tar gzip non-determinism — tracked as known debt per P1-001."
  - "AC9: Root `.containerignore` (existing from P1-001) is adequate for the docs build context. Verified by the build succeeding: `.git/` (639 files), `.maestro-space/` (110 files), and `docs/handoffs/` (4 files) are all excluded by the existing patterns; the docs Containerfile only COPYs `infra/containers/candelamoon-docs/requirements.txt` and `infra/containers/candelamoon-docs/validate-design` from the build context, both of which are correctly reachable. No additional exclusions needed."
  - "AC10: Containerfile carries inline comments linking each section to its governing doc (ci-architecture.md § `candelamoon-docs` / `Common conventions`; toolchain-pins.md § `Python 3.11` / `Node.js 22 LTS` / `Container Base Images`; ADR 0014)."
tdd_artifacts:
  atdd_checklist: ""
  test_files: []
  red_phase_verified: false
implementation_artifacts:
  files_created:
    - "infra/containers/candelamoon-docs/Containerfile"
    - "infra/containers/candelamoon-docs/requirements.txt"
    - "infra/containers/candelamoon-docs/requirements.lock"
    - "infra/containers/candelamoon-docs/package.json"
    - "infra/containers/candelamoon-docs/package-lock.json"
    - "infra/containers/candelamoon-docs/validate-design"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/vivaldi-devops-architect-activity-report.md"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/vivaldi-devops-architect-activity-report.json"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/bach-senior-developer-activity-report.md"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/bach-senior-developer-activity-report.json"
  files_modified:
    - "infra/containers/candelamoon-docs/Containerfile"
    - "infra/containers/candelamoon-docs/requirements.txt"
    - "infra/containers/candelamoon-docs/validate-design"
    - "docs/infrastructure/toolchain-pins.md"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/handoff.md"
  green_phase_verified: true
review_phase_1:
  blind_hunter_findings:
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/findings-phase-1-berlioz.md"
  edge_case_hunter_findings:
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/findings-phase-1-bartok.md"
  acceptance_analyst_findings:
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/findings-phase-1-verdi.md"
  triaged_findings:
    - id: "patch-1"
      title: "Lock pip transitive dependencies with hashes (B-06, BAR-003, BAR-004)"
      finding_ids: ["B-06", "BAR-003", "BAR-004"]
      disposition: "applied"
      detail: "Generated infra/containers/candelamoon-docs/requirements.lock with `uv pip compile --generate-hashes --python-version 3.11 --python-platform x86_64-unknown-linux-gnu requirements.txt` (9 packages = 3 direct + 6 transitive, every artifact carrying --hash=sha256:...). The Containerfile now installs with `pip install --no-cache-dir --require-hashes --no-deps -r /tmp/requirements.lock` — a changed/yanked/mirror-served wheel fails the build and no live PyPI resolution happens at build time. packaging==26.3 is NOT in the lock: it is pre-installed in the python:3.11-slim base itself (verified via `podman run` base pip freeze), so `pip freeze` still reports 10 entries. Locked transitive versions recorded in toolchain-pins.md § Python. Verified: build step 9 installed exactly attrs 26.1.0, jsonschema 4.23.0, jsonschema-specifications 2025.9.1, pathspec 1.1.1, PyYAML 6.0.2, referencing 0.37.0, rpds-py 2026.6.3, typing-extensions 4.16.0, yamllint 1.37.1."
    - id: "patch-2"
      title: "Lock npm transitive dependencies (B-07, BAR-005)"
      finding_ids: ["B-07", "BAR-005"]
      disposition: "applied"
      detail: "Created infra/containers/candelamoon-docs/package.json (markdownlint-cli 0.45.0, markdown-link-check 3.13.7 exact pins) and package-lock.json (lockfileVersion 3, 165 packages with integrity hashes, generated with `npm install --package-lock-only` on npm 11.13.0). The Containerfile COPYs both files and runs `npm ci --ignore-scripts` (exact locked tree, integrity-verified, no lifecycle scripts as root), then wires the global layout npm install -g would produce: packages under /opt/node/lib/node_modules + bin symlinks in /opt/node/bin (markdownlint -> markdownlint-cli/markdownlint.js; markdown-link-check -> markdown-link-check/markdown-link-check). `npm cache clean --force` and the _logs/_cacache removal still run after. Note: `npm ls -g --depth=0` now lists the full 165-package tree (the lock-driven install carries no global-install bookkeeping); the four expected top-level names (corepack@0.34.6, markdown-link-check@3.13.7, markdownlint-cli@0.45.0, npm@10.9.8) are all present and the CLIs work."
    - id: "patch-3"
      title: "Scope PIP_NO_CACHE_DIR to build only (B-11, BAR-013)"
      finding_ids: ["B-11", "BAR-013"]
      disposition: "applied"
      detail: "Removed PIP_NO_CACHE_DIR=1 from the ENV block (it persisted into the runtime image and disabled the pip-cache volume contract). The build-only pip install now passes --no-cache-dir explicitly. Verified at runtime: `printenv PIP_NO_CACHE_DIR` is unset (exit 1) in candelamoon-docs:review, so runtime pip operations read/write /home/builder/.cache/pip as the cache-mount convention expects."
    - id: "patch-4"
      title: "Create /workspace before timestamp normalization (B-12, BAR-010)"
      finding_ids: ["B-12", "BAR-010"]
      disposition: "applied"
      detail: "Moved the `mkdir -p /workspace && chown builder:builder /workspace` RUN to BEFORE the mtime-normalization pass, and added /workspace to the `find ... -exec touch` roots. Verified: /workspace mtime = 2025-01-01 00:00:00 UTC (SOURCE_DATE_EPOCH) and owner builder:builder in the built image; two --no-cache builds produce identical file lists including /workspace."
    - id: "patch-5"
      title: "Tighten validate-design version checks to exact pins (B-14, BAR-007)"
      finding_ids: ["B-14", "BAR-007"]
      disposition: "applied"
      detail: "Replaced the loose unanchored `[0-9]+\\.[0-9]+` patterns with anchored exact pins: jsonschema ^4\\.23\\.0$, pyyaml ^6\\.0\\.2$, yamllint ^yamllint 1\\.37\\.1$, markdownlint ^0\\.45\\.0$, markdown-link-check ^3\\.13\\.7$, npm ^10\\.9\\.8$ (exact because npm ships inside the pinned Node 22.23.2 tarball), python3 ^Python 3\\.11\\. (any patch allowed per toolchain-pins.md — the patch is fixed by the base digest), node ^v22\\. (any patch allowed per toolchain-pins.md — fixed by the SHA-256-pinned tarball)."
    - id: "patch-6"
      title: "Real Python import checks in validate-design (B-15, BAR-006)"
      finding_ids: ["B-15", "BAR-006"]
      disposition: "applied"
      detail: "jsonschema and pyyaml checks now import the REAL modules and print __version__: `python3 -c \"import jsonschema; print(jsonschema.__version__)\"` and `python3 -c \"import yaml; print(yaml.__version__)\"`, each verified against its pinned value by the anchored pattern. A stale/corrupted .dist-info can no longer pass — the import itself must succeed. The triaged patch suggested one combined command importing both modules; I split it into two checks so a failure names the failing package precisely (one command per check keeps the check() helper's single-pattern contract). Note: jsonschema prints a DeprecationWarning on stderr when __version__ is accessed (jsonschema 4.x deprecation); it does not affect the anchored match and is visible only in --verbose first-line output."
    - id: "patch-7"
      title: "Reject unknown arguments in validate-design (B-16, BAR-008)"
      finding_ids: ["B-16", "BAR-008"]
      disposition: "applied"
      detail: "Argument parsing now rejects anything other than exactly zero args or one --verbose: `$# -gt 1` and unknown single args print usage to stderr and exit 2. Verified: `validate-design --verbsoe` -> exit 2 with usage; `validate-design --verbose extra` -> exit 2 with usage."
    - id: "patch-8"
      title: "Change default CMD to validate-design (B-17)"
      finding_ids: ["B-17"]
      disposition: "applied"
      detail: "CMD changed from [\"bash\"] to [\"validate-design\"] so `podman run --rm --network=none <image>` validates by default instead of false-greening in a shell. Containerfile comment documents `--entrypoint bash` for interactive inspection. Verified: bare `podman run --rm --network=none candelamoon-docs:review` exits 0 with 'OK: all design validator tools present and runnable'."
    - id: "patch-9"
      title: "Fix sudoers guard grep error handling (BAR-009)"
      finding_ids: ["BAR-009"]
      disposition: "applied"
      detail: "Rewrote the sudoers check as an explicit per-path loop: `for f in /etc/sudoers /etc/sudoers.d/*; do [ -f \"$f\" ] || continue; if grep -q '^builder\\b\\|^%builder\\b' \"$f\"; then ERROR; exit 1; fi; done`. grep status 2 (missing/unreadable path) can no longer be negated into success. The loop is a single backslash-continued shell line because the RUN body is one logical line (build failed with 'syntax error expecting done' on the multi-line form — first build attempt, fixed). Verified: build step 14 passes on the base (no /etc/sudoers file, /etc/sudoers.d/* glob literal -> both skipped), and a direct in-image run of the loop reports no builder entries."
    - id: "patch-10"
      title: "Add timeout to validator checks (BAR-015)"
      finding_ids: ["BAR-015"]
      disposition: "applied"
      detail: "check() now invokes every probe through `timeout 30`; exit 124 is reported distinctly ('timed out after 30s') from ordinary command failure (which reports 'exit <rc>; output did not match ...'). coreutils timeout ships in the slim base. Verified: `timeout 1 sleep 5` in-image returns 124."
    - id: "patch-11"
      title: "Document build-time network domains (B-03, B-04, A-02)"
      finding_ids: ["B-03", "B-04", "A-02"]
      disposition: "applied"
      detail: "Containerfile header now carries a consolidated build-time network allowlist comment listing all five domains: pypi.org / files.pythonhosted.org (pip), registry.npmjs.org (npm), nodejs.org (Node.js tarball), deb.debian.org (apt). Each install section keeps its inline endpoint comment. Handoff AC5 updated to match. Documentation-only fix (the build already worked); ci-architecture.md § candelamoon-docs 'Build-time network: PyPI, npm registry' still lists only two hosts — updating the normative spec doc is flagged as a follow-up recommendation in the Agent Output / Known Issues."
    - id: "defer-1"
      title: "Deferred: full APT snapshotting (B-05, BAR-002)"
      finding_ids: ["B-05", "BAR-002"]
      disposition: "deferred"
      detail: "Same as P1-001 defer-2. apt packages are versioned implicitly by the base-image digest; full snapshot-pinning (dated snapshot + exact package versions/hashes) is deferred to P1-005. The Containerfile comment already documents this (mirrors P1-001 BER-002)."
    - id: "defer-2"
      title: "Deferred: markdown-link-check offline configuration (BAR-012)"
      finding_ids: ["BAR-012"]
      disposition: "deferred"
      detail: "markdown-link-check resolves HTTP(S) targets, which conflicts with --network=none for remote links. The MVP never invokes it on real content, so the incompatibility is not exercised; real validation logic (P1-017) will need an offline mode / URL classification / per-request timeout policy. Deferred to P1-017 when the real validation logic lands."
    - id: "defer-3"
      title: "Deferred: real design validation logic (B-01, B-02, A-01)"
      finding_ids: ["B-01", "B-02", "A-01"]
      disposition: "deferred"
      detail: "The schema/ADR/capability-matrix/evidence-manifest validation the spec describes is intentionally out of scope for the MVP per the handoff ('MVP: asserts all tools are present and runnable; real validation logic against docs/ content is P1-017 follow-up'). The MVP is the pre-condition for P1-017. The handoff already records this as a known debt."
    - id: "dismiss-1"
      title: "Dismissed: x64-only Node payload (B-08, BAR-001)"
      finding_ids: ["B-08", "BAR-001"]
      disposition: "dismissed"
      detail: "Single-arch is intentional: all runners (self-hosted Linux x64, WSL2) are x86_64. NODE_SHA256_LINUX_X64 documents the platform contract; an arch-parameterized tarball selection would add complexity with no consumer."
    - id: "dismiss-2"
      title: "Dismissed: /workspace-out mount points (B-09)"
      finding_ids: ["B-09"]
      disposition: "dismissed"
      detail: "Follows the P1-001 pattern: /workspace-out mount points are created by podman at bind-mount time; baking them into the image provides no runtime benefit and the convention does not require it."
    - id: "dismiss-3"
      title: "Dismissed: USER builder not the final directive (B-10)"
      finding_ids: ["B-10"]
      disposition: "dismissed"
      detail: "WORKDIR/CMD after USER is standard Dockerfile practice; USER remains the final USER directive. The handoff's AC4 wording ('final USER directive') matches the P1-001 precedent."
    - id: "dismiss-4"
      title: "Dismissed: APT paths not normalized (B-13)"
      finding_ids: ["B-13"]
      disposition: "dismissed"
      detail: "Same known debt as P1-001: /etc and /var metadata are not touched by the normalization pass. Acceptable for the pinned-base contract; recorded in known_debt."
    - id: "dismiss-5"
      title: "Dismissed: no negative tests (B-18)"
      finding_ids: ["B-18"]
      disposition: "dismissed"
      detail: "Bootstrap exception — no TDD required for this infra task (documented in the handoff's Instructions for Agent). Negative paths (unknown args, timeout, missing tools) are exercised manually in this review round."
    - id: "dismiss-6"
      title: "Dismissed: linkchecker removal (BAR-011)"
      finding_ids: ["BAR-011"]
      disposition: "dismissed"
      detail: "No existing consumers of the pip linkchecker CLI; the npm markdown-link-check substitution was an explicit, documented deviation in the implementation round (Deviations §1) and is recorded in requirements.txt and toolchain-pins.md."
    - id: "dismiss-7"
      title: "Dismissed: bind mount ownership (BAR-014)"
      finding_ids: ["BAR-014"]
      disposition: "dismissed"
      detail: "CONOPS concern (runner must mount volumes with matching ownership/--userns=keep-id), not an image bug. Documented in ci-architecture.md; the image bakes the correct placeholder ownership."
    - id: "dismiss-8"
      title: "Dismissed: 1-byte image size difference (A-03)"
      finding_ids: ["A-03"]
      disposition: "dismissed"
      detail: "Verdi observed 770379222 vs 770379221 bytes between two builds; content was identical (per-file manifests matched). Immaterial — both digests/sizes differ solely from Podman layer-tar gzip non-determinism, the recorded AC8 known debt."
  fixes_applied: true
review_phase_2:
  red_team_findings:
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/findings-phase-2-stravinsky.md"
  blue_team_findings:
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/findings-phase-2-brahms.md"
  triaged_findings:
    - id: "SEC-01"
      title: "Workspace files can hijack Python imports (HIGH) — applied"
      finding_ids: ["SEC-01"]
      disposition: "applied"
      detail: "validate-design now runs every Python import check with `python3 -I` (isolated mode: the current directory, PYTHONPATH, and user site-packages are NOT on sys.path) and the script cd's to / at startup, so the bind-mounted repository (/workspace, attacker-controlled content) can never satisfy or shadow the jsonschema/yaml imports. Inline comments document the -I rule and require future P1-017 validator code to use explicit /workspace paths and image-path imports. Red evidence on the pre-fix image (candelamoon-docs:review): a /workspace/jsonschema.py containing `__version__ = \"4.23.0\"` plus a print executed attacker code AND false-greened — `OK: jsonschema PWNED-JSONSCHEMA`, exit 0 (the exact SEC-01 attack scenario). Green on candelamoon-docs:phase2: same hostile files present, exit 0 with the real modules, no attacker output (both jsonschema.py and yaml.py variants tested)."
    - id: "SEC-02"
      title: "pip can execute a source distribution as root (CRITICAL) — applied"
      finding_ids: ["SEC-02"]
      disposition: "applied"
      detail: "Builder account creation (uid/gid 1000, lock, sudoers guard, home contract) moved ABOVE the pip block; requirements.lock is COPY'd with --chown=builder:builder. The pip section is now two phases: (1) USER builder runs `python3 -m pip download --no-cache-dir --require-hashes --no-deps --only-binary=:all: -r /tmp/requirements.lock -d /tmp/pip-wheelhouse` — only prebuilt wheels can satisfy --only-binary=:all:, so no sdist setup.py / PEP 517 build backend can ever execute — and asserts the wheelhouse is non-empty and contains ONLY .whl files; (2) USER root runs the fully offline install `python3 -m pip install --no-cache-dir --require-hashes --no-deps --only-binary=:all: --no-index --find-links=/tmp/pip-wheelhouse -r /tmp/requirements.lock`, then removes the wheelhouse and the lock. All network retrieval and any package parsing happen as uid 1000; root only extracts hash-verified local wheels into /usr/local. A future lock change with no linux x86_64 cp311 wheel fails the build (fail-closed). Verified: build log shows 9 wheels downloaded as builder (incl. cp311 wheels for PyYAML/rpds-py), install phase reports 'Looking in links: /tmp/pip-wheelhouse' with all 9 processed, cleanup confirmed (wheelhouse + lock absent from the final image, /tmp clean). Final USER builder directive unchanged; the 'last USER directive' comment now documents the temporary USER switches. Added --no-cache-dir to the download phase (deviation: not in Brahms' sketch) so no pip cache is baked into the image — required for AC8 determinism."
    - id: "defer-sec-03"
      title: "Deferred to CI: build-time network allowlist enforcement (HIGH)"
      finding_ids: ["SEC-03"]
      disposition: "deferred"
      detail: "Per Brahms defer-to-CI: the 5-domain allowlist stays documented in the Containerfile, but enforcement must live on the Linux build runner — default-deny build network namespace or approved HTTPS proxy permitting only deb.debian.org, nodejs.org, pypi.org, files.pythonhosted.org, registry.npmjs.org; fail the job on --network=host; strongest mode prefetches all artifacts then builds with `podman build --network=none`. Tracked for the CI job definition round."
    - id: "defer-sec-04"
      title: "Deferred to CI: npm runtime JavaScript sandboxing (HIGH)"
      finding_ids: ["SEC-04"]
      disposition: "deferred"
      detail: "Per Brahms defer-to-CI: keep `npm ci --ignore-scripts`, lockfile integrity, and root-owned /opt/node as install-time controls; every validation invocation must run hardened (`--network=none --read-only --cap-drop=ALL --security-opt=no-new-privileges --user=1000:1000`, read-only /workspace bind, tmpfs /tmp, no sockets/secrets mounts). CI should also assert the lockfile is unchanged during npm ci and that no install script is enabled."
    - id: "defer-sec-05"
      title: "Deferred to CI: runtime network isolation enforcement (HIGH)"
      finding_ids: ["SEC-05"]
      disposition: "deferred"
      detail: "Per Brahms defer-to-CI: `--network=none` is a caller convention; the merge-gate invocation becomes an exact centrally-owned podman run command (with --network=none --read-only --cap-drop=ALL --security-opt=no-new-privileges --user=1000:1000, read-only workspace bind, --tmpfs /tmp) plus a negative test proving the docs-validation job cannot reach an external endpoint. Networked link-checking, if ever needed, becomes a separately authorized job with an egress proxy."
    - id: "defer-sec-06"
      title: "Deferred: apt package version drift (MEDIUM)"
      finding_ids: ["SEC-06"]
      disposition: "deferred"
      detail: "Per Brahms defer-to-CI: apt packages remain versioned implicitly by the base-image digest; full Debian snapshot/apt-proxy pinning with `package=version` installs and dpkg manifests is the shared P1-001/P1-002 build policy (P1-005 follow-up), refreshing snapshot + base digest together."
    - id: "dismiss-sec-07"
      title: "Dismissed: default validator is tool-presence only (MEDIUM)"
      finding_ids: ["SEC-07"]
      disposition: "dismissed"
      detail: "Per Brahms dismiss: accurate as a capability statement but not a container-security defect — P1-002 is explicitly the MVP tool-presence validator and real /workspace/docs validation (schemas, ADR register, capability matrix, evidence manifest) is the documented P1-017 follow-up. P1-017 must adopt the SEC-01 isolated-import rule and explicit /workspace paths and receive its own threat model."
  fixes_applied: true
coverage_audit:
  rating: "n/a"
  risk_weighted_score: 0
  memtrace_reconciliation: "n/a — bootstrap exception per handoff § Instructions (infra/docs task, no test surface). Memtrace re-index not required for the P1-002 change because the diff is infra-only (Containerfile, requirements.txt, requirements.lock, package.json, package-lock.json, validate-design, toolchain-pins.md) and touches no application symbols that would alter the symbol/edge counts; the existing CandelaMoon index at base SHA 2118b61c remains valid for symbol discovery. A re-index is recommended before PR merge for graph consistency, but is not a blocker for UAT."
  coverage_gaps: []
uat:
  status: "passed"
  user_decision: "candelamoon-docs Containerfile green-verified on candelamoon-docs:phase2 (id 127a1439acb4..., 771,003,453 bytes, 23/23 build steps); Vivaldi's initial build, Bach's review-phase-1 patch round (11 applied + 3 deferred + 8 dismissed), and Bach's review-phase-2 security patch round (SEC-01 import isolation + SEC-02 wheel-only pip applied; SEC-03..SEC-06 deferred to CI/P1-005; SEC-07 dismissed as P1-017 scope) all pass. Full AC7 validation suite green under --network=none (Python 3.11.15, Node v22.23.2, markdownlint 0.45.0, yamllint 1.37.1, markdown-link-check 3.13.7, npm 10.9.8; uid=1000 builder; default CMD validate-design exits 0 with 8/8 OK). SEC-01 red→green proof captured: pre-fix image false-greens with a /workspace/jsonschema.py containing attacker code, fixed image exits 0 with real modules. Two-build reproducibility verified (identical pip freeze md5 a6a8985a..., identical file-list md5 dca115fa..., image size 771,003,453 bytes). All ten acceptance criteria met (AC8 partial pass — content reproducible, digest not — tracked as known debt per P1-001). Task ready for human merge approval."
documentation:
  tech_writer_artifacts:
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/session-handout.md"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/schubert-tech-writer-activity-report.md"
    - ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/schubert-tech-writer-activity-report.json"
  session_handout: ".maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/session-handout.md"
  memtrace_repo_id: "CandelaMoon"
memtrace_indexed_sha: "2118b61cd1dc49d600b36f06f7d832d5a7b8b824"
memtrace_episode_ids: []
capability_rows: []
adrs: ["0014"]
verification:
  tests_pass: true
  memtrace_review: false
  acceptance_audit: true
  edge_case_hunt: true
  blind_hunt: true
  security_review: true
  policy_check: true
known_debt:
  - "AC8: Podman layer-tar gzip is non-deterministic (carried forward from P1-001). Image content is reproducible (file counts, total bytes, pip freeze, npm modules, image size all match across two --no-cache builds). Image digest is not bit-reproducible — same root cause as P1-001 (Podman gzip non-determinism). Tracked as cross-task known debt; resolution path: pin every downloaded artifact by SHA-256 (already done for Node.js tarball, PyPI via --require-hashes, npm via lockfile integrity; apt relies on the base-image digest + HTTPS), and switch to a deterministic compression backend (e.g. zstd -19) when Podman supports it."
  - "Design validator is MVP. The script asserts that all required tools are installed and runnable; the actual validation logic (architecture schemas, ADR register, capability matrix, evidence manifest, ADR/capability-matrix validation scripts) is P1-017 follow-up. The MVP is a hard pre-condition for P1-017 because the real validator scripts will run inside this image."
  - "Review round (2026-08-09): npm audit reports 8 vulnerabilities (4 moderate, 4 high) in the locked transitive npm tree (npm ci also emits deprecation warnings for glob@11.0.3 / whatwg-encoding@3.1.1). The tree is now LOCKED in package-lock.json so it cannot drift silently, but the vulnerable versions remain until a deliberate pin bump + lock regeneration. Tracked by P1-022 (dependency vulnerability remediation)."
  - "Review round (2026-08-09): ci-architecture.md § 'candelamoon-docs' 'Build-time network' still lists only 'PyPI, npm registry'. The Containerfile header and handoff AC5 now document the full 5-domain allowlist (pypi.org, files.pythonhosted.org, registry.npmjs.org, nodejs.org, deb.debian.org); the normative spec doc should be updated in the same PR as the next pin change."
  - "SEC-03..SEC-06 deferred to CI: build-time network allowlist enforcement (5-domain), npm runtime JavaScript sandboxing, runtime --network=none enforcement, and apt package version drift. Per Brahms' defer-to-CI reasoning, the image-side controls (wheel-only pip via --only-binary=:all:, npm ci --ignore-scripts, hash-locked pip+npm trees, non-root runtime user, SEC-01 isolated Python imports, sudoers fail-closed) are in place; the CI job definition (P1-010) and the publication job (P1-005) must add the enforcement / verification layer."
  - "STR-10 (archive resource bounds) from P1-001 review remains an open follow-up across both image tasks. Brahms' recommendation was to add a guarded-download / check-zip helper with per-archive size / entry-count / expansion budgets. Not addressed in P1-002's image; the Node.js tarball is the only archive extracted during this Containerfile's build, and it is already SHA-256-pinned. The next apply-now patch round should pick this up uniformly for P1-001 and P1-002."
  - "Documentation debt (Schubert 2026-08-09): ci-architecture.md § 'candelamoon-docs' Containerfile path line carries no status note (P1-001's section was updated; P1-002's was not). Should be appended with 'implemented per P1-002; green-verified 2026-08-09; review phases 1+2 closed; SEC-01/SEC-02 applied' and a handoff pointer. Deferred to the same PR as the build-time network spec fix; not a blocker for UAT."
rollback_strategy: "Delete infra/containers/candelamoon-docs/, revert toolchain-pins.md digest update, and revert .containerignore if modified. No code or build files are affected — the Containerfile is not yet referenced by any CI workflow."
---

# Task: P1-002 — candelamoon-docs Containerfile

## Context

Phase 1 (Delivery Foundation) requires a containerized docs validation environment. ADR 0014 mandates Podman-first, rootless execution with images pinned by digest. The `candelamoon-docs` image is the second of four container image roles (after P1-001 candelamoon-android). It serves as the execution environment for the docs-validate CI job, memtrace-sync support, and evidence audit.

This task follows the P1-001 pattern (green-verified, review phases 1+2 closed). The Containerfile shares common conventions with P1-001: non-root `builder` user (uid/gid 1000), `--network=none` at run-time, digest-pinned base image, inline doc comments.

**Key references:**
- CI architecture: `docs/infrastructure/ci-architecture.md` § "candelamoon-docs" (lines 69-76) defines all image requirements
- Toolchain pins: `docs/infrastructure/toolchain-pins.md` — § `Python 3.11` (line 132-136), § `Node.js 22 LTS` (line 118-124), § `Container Base Images` (line 163-170)
- ADR 0014: `docs/adr/0014-podman-first-execution.md`
- Phase plan: `.maestro-space/maestro-plans/phase-1-delivery-system/phase-plan.md`
- P1-001 reference Containerfile: `infra/containers/candelamoon-android/Containerfile` (green-verified pattern to follow)
- P1-001 root `.containerignore`: `.containerignore` (existing, may need docs-specific additions)

## Instructions for Agent

**Production agent: Vivaldi (DevOps Architect)** — subagent_type: `vivaldi-devops-architect`

Read the handoff file first. It contains your task, acceptance criteria, and context.

**Working directory:** `D:\Repos\CandelaMoon`

**Spec:** `docs/infrastructure/ci-architecture.md` § "candelamoon-docs" (lines 69-76) + § "Common conventions" (lines 53-58)
**Plan:** `.maestro-space/maestro-plans/phase-1-delivery-system/phase-plan.md`, Task P1-002
**Relevant ADRs:** 0014 (Podman-First Execution)
**Reference docs:**
- `docs/infrastructure/ci-architecture.md` — "candelamoon-docs" section (lines 69-76) + "Common conventions" (lines 53-58) define all image requirements
- `docs/infrastructure/toolchain-pins.md` — normative tool versions (Python 3.11, Node.js 22 LTS, pip deps, base image digest)
- `infra/containers/candelamoon-android/Containerfile` — P1-001 reference: follow its structure, non-root user hardening, mtime normalization, inline doc comments, `.containerignore` patterns
- `.containerignore` — existing root file from P1-001; review and append docs-specific exclusions if needed

Your agent identity and full operating rules are defined in your agent file at `.maestro-space/maestro-agents/vivaldi-devops-architect.md`. Read it to understand your role, contract, and deliverables.

**Activity report template:** `.maestro-space/maestro-templates/agent-activity-report.md`

**Bootstrap exception (docs/infra task):** Skip TDD red phase and coverage audit (steps 2 and 10 of the 14-step cycle). Still produce the Containerfile and verify via `podman build` + toolchain validation commands.

**Implementation notes:**
- The `python:3.11-slim` base does NOT ship a pre-existing uid-1000 user — plan for `groupadd -g 1000 builder && useradd -u 1000 -g builder -m builder` (simpler than P1-001's rename logic)
- pip deps should be installed from a `requirements.txt` embedded in the Containerfile or in an adjacent `infra/containers/candelamoon-docs/requirements.txt`
- Node.js 22 LTS: install from the official NodeSource tarball or nodesource setup script; pin the major version
- `markdownlint-cli` is the npm package; install globally via `npm install -g markdownlint-cli`
- Link checker: use `markdown-link-check` (npm) or `linkchecker` (pip) — Vivaldi decides based on what runs best offline in the slim image
- Design validator entrypoint: a shell script at `/usr/local/bin/validate-design` that wraps the validation commands; for MVP, the validator just asserts that the schema files, pip tools, and node tools are present and runnable (the actual validation logic against `docs/` content is a follow-up in P1-017)
- Follow the P1-001 security patterns: `DEBIAN_FRONTEND=noninteractive`, `--no-install-recommends`, fail-closed on every step, mtime normalization to `$SOURCE_DATE_EPOCH`
- Use the same `builder` uid/gid as P1-001 (1000:1000) for cache volume compatibility

**After completing your work:**
1. Update the handoff file's `implementation_artifacts` section with created/modified files
2. Set `green_phase_verified: true` upon successful `podman build` + validation
3. Update `head_sha` with the current commit SHA
4. Write the Agent Output section below with your actions and verification
5. Write a parallel activity report (JSON + MD) in the task folder

## Agent Output

### Vivaldi (DevOps Architect) — Implementation (2026-08-09)

#### Actions

1. **Read** the handoff, `docs/infrastructure/ci-architecture.md`, `docs/infrastructure/toolchain-pins.md`, `docs/adr/0014-podman-first-execution.md`, `infra/containers/candelamoon-android/Containerfile` (P1-001 reference), and `.containerignore` to lock the spec.
2. **Resolved** the `python:3.11-slim` base image digest: `podman pull docker.io/library/python:3.11-slim` → `podman image inspect --format '{{index .RepoDigests 0}}'` → `docker.io/library/python@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` (image ID `245f9d32fabaec22e749aa5cfef79996088135e9d4410f4e7ebe133c2be98132`, created 2026-08-05 01:12:29 UTC, in-image `python3 --version` reports `Python 3.11.15`, `cat /etc/os-release` reports `Debian GNU/Linux 13 (trixie)` / `DEBIAN_VERSION_FULL 13.6`).
3. **Verified** the base ships no pre-existing uid-1000 user (`getent passwd 1000` returns nothing; `getent passwd builder` returns nothing) — confirmed the simpler `groupadd + useradd` path per the handoff's implementation note.
4. **Pinned** Node.js to `22.23.2` (latest 22.x LTS security release, 2026-07-28, line "Jod"). Resolved the SHA-256 of `node-v22.23.2-linux-x64.tar.xz` from `https://nodejs.org/dist/v22.23.2/SHASUMS256.txt` → `d60acfe00a2932254bb0ad20e01b0d74397a0875595de719654b214f4b03f307`.
5. **Wrote** `infra/containers/candelamoon-docs/Containerfile` (~290 lines, 19 steps: 1 FROM, 4 ENV, 10 RUN, 1 COPY ×2, 1 USER, 1 WORKDIR, 1 CMD). Inline comments cite `ci-architecture.md § candelamoon-docs` / `Common conventions`, `toolchain-pins.md § Python 3.11` / `Node.js 22 LTS` / `Container Base Images`, and ADR 0014 at every step (AC10).
6. **Wrote** `infra/containers/candelamoon-docs/requirements.txt` with the three pip pins (`jsonschema==4.23.0`, `pyyaml==6.0.2`, `yamllint==1.37.1`); the file's header documents the link-checker choice and the reason `linkchecker` was rejected.
7. **Wrote** `infra/containers/candelamoon-docs/validate-design` — the MVP design-validator entrypoint that asserts every required tool is installed and runnable. Uses `importlib.metadata` (deprecation-free) for Python versions and unanchored regex matching so a leading product name (e.g. `yamllint 1.37.1`) does not break the check. Supports `--verbose` for log-friendly CI output.
8. **Built** the image: `podman build --no-cache -t candelamoon-docs:test -f infra/containers/candelamoon-docs/Containerfile .` → succeeded.
9. **Iterated** to fix two issues found during green-phase verification:
   - **Issue A** (validate-design): `yamllint --version` outputs `yamllint 1.37.1` (with a leading product name); the original anchored regex `^[0-9]+\.` did not match. Switched to unanchored `[0-9]+\.[0-9]+` patterns so all CLIs work uniformly. Also replaced `jsonschema.__version__` (deprecated) with `importlib.metadata.version('jsonschema')` to drop the deprecation warning.
   - **Issue B** (AC8 reproducibility): the first two `--no-cache` builds produced identical file counts and nearly-identical total bytes, but `/home/builder/.npm/_logs/` contained timestamped npm debug-log files whose CONTENT varied between builds (different timestamps, durations, paths) — defeating AC8 even though mtimes were normalized. Fixed by adding `rm -rf /home/builder/.npm/_logs /home/builder/.npm/_cacache` to the npm install RUN, with a comment explaining why.
10. **Re-built** the image after the two fixes; build succeeded.
11. **Verified** AC7 (per the `podman run --rm --network=none candelamoon-docs:test ...` commands in the verification table below).
12. **Verified** AC8 reproducibility: two `--no-cache --source-date-epoch=1735689600 --rewrite-timestamp` builds produce identical file counts, total bytes, pip freeze (10 entries), and npm modules (4 global packages). The image size matches exactly: 770,379,387 bytes both times. Image digests differ (sha256:a1090f0f... vs sha256:38a604f5...) due to Podman layer-tar gzip non-determinism — carried forward from P1-001 AC8 as known debt.
13. **Verified** AC6 (`--network=none`): DNS resolution fails (`curl: (6) Could not resolve host: pypi.org`), TCP connections fail (`bash: connect: Network is unreachable`).
14. **Verified** AC9: the existing root `.containerignore` (from P1-001) is adequate for the docs build context. The Containerfile only COPYs two small files (`infra/containers/candelamoon-docs/requirements.txt` and `infra/containers/candelamoon-docs/validate-design`); the `.git/` (639 files), `.maestro-space/` (110 files), and `docs/handoffs/` (4 files) directories are all correctly excluded by the existing patterns. No additional exclusions were needed.
15. **Updated** `docs/infrastructure/toolchain-pins.md`: filled in the resolved python:3.11-slim digest in `Container Base Images` and `Python`; resolved Node.js 22.23.2 SHA-256 in `Node`; added a `candelamoon-docs pip pins` and `candelamoon-docs npm pins` subsection to the `Python` and `Node` sections respectively.
16. **Wrote** the parallel activity report (`vivaldi-devops-architect-activity-report.md` and `.json`).
17. **Updated** the handoff: `implementation_artifacts`, `green_phase_verified: true`, `head_sha`, `known_debt` additions, and the Agent Output section.

#### Verification table (AC7)

| Command | Expected | Observed |
|---|---|---|
| `podman pull docker.io/library/python:3.11-slim` then `podman image inspect --format '{{index .RepoDigests 0}}' ...` | digest `sha256:...` | `docker.io/library/python@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` |
| `podman build --no-cache -t candelamoon-docs:test -f infra/containers/candelamoon-docs/Containerfile .` | `Successfully tagged localhost/candelamoon-docs:test` | `Successfully tagged localhost/candelamoon-docs:test` (id `b0a340483c8a3a14ff3823355713081969bd171b6b43391bd3f3c9a28d0fc2ca`, 770,379,221 bytes) |
| `podman run --rm --network=none candelamoon-docs:test python3 --version` | Python 3.11.x | `Python 3.11.15` |
| `podman run --rm --network=none candelamoon-docs:test node --version` | v22.x | `v22.23.2` |
| `podman run --rm --network=none candelamoon-docs:test markdownlint --version` | valid version | `0.45.0` |
| `podman run --rm --network=none candelamoon-docs:test yamllint --version` | valid version | `yamllint 1.37.1` |
| `podman run --rm --network=none candelamoon-docs:test markdown-link-check --version` | valid version | `3.13.7` |
| `podman run --rm --network=none candelamoon-docs:test id` | uid=1000(builder) | `uid=1000(builder) gid=1000(builder) groups=1000(builder)` |
| `podman run --rm --network=none candelamoon-docs:test /usr/local/bin/validate-design` | exit 0, all tools OK | exit 0; `OK: all design validator tools present and runnable` |
| `podman run --rm --network=none candelamoon-docs:test pip freeze` | jsonschema, pyyaml, yamllint, transitives | 10 entries: `attrs==26.1.0`, `jsonschema==4.23.0`, `jsonschema-specifications==2025.9.1`, `packaging==26.3`, `pathspec==1.1.1`, `PyYAML==6.0.2`, `referencing==0.37.0`, `rpds-py==2026.6.3`, `typing_extensions==4.16.0`, `yamllint==1.37.1` |
| `podman run --rm --network=none candelamoon-docs:test npm ls -g --depth=0` | markdownlint-cli, markdown-link-check | `corepack@0.34.6`, `markdown-link-check@3.13.7`, `markdownlint-cli@0.45.0`, `npm@10.9.8` |
| `podman run --rm --network=none candelamoon-docs:test curl https://pypi.org/` | network unreachable | `curl: (6) Could not resolve host: pypi.org` (exit 6) |
| AC8: two `--no-cache --source-date-epoch=1735689600 --rewrite-timestamp` builds | identical file counts and total bytes | `/opt/node 9532/232233887` (both), `/usr/local 2440/45961513` (both), `/home/builder 0/0` (both), `pip freeze` identical (both), image size 770,379,387 bytes (both); image digest differs: `sha256:a1090f0f...` vs `sha256:38a604f5...` (Podman gzip non-determinism, known debt) |

#### Deviations

1. **Link checker delivered as `markdown-link-check` (npm) rather than `linkchecker` (pip).** The handoff gave Vivaldi the choice. Rationale: (a) `markdown-link-check` is purpose-built for Markdown link validation and pairs naturally with `markdownlint-cli` on the same npm toolchain; (b) the pip alternative `linkchecker` carries many additional Python deps (BeautifulSoup, requests, ...) that bloat the slim base image; (c) using a single toolchain (npm) for both markdown lint and link check keeps the image simpler. Recorded in `requirements.txt` and `toolchain-pins.md § Node` "candelamoon-docs npm pins". AC3 wording was updated to reflect this.
2. **Base image does not need the P1-001 rename-the-base-user logic.** `python:3.11-slim` ships no pre-existing uid-1000 user (verified). Used the simpler `groupadd --gid 1000 --system builder && useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash --no-log-init builder` path with `usermod --lock` + `usermod -G builder builder` for the same postcondition set as P1-001 (uid/gid/supplementary-groups/sudoers-free/home-owner).
3. **Build-time network expanded to include `nodejs.org`.** AC5 in the handoff said "pypi.org, files.pythonhosted.org (pip), registry.npmjs.org (npm)" — but the Node.js binary distribution lives on `nodejs.org`, not the npm registry. The Containerfile comment at the Node.js install step documents this; the new effective build-time allowlist is `{pypi.org, files.pythonhosted.org, registry.npmjs.org, nodejs.org}`. The AC5 line in the handoff was updated to reflect this.
4. **Validator script is MVP; real validation logic deferred to P1-017.** The handoff said "MVP: assert tools are present and runnable" and the actual schema/ADR/capability-matrix/evidence-manifest validation is a follow-up. The shipped `validate-design` does exactly that MVP and includes a `--verbose` mode for log-friendly CI output.

#### Known issues

1. **AC8 image digest is not bit-reproducible** — same root cause as P1-001: Podman layer-tar gzip is non-deterministic. Image content IS reproducible (file counts, total bytes, image size 770,379,387 bytes all match exactly across two `--no-cache` builds). Resolution path: pin every downloaded artifact by SHA-256 (Node.js tarball already done; apt and PyPI rely on the base-image digest + HTTPS); switch to a deterministic compression backend (e.g. zstd -19) when Podman supports it. Out of scope for P1-002.
2. **Design validator is MVP** — see Deviations §4. P1-017 will add the real schema/ADR/capability-matrix/evidence-manifest validation scripts that the docs-validate job will invoke. The MVP is the pre-condition: the scripts will run inside this image and assume every tool the MVP checks is present.
3. **No SHA-256 verification on apt or PyPI downloads** — apt packages are versioned implicitly by the base image digest (the python:3.11-slim base pins its own apt sources and package revisions). PyPI wheels are downloaded over HTTPS and pinned by exact version in `requirements.txt`, but not cryptographically verified at build time. Recording SHA-256s in `toolchain-pins.md` and adding `pip install --require-hashes` against a `requirements.txt` that includes `--hash=sha256:...` per line is a small follow-up (mirrors P1-001's known debt for cmdline-tools / Gradle / Robolectric).
4. **Base image digest resolution timestamp not recorded alongside Temurin 17** — toolchain-pins.md records the `2026-08-04 01:27:24 UTC` creation date for the Temurin 17 base (P1-001); the python:3.11-slim digest was resolved on 2026-08-09 with the in-image `python3 --version` (3.11.15) and the OS (`Debian 13 trixie / DEBIAN_VERSION_FULL 13.6`) recorded. If a future pin bump lands, both pieces of evidence should be re-captured in the same PR.

#### Handoff to

Bernstein for Review Phase 1 dispatch (Berlioz/Bartók/Verdi). Pass `infra/containers/candelamoon-docs/Containerfile`, `infra/containers/candelamoon-docs/requirements.txt`, and `infra/containers/candelamoon-docs/validate-design` to the review agents; point them at the AC2-AC9 evidence in the verification table above and the AC8 partial-pass caveat in Known Issues §1. The P1-002 follow-up tasks (P1-017 design-validator logic; P1-022 dependency vulnerability remediation) should be visible in the phase plan and can be tracked in the same review cycle.

### Bach (Senior Developer) — Review Phase 1 patch round (2026-08-09)

#### Environment

- Host: Windows 11 (WSL2 backend; podman-machine-default, 8 vCPU / 8 GiB RAM / 100 GiB disk). Podman 5.8.3 rootless.
- Base image `docker.io/library/python:3.11-slim@sha256:78b39ef14d...` cached locally (`--pull=never`).
- Lock generation tooling: `uv 0.11.13` (`uv pip compile --generate-hashes`), host npm 11.13.0 (`npm install --package-lock-only` → lockfileVersion 3, readable by in-image npm 10.9.8).
- Prior image for reference: `localhost/candelamoon-docs:test` (id `b0a340483c8a...`, pre-review).
- Built image: `localhost/candelamoon-docs:review` (id `d3c7f79d9df29fe780b197f09c2a817739c5f71a678edd0fcf1d33c3578d6b96`, 769,460,929 bytes).
- Build/verification logs: `%TEMP%/opencode/p1-002-review/build-review.log`, `build-review2.log`, `build-review-repro.log`.

#### Actions

1. **Read** the handoff, my agent identity file, the activity-report template + `agent-output.schema.json`, all three findings reports (`findings-phase-1-berlioz.md` B-01..B-18, `findings-phase-1-bartok.md` BAR-001..BAR-015, `findings-phase-1-verdi.md` A-01..A-03), the P1-001 handoff (triaged_findings format precedent), and `ci-architecture.md` § candelamoon-docs / Common conventions.
2. **PATCH 1** — generated `infra/containers/candelamoon-docs/requirements.lock` (9 packages, every artifact `--hash=sha256:...`) with `uv pip compile --generate-hashes --python-version 3.11 --python-platform x86_64-unknown-linux-gnu requirements.txt`; verified the resolved set matches the recorded in-image pip freeze (10 entries incl. base-shipped `packaging==26.3`, confirmed present in the base image itself via `podman run` pip freeze). Updated the Containerfile pip step to `pip install --no-cache-dir --require-hashes --no-deps -r /tmp/requirements.lock`, updated `requirements.txt` header and `toolchain-pins.md` § Python.
3. **PATCH 2** — created `package.json` (markdownlint-cli 0.45.0, markdown-link-check 3.13.7 exact) and generated `package-lock.json` (lockfileVersion 3, 165 packages, integrity hashes) via `npm install --package-lock-only`. Rewrote the npm step: COPY both files → `npm ci --ignore-scripts` in a staging dir → copy the locked tree into `/opt/node/lib/node_modules` → wire `/opt/node/bin` symlinks (markdownlint, markdown-link-check) → `npm cache clean --force` + `_logs/_cacache` removal (still runs). Verified the two bin names from registry metadata (`npm view ... bin`).
4. **PATCH 3** — removed `PIP_NO_CACHE_DIR=1` from the ENV block; the pip RUN now carries `--no-cache-dir` alone. Updated the ENV-block and pip-section comments. Verified at runtime: `printenv PIP_NO_CACHE_DIR` unset.
5. **PATCH 4** — moved the `mkdir -p /workspace && chown builder:builder /workspace` RUN before the mtime-normalization pass and added `/workspace` to the `find ... -exec touch` roots. Verified: /workspace mtime 2025-01-01 00:00:00 UTC, owner builder:builder.
6. **PATCH 5 + 6 + 7 + 10** — rewrote `validate-design`: anchored exact-version patterns (jsonschema `^4\.23\.0$`, pyyaml `^6\.0\.2$`, yamllint `^yamllint 1\.37\.1$`, markdownlint `^0\.45\.0$`, markdown-link-check `^3\.13\.7$`, npm `^10\.9\.8$`; python `^Python 3\.11\.`, node `^v22\.`), real module imports for jsonschema/yaml with per-package checks (split from the triaged single-command form so failures name the failing package), strict argument validation (unknown/extra args → usage on stderr, exit 2), and `timeout 30` around every probe with a distinct exit-124 report.
7. **PATCH 8** — CMD `["bash"]` → `["validate-design"]` with an inline `--entrypoint bash` note for interactive use.
8. **PATCH 9** — rewrote the sudoers guard as the explicit per-path loop. First build failed with `/bin/sh: syntax error expecting "done"` because the multi-line loop cannot live inside a backslash-continued RUN body; collapsed to a single shell line (noted in the triaged finding). Second build green.
9. **PATCH 11** — added the consolidated 5-domain build-time network allowlist comment block to the Containerfile header and updated handoff AC5.
10. **Built** `podman build --pull=never -t candelamoon-docs:review -f infra/containers/candelamoon-docs/Containerfile .` → 20/20 steps, `Successfully tagged localhost/candelamoon-docs:review`.
11. **Verified** the full AC7 suite under `--network=none` plus negative paths (unknown arg → exit 2, extra args → exit 2, timeout(1) exit 124 in-image, sudoers loop no-false-positive) and runtime env (PIP_NO_CACHE_DIR unset).
12. **Reproducibility** — second `--no-cache` build (`candelamoon-docs:review2`): identical file lists (`find /opt/node /usr/local /home/builder /workspace` Compare-Object → IDENTICAL), identical counts/bytes per tree, identical pip freeze (md5 `a6a8985a...`), identical image size 769,460,929 bytes; digests differ (Podman gzip non-determinism, known debt). Removed `review2` after comparison.
13. **Committed** the code changes (`ff6c64d0`), then updated this handoff (`head_sha`, AC5, `implementation_artifacts`, `review_phase_1.triaged_findings` 11 patches + 3 deferred + 8 dismissed, `fixes_applied: true`, `known_debt`, this section) and wrote the activity report (JSON + MD).

#### Files

- Modified: `infra/containers/candelamoon-docs/Containerfile` — patches 1-4, 8, 9, 11 (lock-driven pip/npm installs, PIP_NO_CACHE_DIR scoping, /workspace reorder, sudoers loop, CMD, network allowlist comment)
- Modified: `infra/containers/candelamoon-docs/validate-design` — patches 5, 6, 7, 10 (exact pins, real imports, arg validation, timeout)
- Modified: `infra/containers/candelamoon-docs/requirements.txt` — lock documentation
- Modified: `docs/infrastructure/toolchain-pins.md` — § Python / § Node lock-file records
- Created: `infra/containers/candelamoon-docs/requirements.lock` (hash-locked pip tree)
- Created: `infra/containers/candelamoon-docs/package.json` + `package-lock.json` (npm locked tree)
- Modified: `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/handoff.md`
- Created: `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/bach-senior-developer-activity-report.md` / `.json`
- Read (context): all three findings reports, P1-001 handoff (triaged format), Vivaldi's reports, `agent-output.schema.json`, `ci-architecture.md`

#### Verification

| Command | Expected | Observed |
|---|---|---|
| `podman build --pull=never -t candelamoon-docs:review -f infra/containers/candelamoon-docs/Containerfile .` | build succeeds | 20/20 steps, `Successfully tagged localhost/candelamoon-docs:review` (id `d3c7f79d9df2...`, 769,460,929 bytes) |
| `pip install --dry-run --require-hashes --no-deps -r requirements.lock` (host) | lock parses, hashes accepted | `Would install PyYAML-6.0.2 jsonschema-4.23.0 pathspec-1.1.1 rpds-py-2026.6.3 typing_extensions-4.16.0 yamllint-1.37.1` |
| `podman run --rm --network=none candelamoon-docs:review python3 --version` | Python 3.11.x | `Python 3.11.15` |
| `... node --version` | v22.x | `v22.23.2` |
| `... npm --version` | 10.9.8 | `10.9.8` |
| `... markdownlint --version` | 0.45.0 | `0.45.0` |
| `... yamllint --version` | yamllint 1.37.1 | `yamllint 1.37.1` |
| `... markdown-link-check --version` | 3.13.7 | `3.13.7` |
| `... id` | uid=1000(builder) | `uid=1000(builder) gid=1000(builder) groups=1000(builder)` |
| `...` (no command — default CMD) | validate-design exit 0 | `OK: all design validator tools present and runnable` (8/8 OK) |
| `... validate-design --verbose` | per-tool OK lines | 8 OK lines with versions; jsonschema first line shows the 4.x DeprecationWarning (cosmetic; anchored match unaffected) |
| `... validate-design --verbsoe` | exit 2, usage | `ERROR: unknown argument: --verbsoe` + usage, exit 2 |
| `... validate-design --verbose extra` | exit 2, usage | `ERROR: too many arguments: --verbose extra` + usage, exit 2 |
| `... bash -c 'printenv PIP_NO_CACHE_DIR'` | unset | unset (rc 1) — runtime pip cache volume usable |
| `... bash -c 'curl -sS --max-time 5 https://pypi.org/'` | unreachable | `curl: (6) Could not resolve host: pypi.org` (exit 6) |
| `... pip freeze` | 10 entries | identical set incl. `packaging==26.3` (base-shipped) |
| `... npm ls -g --depth=0` | markdownlint-cli, markdown-link-check present | full locked tree (165 pkgs) listed; `corepack@0.34.6`, `markdown-link-check@3.13.7`, `markdownlint-cli@0.45.0`, `npm@10.9.8` all present |
| `... stat -c '%U:%G %y' /workspace` | builder, SOURCE_DATE_EPOCH | `builder:builder 2025-01-01 00:00:00.000000000 +0000` |
| `... bash -c 'timeout 1 sleep 5; echo rc=$?'` | timeout works (coreutils) | `timeout-rc=124` |
| sudoers loop (in-image, direct) | no false positive | `no sudoers entries for builder (good)` |
| AC8: two `--no-cache` builds | identical content | identical `find` file lists, counts/bytes per tree (`/opt/node 11169/231786503`, `/usr/local 2867/45963238`, `/home/builder 4/0`, `/workspace 1/0` both), identical pip freeze md5 `a6a8985a...`, image size 769,460,929 bytes both; digests differ (`d3c7f79d9df2` vs `602cf10611ec` — Podman gzip non-determinism, known debt) |

Full logs: `%TEMP%/opencode/p1-002-review/build-review.log`, `build-review2.log`, `build-review-repro.log`

#### Deviations

1. **validate-design checks split** — the triaged PATCH 6 suggested one combined `python3 -c "import jsonschema; ...; import yaml; ..."` command; implemented as two separate checks (one command per check) so a failure names the failing package precisely and the `check()` helper keeps its single-pattern contract. Both do real imports and assert the exact pinned versions — the B-15/BAR-006 intent is fully met.
2. **sudoers loop single-line form** — the triaged multi-line `for ... do ... done` block cannot span lines inside a backslash-continued RUN body (`/bin/sh: syntax error expecting "done"` on the first build); collapsed to one shell line with identical semantics, plus an inline comment.
3. **npm install mechanism** — `npm install -g` cannot honor a lockfile, so PATCH 2's 'npm ci then global install from the locked tree' is implemented as `npm ci --ignore-scripts` + copying the locked tree into the global layout + explicit bin symlinks. Result is equivalent to `npm install -g` with full lockfile determinism; side effect: `npm ls -g --depth=0` now displays the whole locked tree (165 packages) rather than only 4 top-level entries (npm's global-install bookkeeping is not written). All expected top-level names are present and the CLIs work.
4. **npm pinned exactly** (`^10\.9\.8$`) — not listed in the triaged patch, but npm ships inside the SHA-256-pinned Node 22.23.2 tarball, so exact-pinning it is deterministic and consistent with the 'exact pins' intent of PATCH 5.

#### Known issues

1. **npm audit: 8 vulnerabilities (4 moderate, 4 high) in the locked transitive npm tree** — e.g. `glob@11.0.3` (npm ci emits its deprecation warning). The tree is locked and cannot drift, but remediation (pin bumps + lock regeneration) is P1-022's scope. Not a blocker for this review round.
2. **ci-architecture.md § candelamoon-docs 'Build-time network' still lists only 'PyPI, npm registry'** — the Containerfile header and handoff AC5 now document the full 5-domain allowlist; the normative spec doc should be updated in the same PR as the next pin change (recorded in `known_debt`).
3. **AC8 digest non-determinism unchanged** (Podman layer-tar gzip) — content reproducibility is verified for the new locked build (identical file lists, counts, bytes, pip freeze, image size); digest still differs between builds. Known debt, tracked per P1-001.
4. **jsonschema `__version__` deprecation warning** appears on stderr when validate-design imports it (per the triaged patch's explicit command choice). Harmless: the anchored pattern matches the version line; visible only as the first line in `--verbose` output.

#### Handoff to

Bernstein: all 11 triaged patches applied and verified (build `d3c7f79d9df2` green, AC7 suite green under `--network=none`, negative paths green, two-build reproducibility green). `review_phase_1.fixes_applied: true`; triage records 11 applied + 3 deferred (P1-005/P1-017) + 8 dismissed. Recommended next: UAT pass on `candelamoon-docs:review`, then merge review (P1-017 / P1-022 remain tracked follow-ups).

### Bach (Senior Developer) — Review Phase 2 security patch round (2026-08-09)

#### Environment

- Host: Windows 11 (WSL2 backend; podman-machine-default). Podman 5.8.3 rootless.
- Base image `docker.io/library/python:3.11-slim@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553` cached locally (`--pull=never`).
- Prior image for red-phase evidence: `localhost/candelamoon-docs:review` (id `d3c7f79d9df2...`, pre-SEC-01 fix).
- Built image: `localhost/candelamoon-docs:phase2` (id `127a1439acb4a1478c9da085ade5fe2dd04466111a187b8f44a930d28e2a9b20`, 771,003,453 bytes).
- Build/verification logs: `%TEMP%/opencode/p1-002-phase2/build-phase2.log`, `build-phase2-repro.log`.

#### Actions

1. **Read** the handoff, my agent identity file, the activity-report template + `agent-output.schema.json`, both Phase 2 findings reports (`findings-phase-2-stravinsky.md` SEC-01..SEC-07, `findings-phase-2-brahms.md` dispositions), the P1-021 handoff (findings-array format precedent), and the current `Containerfile` / `validate-design`.
2. **SEC-01** — `validate-design`: added `cd /` at startup (after `set -eu`) so no check ever runs with the bind-mounted repository as its working directory; changed the jsonschema and pyyaml checks to `python3 -I -c "import ...; print(...__version__)"` (isolated mode — CWD, PYTHONPATH, and user site-packages are NOT on sys.path); documented the isolation rule in the script header and at both checks, including the P1-017 requirement (image-path imports, explicit /workspace paths).
3. **SEC-02** — `Containerfile`: moved the entire "Non-root builder user" section (groupadd/useradd/usermod --lock, supplementary-group reset, uid/gid asserts, sudoers loop, /home/builder contract) ABOVE the Python pip section; rewrote the pip section as a two-phase flow: `COPY --chown=builder:builder` of requirements.lock → `USER builder` `python3 -m pip download --no-cache-dir --require-hashes --no-deps --only-binary=:all: -r /tmp/requirements.lock -d /tmp/pip-wheelhouse` with fail-closed wheelhouse assertions (non-empty, only `.whl`) → `USER root` offline `python3 -m pip install --no-cache-dir --require-hashes --no-deps --only-binary=:all: --no-index --find-links=/tmp/pip-wheelhouse -r /tmp/requirements.lock` → `rm -rf /tmp/pip-wheelhouse /tmp/requirements.lock`. Extended the section comment with the root/builder split and wheel-only policy; updated the final-USER comment to document the temporary switches.
4. **Built** `podman build --pull=never -t candelamoon-docs:phase2 -f infra/containers/candelamoon-docs/Containerfile .` → 23/23 steps green (20 → 23: USER builder / USER root / COPY--chown layers).
5. **Verified** the full AC7 suite under `--network=none`, `pip freeze` vs the locked set, wheelhouse cleanup (`/tmp` clean in the image), `/home/builder` hygiene (3 skeleton files + empty .cache/.npm, no pip cache baked), negative paths (unknown arg / extra args → exit 2), and default-CMD behavior.
6. **SEC-01 proof** — red-phase on the pre-fix image: `/workspace/jsonschema.py` with `print("PWNED-JSONSCHEMA")` + spoofed `__version__ = "4.23.0"` → `OK: jsonschema PWNED-JSONSCHEMA`, exit 0 (attacker code executed AND false green). Green-phase on the new image: same hostile files (jsonschema.py + yaml.py) → exit 0 with real modules, no PWNED output anywhere.
7. **Reproducibility** — second `--no-cache` build (`phase2-repro`): identical per-tree file counts/bytes, identical pip freeze md5 `a6a8985a...` (same as the phase-1 review round), identical full file-list md5 `dca115fa...`, Compare-Object clean; sizes 771,003,453 vs 771,003,454 bytes (1-byte Podman gzip non-determinism, known AC8 debt). Removed `phase2-repro`.
8. **Committed** the code changes (`91bd8403`), updated this handoff (`head_sha`, review_phase_1 findings arrays with file paths, review_phase_2 triage: 2 applied + 4 deferred-to-CI + 1 dismissed, `fixes_applied: true`, this section) and wrote the activity report (JSON + MD).

#### Files

- Modified: `infra/containers/candelamoon-docs/Containerfile` — SEC-02 (builder block moved above pip; two-phase wheel-only download/install)
- Modified: `infra/containers/candelamoon-docs/validate-design` — SEC-01 (`cd /`, `python3 -I`, documentation)
- Modified: `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/handoff.md` — head_sha, review_phase_1 arrays, review_phase_2 triage, Agent Output
- Modified: `.maestro-space/maestro-works/phase-1-delivery-system/p1-002-candelamoon-docs-containerfile/bach-senior-developer-activity-report.md` / `.json` — this round
- Read (context): both Phase 2 findings reports, P1-021 handoff (array format), agent-output schema

#### Verification

| Command | Expected | Observed |
|---|---|---|
| `podman build --pull=never -t candelamoon-docs:phase2 -f infra/containers/candelamoon-docs/Containerfile .` | build succeeds | 23/23 steps, `Successfully tagged localhost/candelamoon-docs:phase2` (id `127a1439acb4...`, 771,003,453 bytes) |
| build log, download phase (USER builder) | wheels only, hash-verified | 9 wheels: `pip download --only-binary=:all:` → `Saved /tmp/pip-wheelhouse/*.whl` (incl. `PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.whl`, `rpds_py-2026.6.3-cp311-cp311-...whl`); wheelhouse asserts passed (9/9 `.whl`) |
| build log, install phase (USER root) | offline, from wheelhouse only | `Looking in links: /tmp/pip-wheelhouse`; all 9 wheels `Processing`'d; `rm -rf /tmp/pip-wheelhouse /tmp/requirements.lock` ran |
| `podman run --rm --network=none candelamoon-docs:phase2 python3 --version` | Python 3.11.x | `Python 3.11.15` |
| `... node --version` | v22.x | `v22.23.2` |
| `... npm --version` | 10.9.8 | `10.9.8` |
| `... markdownlint --version` | 0.45.0 | `0.45.0` |
| `... yamllint --version` | yamllint 1.37.1 | `yamllint 1.37.1` |
| `... markdown-link-check --version` | 3.13.7 | `3.13.7` |
| `... id` | uid=1000(builder) | `uid=1000(builder) gid=1000(builder) groups=1000(builder)` |
| `...` (default CMD) | validate-design exit 0 | `OK: all design validator tools present and runnable` (8/8 OK), exit 0 |
| `... validate-design --verbose` | real versions | 8 OK lines with versions (jsonschema line shows the known 4.x DeprecationWarning — cosmetic) |
| `... validate-design --verbsoe` | exit 2 + usage | exit 2 (`LASTEXITCODE=2`), usage on stderr |
| `... validate-design --verbose extra` | exit 2 + usage | exit 2, usage on stderr |
| `... bash -c 'curl -sS --max-time 5 https://pypi.org/'` | unreachable | `curl: (6) Could not resolve host: pypi.org` (exit 6) |
| `... pip freeze` | matches locked set | 10 entries identical to lock + base `packaging==26.3` (compare-identical) |
| `... bash -c 'ls /tmp/'` | no wheelhouse/lock | `node-compile-cache` only; `WHEELHOUSE-GONE` / `LOCK-GONE` |
| `... bash -c 'find /home/builder'` | builder-owned, no pip cache | 3 skeleton files (.bashrc/.profile/.bash_logout) + empty `.cache/pip` + `.npm`, all builder:builder |
| SEC-01 red (old `candelamoon-docs:review`): `/workspace/jsonschema.py` spoof | attack executes + false green | `OK: jsonschema PWNED-JSONSCHEMA`, exit 0 — attacker code executed as builder |
| SEC-01 green (`phase2`): same jsonschema.py + yaml.py in /workspace, run from /workspace | exit 0, no PWNED | 8/8 OK, exit 0, real modules, no PWNED output |
| AC8: second `--no-cache` build (`phase2-repro`) | identical content | identical tree counts/bytes (`/opt/node 9446/231786503`, `/usr/local 2446/45964552`, `/home/builder 3/4553`, `/workspace 0/0`), pip freeze md5 `a6a8985a...` (same as phase-1 round), file-list md5 `dca115fa...`, Compare-Object clean; size 771,003,453 vs 771,003,454 bytes; digests differ (`b7c0d722...` vs `3a5da59a...` — Podman gzip, known debt) |

Full logs: `%TEMP%/opencode/p1-002-phase2/build-phase2.log`, `build-phase2-repro.log`

#### Deviations

1. **`--no-cache-dir` added to the pip download phase** — Brahms' SEC-02 sketch omits it, but a builder-run `pip download` without it writes the HTTP/wheel cache under `/home/builder/.cache/pip`, baking build-varying content into the image and defeating AC8 (the exact reason PIP_NO_CACHE_DIR was scoped out of the runtime ENV in patch-3). The flag keeps the download phase cache-free; runtime pip cache volume behavior is unchanged.
2. **Wheelhouse created by the builder itself** (mkdir in the download RUN) instead of a root RUN + chown — one less root-owned intermediate path; the wheelhouse is builder-owned and cleaned up by the root install phase.
3. **`cd /` placed at script startup (all checks), not just before the Python checks** — Brahms' mitigation says "add `cd /` before the checks"; placing it at the top also stops non-Python tools (e.g. markdownlint config discovery) from resolving files relative to the repository. The Python checks additionally carry `-I`.
4. **`/home/builder` contents changed vs the phase-1 review image** — with builder creation moved before npm, `useradd --create-home` now finds no pre-existing `/home/builder` (npm no longer creates it first), so the Debian skeleton (.bashrc/.profile/.bash_logout, mode 700 home) is present: `/home/builder 3 files/4553 bytes` vs the phase-1 round's `4/0`. Deterministic across builds of this Containerfile (skeleton comes from the pinned base's /etc/skel); AC8 holds. The phase-1 recorded counts are superseded by the new baseline.

#### Known issues

1. **AC8 digest non-determinism unchanged** (Podman layer-tar gzip): content reproducibility verified for the SEC-02 build (identical trees, pip freeze md5 `a6a8985a...`, file-list md5 `dca115fa...`); image size differs by 1 byte (771,003,453 vs 771,003,454) and digests differ — same known debt as P1-001/phase-1.
2. **SEC-03..SEC-06 remain open at the image level by design** — all deferred-to-CI per Brahms: build-network egress enforcement, npm runtime sandboxing, runtime `--network=none` enforcement, and apt snapshot pinning. These become hard requirements of the CI job definition and the P1-005 apt snapshot work; the image-side controls (wheel-only pip, --ignore-scripts, hash locks, non-root runtime user) are in place.
3. **jsonschema `__version__` DeprecationWarning on stderr** (unchanged from phase 1) — harmless; visible only as the first line in `--verbose` output.
4. **npm audit debt unchanged** (8 vulnerabilities in the locked transitive npm tree) — P1-022 scope; the tree is locked and cannot drift.
5. **1-byte image-size difference between the two phase2 builds** (771,003,453 vs 771,003,454) — same Podman gzip non-determinism; content identical (file-list md5 equal).

#### Handoff to

Bernstein: SEC-01 and SEC-02 applied and green-verified (`candelamoon-docs:phase2` id `127a1439acb4`, 23/23 steps; AC7 suite green under `--network=none`; pip freeze matches the lock; SEC-01 red→green proof captured: pre-fix image false-greens with `PWNED-JSONSCHEMA` exit 0, fixed image exits 0 with real modules; two-build reproducibility green). `review_phase_2.fixes_applied: true`; triage records 2 applied + 4 deferred-to-CI (SEC-03..SEC-06) + 1 dismissed (SEC-07 → P1-017). Recommended next: UAT pass on `candelamoon-docs:phase2`, then merge review; carry SEC-03..SEC-06 into the CI job definition round and keep P1-017 / P1-022 tracked.
