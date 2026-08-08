# P1-015: Configure self-hosted Windows runner for host integration

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: none
**Complexity**: M
**Related ADRs**: 0014

## Description

Configure the self-hosted Windows runner for LuminalShine host integration.
Enables host-bound Windows tests off GitHub-hosted runners.

## Acceptance Criteria

- GitHub Actions self-hosted runner installed and connected on a Windows machine.
- Runner labeled for host integration workflows.
- Test job targeting the runner succeeds.
- Configuration documented.

## Implementation Plan

1. Set up the Windows host with the LuminalShine host installed.
2. Install GitHub Actions runner software.
3. Configure runner labels.
4. Test with a simple workflow job.

## Evidence Requirements

- Runner online in GitHub Actions.
- Test job completes.
- Documentation updated.

## Known Risks

- Windows host must remain powered and connected.
- LuminalShine host version must be pinned.

## References

- Infra: `docs/infrastructure/device-lab-architecture.md`
- ADRs: 0014

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
