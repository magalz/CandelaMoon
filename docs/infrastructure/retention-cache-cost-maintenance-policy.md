# Retention Cache Cost Maintenance Policy

## Artifacts

- Build artifacts retained: CI runs 30 days, release artifacts indefinitely, SBOMs indefinitely, test evidence 90 days, logs 30 days.
- Storage location: GitHub Actions artifacts, GitHub Releases, external storage.

## Cache

- CI cache: Gradle/AGP dependencies, Android SDK, NDK, Podman images.
- Cache key composition: image digest + lockfile hash + toolchain version.
- Eviction: LRU, max total size, per-branch limit.
- Poisoning prevention: no cache sharing between fork and non-fork PRs.

## Cost

- Estimated monthly CI cost for solo developer.
- Cost optimization: self-hosted runners for device/Windows tests, GitHub-hosted runners for container jobs, cache reuse, job parallelism control.
- Budget cap and alerting.

## Maintenance

Ongoing tasks; each task lists owner, frequency, trigger, and checklist.

### Android Target SDK Compliance

- Owner: @magalz
- Frequency: annual
- Trigger: new Android API level target or SDK availability
- Checklist: verify target SDK against Play policy, update candelamoon-android image, re-run device lab suite, update evidence manifest

### Dependency Updates

- Owner: @magalz
- Frequency: monthly
- Trigger: calendar (1st week of month) or security advisory
- Checklist: bump lockfiles, run per-PR pipeline, check nightly dependency freshness job, record results in evidence manifest

### Podman Image Rebuilds

- Owner: @magalz
- Frequency: quarterly
- Trigger: calendar (quarter start) or base-image upstream change
- Checklist: rebuild all four images, verify signatures, republish to GHCR, update cache keys, re-run canary PR

### Base Image Refresh

- Owner: @magalz
- Frequency: quarterly
- Trigger: upstream base image release or CVE advisory
- Checklist: diff base image changes, scan for new vulnerabilities, rebuild images, update SBOMs, republish

### Device Lab Calibration

- Owner: @magalz
- Frequency: per release
- Trigger: release-candidate pipeline preparation
- Checklist: verify Google TV Streamer runner health, API 28-30 compatibility tier, Windows host for LuminalShine, device test evidence

### Memtrace Reindex After Default-Branch Merges

- Owner: @magalz
- Frequency: per merge
- Trigger: merge to default branch (moonlight-noir)
- Checklist: confirm reindex completed, verify synchronization state tuple, confirm overlay episode recorded, run sync gate checks

### Security Scan Rule Updates

- Owner: @magalz
- Frequency: monthly
- Trigger: calendar (1st week of month) or scanner release
- Checklist: update scan rules and signatures, run security scan across repo, reconcile findings, update security scan evidence
