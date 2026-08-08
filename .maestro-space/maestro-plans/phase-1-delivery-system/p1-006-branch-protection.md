# P1-006: Configure GitHub branch protection rulesets

**Phase**: Phase 1
**Status**: In Development
**Dependencies**: none
**Complexity**: S
**Related ADRs**: 0013

## Current Evidence

- PR #3 (merged): Added CODEOWNERS (`* @magalz`), CI workflow, bot PR creation.
- CI workflow triggers on push/PR to `moonlight-noir`.
- Branch protection rulesets not yet fully configured (no required reviews, status checks).

## Description

Configure branch protection rulesets for the default branch: no direct pushes,
required reviews, required statuses. Enforces the delivery-model commit gates.

## Acceptance Criteria

- [ ] Default branch has ruleset preventing direct pushes.
- [ ] PRs require at least one approving review before merge.
- [ ] Required status checks are configured (CI test job).
- [ ] Ruleset is documented.

## Remaining Work

1. Configure ruleset via GitHub UI or API.
2. Add required status check: CI `test` job.
3. Document the ruleset.

## Evidence Requirements

- API output or screenshot showing ruleset is active.
- Test push to default branch is rejected.

## Known Risks

- Overly strict rulesets can block emergency fixes — document bypass procedure.
- Ruleset must not prevent `candelamoon-bot` from opening PRs.

## References

- CODEOWNERS: `.github/CODEOWNERS`
- CI: `.github/workflows/ci.yml`
- ADRs: 0013

## Session History

| Session Date | Status Change | Head SHA | PR URL | Handoff Path |
|---|---|---|---|---|
| 2026-08-06 | In Development (PR #3) | — | PR #3 | — |
