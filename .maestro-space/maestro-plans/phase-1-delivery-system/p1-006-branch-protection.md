# P1-006: Configure GitHub branch protection rulesets

**Phase**: Phase 1
**Status**: Pending
**Dependencies**: none
**Complexity**: S
**Related ADRs**: 0013

## Description

Configure branch protection rulesets for the default branch (`moonlight-noir`):
no direct pushes, required reviews, required statuses. Enforces the delivery-model
commit gates.

## Acceptance Criteria

- Default branch has ruleset preventing direct pushes.
- PRs require at least one approving review before merge.
- Required status checks are configured.
- Ruleset is documented for future maintainers.

## Implementation Plan

1. Review current branch protection settings on GitHub.
2. Configure ruleset via GitHub UI or API.
3. Document the ruleset in `docs/infrastructure/` or a `.github/` config.

## Evidence Requirements

- Screenshot or API output showing the ruleset is active.
- A test push to the default branch is rejected.

## Known Risks

- Overly strict rulesets can block legitimate emergency fixes — document bypass procedure.
- Ruleset must not prevent the bot (candelamoon-bot) from opening PRs.

## References

- ADRs: 0013
- GitHub docs: branch protection rulesets

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| | | | | |
