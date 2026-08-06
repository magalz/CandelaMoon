# Incident And Rollback Policy

This policy defines what happens when something goes wrong: a bad release, a compromised dependency or base image, or a broken Memtrace/GitHub synchronization state. The guiding rule: halt first, diagnose second, repair third, verify fourth, resume fifth. For Memtrace, there is no substitute path: if Memtrace is unavailable, no code changes are authorized.

## Bad Release

A "bad release" is any release found, after publication, to contain a critical defect, a security vulnerability, a licensing violation, or a provenance break.

Procedure:
1. **Identify** — confirm the report (user reports, monitoring, CI evidence, scanner findings) and record it in the incident log.
2. **Halt distribution within 1 hour** — remove the release from the distribution channel (deprecate/hide on the release page, disable the auto-update channel, remove from the store listing if pushed there). Download traffic for the bad version must stop or be blocked.
3. **Pull the release** — unpublish or supersede the artifacts; keep the evidence bundle (screenshots, logs, test reports) for the post-mortem.
4. **Security advisory if applicable** — if the defect is a vulnerability, publish an advisory per the vulnerability disclosure process within 24 hours for critical cases.
5. **Prepare the fix** — fix on a dedicated branch with the regression test attached; the fix goes through the normal review + scan + sign pipeline on the fastest emergency track.
6. **Release the patched version** — ship the patched release through the standard signed pipeline; the patched version must be above the bad version and the SBOM diff between the two is reviewed.
7. **Post-mortem** — within 5 working days: root cause, why the gate missed it, which gate should have caught it, and the pipeline change that closes the gap.

Time targets: halt within 1 hour; fix within 24 hours for critical defects (72 hours for high); post-mortem within 5 working days.

## Compromised

### Compromised dependency

1. **Identify affected artifacts** — find every release and every CI build whose SBOM contains the compromised component; SBOM search is the primary tool.
2. **Scan SBOMs** — build a full inventory of where the component is used, including transitive usage and container images containing it.
3. **Halt builds using the compromised version** — block CI on any build that resolves to the compromised version; the version-catalog pin bump to a safe version lands first, before any rebuild.
4. **Pin to a safe version** — bump the lockfile/catalog to the nearest unaffected version, verify with the scanner, and review the diff.
5. **Rebuild and re-sign** — all affected release artifacts are rebuilt from the safe pin, re-scanned, re-signed with the release key, and re-issued with new provenance; old artifacts are pulled and superseded.
6. **Notify users** — affected versions are listed in a release note and, for critical cases, in a security advisory.

### Compromised base image

The procedure is identical to the compromised-dependency procedure, plus:

- **Replace all derived container images** — every image that references the compromised base (directly or transitively) is rebuilt from the emergency base image (nearest unaffected digest), regardless of whether scanning shows a reachable vulnerability. Image digests in provenance are updated and re-verified.

## Stale Graph

A "stale graph" is a state where the Memtrace index and GitHub disagree about the state of the repository: for example, `main` at a local SHA the remote does not have, the Memtrace index at a SHA matching neither local nor remote, or a rebase/force-push that desynchronized the replay history.

Procedure:
1. **Halt all development** — freeze all edits, commits, and PR merges on the affected branch. No new work enters the repository until synchronization is verified. If Memtrace is unavailable, the halt persists: there is no substitute path that authorizes code changes without Memtrace.
2. **Diagnose** — establish the three-way state: local Git (`git rev-parse main`), remote Git (`git ls-remote origin main`), and the Memtrace indexed SHA (`memtrace status --json`, which reports the indexed commit). Determine which pair disagrees and why (unpushed commits, force-push, missed index update, daemon down).
3. **Repair** — per diagnosis:
   - Local vs remote mismatch: reconcile with the team (push, reset, or merge) and record the chosen resolution.
   - Memtrace index stale relative to git: reindex (`memtrace index` incremental, or `replay_history` after cleanup if the replay is broken).
   - Rebase aftermath: re-run history replay so the bi-temporal record matches the new lineage.
   - Configuration break: fix the daemon/watch configuration, then reindex.
4. **Verify synchronization canary** — after repair, check a known canary: a symbol known to have changed during the incident must appear in the replayed graph at the correct commit (for example, `get_evolution` between two known commits matches git's own log). Only a passing canary authorizes resuming.
5. **Resume** — unfreeze the branch and continue; the incident is closed.

**If Memtrace is unavailable** (daemon down, store corrupt, index lost): wait for restoration; no substitute path authorizes code changes. Manual git operations are still permitted (branch housekeeping, tag fixes) but no code edits, commits, or merges happen until the canary passes.

Record every incident in the phase audit (`phase-audit` log): time detected, diagnosis, repair actions, canary result, resume time. The audit entry is required for closure, not optional.
