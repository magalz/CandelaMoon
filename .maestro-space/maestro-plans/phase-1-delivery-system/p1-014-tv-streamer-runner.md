# P1-014: Configure self-hosted runner for Google TV Streamer

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: none
**Complexity**: M
**Related ADRs**: 0014

## Description

Configure the self-hosted runner for the Google TV Streamer device. Enables
host-bound device tests off GitHub-hosted runners.

## Acceptance Criteria

- GitHub Actions self-hosted runner is installed and connected on the TV Streamer host.
- Runner is labeled appropriately for workflow targeting.
- A test workflow job runs on the device runner.
- Runner configuration is documented.

## Implementation Plan

1. Set up the physical host machine with the TV Streamer connected.
2. Install GitHub Actions runner software.
3. Configure runner labels and environment.
4. Test with a simple workflow job.

## Evidence Requirements

- Runner appears as "online" in GitHub Actions settings.
- Test job completes on the runner.
- Documentation of the setup in `docs/infrastructure/device-lab-architecture.md`.

## Known Risks

- TV Streamer must remain powered and connected.
- Network firewall rules may need adjustment.

## References

- Infra: `docs/infrastructure/device-lab-architecture.md`
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
