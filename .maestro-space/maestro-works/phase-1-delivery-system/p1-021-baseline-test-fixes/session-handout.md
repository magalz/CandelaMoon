# Session Handout — P1-021 Baseline Test Fixes (Tech Writer Phase)

**Date:** 2026-08-07
**Task:** P1-021 — Fix baseline unit test failures surfaced by Phase 0 CI (theme inflation + startup NPEs)
**ADR:** 0020 (Session Handout for Context Continuity)
**Spec:** `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md` sections 9.2 and 15

---

## Current State

- **Branch:** `phase1/p1-021-baseline-test-fixes`
- **Head SHA:** `584dc970996b4a1557b2a808a25afebe40464e7c` (workflow-only commit; previous source-code head `0aa9b711a4cdb215ce331831b17f455d6c8ee868` — all tracked code/test/XML changes)
- **Base SHA:** `53659407e185a4629bf9654a14f0f39b2c5c38c0`
- **PR URL:** https://github.com/magalz/CandelaMoon/pull/6 (`state: MERGED`, `isDraft: false` per `gh pr view` 2026-08-07; author `app/candelamoon-bot`; base `moonlight-noir`; title `P1-021: Fix baseline unit test failures`; merge commit `e952b09e93e061b5afb1ef8b015b9dc15282559c`; merged at `2026-08-07T21:14:26Z`; head `584dc970996b4a1557b2a808a25afebe40464e7c`)
- **Memtrace repo_id:** `CandelaMoon`
- **Memtrace indexed SHA:** `584dc970996b4a1557b2a808a25afebe40464e7c` (equals head; graph is source-code current — the final commit modifies only `.github/workflows/open-pr-bot.yml`, which is not symbol-tracked, so the graph content is unchanged from the `0aa9b711` index)
- **Memtrace index:** 21,029 nodes / 84,841 edges, last indexed 2026-08-07T19:17:20Z, branch `phase1/p1-021-baseline-test-fixes`
- **Handoff status:** `done` (schema-valid — UAT accepted, coverage audit PASS, PR opened, Memtrace GitHub review clean)
- **UAT decision:** `passed` — `UAT not applicable — evidence accepted.` All acceptance criteria are evidence-verified (no user-facing device behavior to test; the fixes are unit-test/CI-gate repairs).

## Completed Evidence

| Gate | Result | Evidence |
|---|---|---|
| Red phase (ADR 0016) | 22 tests, 2 failed (predicted); `StartupCrashTest.testUiHelperCrash` green at red phase (Robolectric attaches a real base Context — QA's static null-base prediction did not reproduce live) | `red-phase.log`; ATDD checklist `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/atdd-checklist.md` |
| Green phase (focused) | 22/22 PASS, BUILD SUCCESSFUL | `green-focused2.log` |
| Green phase (full suite, AC #4) | 68/68 PASS, BUILD SUCCESSFUL in 1m 45s (51 baseline + 16 API-tier matrix + 1 attached-lifecycle) | `review-green-full-final.log` |
| Base comparison | 51 tests, 5 failed → 68 tests, 0 failed (separates code defects from environment effects) | `base-full.log` |
| Review Phase 1 (Blind/Edge/Acceptance) | 6 triaged findings (PH1-001 through PH1-006); PH1-001/002/003/004 patched, PH1-005 deferred, PH1-006 dismissed | Handoff `review_phase_1` |
| Review Phase 2 (Red/Blue security) | SEC-001 info — no actionable security issue introduced | Handoff `review_phase_2` |
| Coverage audit (ADR 0019) | PASS — risk-weighted score 50/50 (100%); Memtrace reconciliation clean (detect_changes 0 unexpected symbols, get_timeline confirms 7 versions of `ArtemisApplication::onCreate`, get_evolution 14 episodes) | `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/coverage-audit.md` |
| UAT | passed — evidence accepted | Handoff `uat` |
| `git diff --check` | clean (5 XML files LF-normalized for PH1-004) | working tree |
| Workflow repair | `.github/workflows/open-pr-bot.yml` bound `create-pr` job to approved `maestro` environment (one-line commit `584dc970`); prior failed run `31215289096` (JWT decode error) superseded | commit `584dc970` |
| open-pr-bot workflow run | `31218847192` — succeeded; created PR #6 in draft state via `app/candelamoon-bot` | GitHub Actions run `31218847192` |
| Memtrace GitHub PR review | `review_github_pr` strict preview — succeeded, `graphState: ready`, **0 comments**, sourceCounts `ast=2 / cross_module=1 / online=0 / yaml=0` (single cross-module + two AST findings below the `strict`/`minSeverity=high` posting threshold) | PR #6 review preview |

## Artifacts Produced

| Path | Description | Tracked by git? |
|---|---|---|
| `app/src/main/java/com/limelight/ArtemisApplication.java` | `onCreate()` — `getBaseContext() != null` guard around failure-path Toast only; `ProfilesManager.load(this)` always runs (PH1-001 rework, final ast_hash `367796489c2397ea`) | yes |
| `app/src/main/res/values/styles.xml` | New `ProfilesExtendedFabButton` + `ProfilesFabButton` styles (exact widget-default parents, `enforceMaterialTheme=false` + `enforceTextAppearance=false`); scoped rationale + removal-criteria comment | yes |
| `app/src/main/res/layout/activity_app_view.xml` | `style="@style/ProfilesExtendedFabButton"` on EFAB; LF-normalized | yes |
| `app/src/main/res/layout/activity_pc_view.xml` | `style="@style/ProfilesExtendedFabButton"` on EFAB; LF-normalized | yes |
| `app/src/main/res/layout-land/activity_pc_view.xml` | `style="@style/ProfilesExtendedFabButton"` on EFAB; LF-normalized | yes |
| `app/src/main/res/layout/activity_profiles.xml` | `style="@style/ProfilesFabButton"` on FAB; LF-normalized | yes |
| `app/src/test/java/com/limelight/MaterialFabCompatTest.java` | New test: 4 methods × 4 SDKs (28/29/30/33) = 16 test instances — production/AppCompat theme inflation, landscape, enforcement-still-active | yes |
| `app/src/test/java/com/limelight/SimpleStartupTest.java` | New `testApplicationOnCreateLoadsProfilesWhenAttached` (attached-lifecycle assertion) | yes |
| `app/src/test/java/com/limelight/profiles/ProfilesNavigationTest.java` | Cast `ImageButton` → `ExtendedFloatingActionButton` on 2 methods (production widget type changed in `bdedb61b`, Jul 2025) | yes |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/atdd-checklist.md` | QA Architect red-phase ATDD checklist (ADR 0016) | yes (TRACKED at .maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/; was gitignored under old docs/handoffs/ per .gitignore, now part of tracked .maestro-space/) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/handoff.md` | Handoff file — single source of truth for task state (spec section 15.3) | no (gitignored) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/coverage-audit.md` | QA Architect standalone coverage audit (ADR 0019) — PASS, 50/50 | yes (committed in `4e834c93`, alongside the .maestro-space/maestro-plans/phase-1-delivery-system-backlog.md completion entry) |
| `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/session-handout.md` | This session handout (ADR 0020) | no (gitignored) |
| `.maestro-space/maestro-plans/phase-1-delivery-system-backlog.md` | P1-021 marked COMPLETE; P1-001 recorded as NEXT PENDING | yes |

## Pending Work

**Remaining for the next agent / operator:**

1. **`@magalz` review/approval of the P1-021 merge.** PR #6 is now `state: MERGED` (per `gh pr view` 2026-08-07, merge commit `e952b09e`, merged at `2026-08-07T21:14:26Z`), so the bot's `**Approval required from @magalz before merge.**` gate has been satisfied. The handoff status remains `done`; this entry is preserved as the explicit "owner sign-off" record per the spec's 15.3 single-source-of-truth contract. No further action is required from `@magalz` unless a post-merge review surfaces an issue.
2. **Begin P1-001 (next pending Phase 1 work item).** Create the official `infra/containers/candelamoon-android/Containerfile`. A local dev build of the CI-equivalent image was used to validate P1-021 (Containerfile preserved at `%TEMP%/opencode/p1-021/Containerfile`); promote it to the official location. Dependencies: none. Complexity: M. Related ADR: 0014. See `.maestro-space/maestro-plans/phase-1-delivery-system-backlog.md` P1-001.

## Keys For Next Session

- **Handoff file:** `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/handoff.md` (single source of truth for task state; frontmatter is schema-valid against `docs/schema/evidence-manifest.schema.json`)
- **Spec:** `docs/superpowers/specs/2026-08-05-candelamoon-roadmap-design.md` (sections 9.2 Podman Execution Boundary, 15 Agent Architecture And Task Workflow)
- **ADR register:** `docs/adr/` (21 ADRs: 0000 template + 0001-0020). Relevant to this task: 0014 (Podman-First Execution), 0016 (ATDD Red Phase Before Implementation), 0019 (Coverage Audit with Memtrace Reconciliation), 0020 (Session Handout for Context Continuity)
- **Coverage audit:** `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/coverage-audit.md` (standalone, PASS, 50/50)
- **ATDD checklist:** `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/atdd-checklist.md` (red-phase scaffolds and implementation tasks A/B/C/D)
- **Test artifacts:** `app/src/test/java/com/limelight/MaterialFabCompatTest.java`, `app/src/test/java/com/limelight/SimpleStartupTest.java`, `app/src/test/java/com/limelight/profiles/ProfilesNavigationTest.java`
- **Implementation backlog:** `.maestro-space/maestro-plans/phase-1-delivery-system-backlog.md` (P1-021 COMPLETE, P1-001 NEXT PENDING)
- **Evidence-manifest schema:** `docs/schema/evidence-manifest.schema.json` (status enum: in-progress, review, coverage-audit, uat, done, blocked)
- **Orchestrator guide:** `.maestro-space/maestro-docs/maestro-orchestrator-guide.md` (14-step task execution flow; step 13 = open PR via Memtrace `review_github_pr`)
- **Memtrace repo_id:** `CandelaMoon` (indexed at head `584dc970`; graph content unchanged from the `0aa9b711` source-code head because the final commit is workflow-only — no re-index required)
- **Memtrace episode IDs:** `4ad065db-d367-44e6-b0a9-dd64c2d79b53`, `b6b5726b-56ab-46ad-b5b9-29c0e6f1817c`, `5b923d4e-444c-4c70-95d5-74513de14fa2`, `6666fd06-14c6-4bc6-b5cf-0133f967e240`
- **Containerized test logs:** `%TEMP%/opencode/p1-021/logs/` (`red-phase.log`, `green-focused2.log`, `green-full2.log`, `base-full.log`, `review-focused2.log`, `review-green-full*.log`)
- **Local dev Containerfile (for P1-001):** `%TEMP%/opencode/p1-021/Containerfile`

## Known Debt

| ID | Item | Severity | Resolution |
|---|---|---|---|
| PH1-005 | LayoutInflationTest's pre-existing retry behavior (`catch InflateException → retry with FrameLayout`) weakens diagnostic evidence for `<merge>` root layouts; outside changed files, not required for P1-021 green | low | Follow-up task (do not expand P1-021 scope) |
| DOC-001 | Narrative discrepancy: the Senior Developer's review-patch Agent Output reports the review-focused run as "20/20 PASSED" but `review-focused2.log` shows 24 PASSED (16 MaterialFabCompatTest + 8 SimpleStartupTest). Arithmetic error in the narrative ("4 SimpleStartupTest methods" — actually 8). Build is green; all claimed tests pass. The standalone coverage audit records the correct count (24). | low (non-blocking, documentation-only) | No code/test change required; narrative is documentation-only debt. Next agent editing the handoff narrative should correct the count to 24/24. |
| DOC-002 | JaCoCo line-coverage report not generated (containerized test runs did not invoke `jacocoTestReport`; bare host has no Android SDK). Not a coverage gap — static mapping confirms every changed symbol is tested. | low (non-blocking) | Add `jacocoTestReport` to the CI test job in a future infra task (P1-010/P1-011 territory) |
| DOC-004 | The `candelamoon-android` image used for the containerized test runs is a local dev build of the CI-equivalent toolchain (Containerfile preserved at `%TEMP%/opencode/p1-021/Containerfile`). The official `infra/containers/candelamoon-android/Containerfile` is P1-001 territory. | low (non-blocking) | Resolved by P1-001 |

## UAT Decision

- **Status:** `passed`
- **User decision:** `UAT not applicable — evidence accepted.`
- **Rationale:** All five acceptance criteria are evidence-verified (red/green test runs, coverage audit, Memtrace reconciliation, security review). There is no user-facing device behavior to test — P1-021 repairs pre-existing unit-test/CI-gate failures. The orchestrator accepted the evidence.

## PR Status

- **PR URL:** https://github.com/magalz/CandelaMoon/pull/6
- **Status (verified via `gh pr view` 2026-08-07):** `state: MERGED`, `isDraft: false`
- **Author:** `app/candelamoon-bot`
- **Title:** `P1-021: Fix baseline unit test failures` (renamed from the bot's auto-generated `p1 021 baseline test fixes` before merge)
- **Base branch:** `moonlight-noir`
- **Head branch:** `phase1/p1-021-baseline-test-fixes`
- **Head SHA:** `584dc970996b4a1557b2a808a25afebe40464e7c`
- **Merge commit:** `e952b09e93e061b5afb1ef8b015b9dc15282559c`
- **Merged at:** `2026-08-07T21:14:26Z`
- **Workflow run that opened it:** `31218847192` (succeeded) — `.github/workflows/open-pr-bot.yml` `create-pr` job, bound to approved `maestro` environment by commit `584dc970`. The Created PR row in Completed Evidence below reflects the bot's "Created draft PR" action at the time it ran; the draft status was lifted before merge.
- **Memtrace GitHub review:** `review_github_pr` strict preview succeeded with `graphState: ready`, **0 comments** posted, sourceCounts `ast=2 / cross_module=1 / online=0 / yaml=0`.
- **Coverage audit commit:** `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/coverage-audit.md` is tracked in commit `4e834c93` (`docs(P1-021): record coverage audit and backlog completion`); it is no longer a pending commit item.

## Rollback Strategy

To undo the P1-021 work if needed:

1. **If the PR is not yet merged:** Close PR #6 (https://github.com/magalz/CandelaMoon/pull/6) and delete branch `phase1/p1-021-baseline-test-fixes` from the remote and local. The `moonlight-noir` base branch is untouched — all work was on the task branch.
2. **If the PR is merged:** Revert the merge commit on `moonlight-noir` (`git revert -m 1 <merge-sha>`), force-reindex Memtrace against the new head, and re-run the base suite to confirm the 5 pre-existing failures are restored to their pre-P1-021 state (they are the baseline failures this task fixed).
3. **Files affected (10 total):** 1 production Java (`ArtemisApplication.java`), 5 XML resources (`styles.xml`, 3 layouts + 1 landscape), 3 test Java files (`MaterialFabCompatTest.java`, `SimpleStartupTest.java`, `ProfilesNavigationTest.java`), 1 workflow file (`.github/workflows/open-pr-bot.yml` — workflow-only commit `584dc970`; revert is safe and restores the un-bound `create-pr` job). No unrelated files were touched.
4. **Documentation rollback:** Revert the `.maestro-space/maestro-plans/phase-1-delivery-system-backlog.md` changes (un-mark P1-021 complete, remove the P1-001 NEXT PENDING note). The handoff/ATDD/audit/session-handout files under `.maestro-space/maestro-works/phase-1-delivery-system/p1-021-baseline-test-fixes/` are TRACKED and can be reverted with the task branch — delete them if no longer needed.
