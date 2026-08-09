# Session Handout Template

> The continuity document that lets the NEXT session begin work with ZERO conversation
> history. The session handout is the only state that survives across sessions.

The companion JSON file is `session-handout.json` (machine-readable keys). The
Tech Writer produces this at step 14 of the per-task 14-step cycle.

**File location**: `.maestro-space/maestro-works/<phase-short-desc>/<task-id>-<short-desc>/session-handout.md`

---

```markdown
# Session Handout — <task-id> <task short title>

**Date**: <YYYY-MM-DD>
**Task**: <task-id> — <task statement>
**ADR**: 0020 (Session Handout for Context Continuity)
**Spec**: `docs/superpowers/specs/<spec>.md` section <N>

---

## Current State

- **Branch**: `<task branch>`
- **Head SHA**: `<40-char hex>` (with note if workflow-only)
- **Base SHA**: `<40-char hex>`
- **PR URL**: <GitHub PR URL, state, draft status, merge status, merge commit if merged>
- **Memtrace repo_id**: `<repo-id>`
- **Memtrace indexed SHA**: `<40-char hex>` (equals head; note if graph content is from a
  prior source-code head because the final commit is workflow-only)
- **Memtrace index**: <node count> / <edge count>, last indexed <ISO timestamp>, branch
- **Handoff status**: `<status>` (schema-valid value)
- **UAT decision**: `<uat.status>` — `<user_decision>`

## Completed Evidence

| Gate | Result | Evidence |
|---|---|---|
| Red phase (ADR 0016) | <N> tests, <M> failed (predicted) | `<log path>`; ATDD checklist `<path>` |
| Green phase (focused) | <N>/<N> PASS | `<log path>` |
| Green phase (full suite) | <N>/<N> PASS | `<log path>` |
| Base comparison | <N> tests, <M> failed → <N'> tests, <M'> failed | `<log path>` |
| Review Phase 1 | <N> triaged findings | handoff `review_phase_1` |
| Review Phase 2 | <N> findings | handoff `review_phase_2` |
| Coverage audit (ADR 0019) | <PASS/CONDITIONAL/FAIL>, risk-weighted score <X>/<Y> | `<coverage-audit path>` |
| UAT | <passed / failed> | handoff `uat` |
| `git diff --check` | clean / not clean | working tree |
| Workflow repair (if any) | <commit> | <description> |
| open-pr-bot workflow run | <run id> — <succeeded/failed> | GitHub Actions |
| Memtrace GitHub PR review | <comments posted> | PR review |

## Artifacts Produced

| Path | Description | Tracked? |
|---|---|---|
| `<path>` | <description> | yes / no (gitignored) |

## Pending Work

[Numbered list. For each pending item: description, why it's pending, dependencies,
the next session's expected first action.]

1. **<@magalz review/approval>** — <description>; status: <pending / merged>
2. **<next task>** — <description>; depends on: <prerequisites>

## Keys For Next Session

- **Handoff file**: `<path>` (single source of truth for task state; schema-valid against
  `docs/schema/evidence-manifest.schema.json`)
- **Spec**: `docs/superpowers/specs/<spec>.md` (sections <N>)
- **ADR register**: `docs/adr/` (<count> ADRs). Relevant: <id list>
- **Coverage audit**: `<path>`
- **ATDD checklist**: `<path>`
- **Test artifacts**: `<path list>`
- **Implementation backlog**: `<path>` (<task-id> <status>, <next-task-id> <status>)
- **Evidence-manifest schema**: `docs/schema/evidence-manifest.schema.json`
- **Orchestrator guide**: `.maestro-space/maestro-docs/maestro-orchestrator-guide.md`
- **Workflow**: `.maestro-space/maestro-docs/maestro-workflow.md`
- **Conventions**: `.maestro-space/maestro-docs/maestro-conventions.md`
- **Memtrace repo_id**: `<repo-id>` (indexed at head `<sha>`; <note if workflow-only>)
- **Memtrace episode IDs**: `<uuid list>`
- **Containerized test logs**: `<path>`
- **Local dev Containerfile** (if any): `<path>`

## Known Debt

| ID | Item | Severity | Resolution |
|---|---|---|---|
| <id> | <description> | <low/med/high> | <how/when to resolve> |

## GitHub Issues Created

Per orchestrator guide §8.2.1 — every HIGH/MEDIUM deferred finding creates a tracked GitHub issue.

| Issue | Severity | Finding(s) | Target |
|---|---|---|---|
| [#N](url) <prefix> | <severity> | <finding IDs> | <owning task> |

Pre-existing issues carrying findings from this task (if any):
| [#N](url) <prefix> | <severity> | <finding IDs> | <owning task> |

## UAT Decision

- **Status**: `<passed/failed/pending>`
- **User decision**: `<text>`
- **Rationale**: <one paragraph>

## PR Status

- **PR URL**: <url>
- **Status**: `state` + `isDraft`
- **Author**: `<app/candelamoon-bot or user>`
- **Title**: `<text>`
- **Base branch**: `<text>`
- **Head branch**: `<text>`
- **Head SHA**: `<sha>`
- **Merge commit** (if merged): `<sha>`
- **Merged at**: `<ISO timestamp>`
- **Workflow run that opened it**: `<id>` — `<succeeded/failed>`
- **Memtrace GitHub review**: <comments posted>, sourceCounts
- **Coverage audit commit**: `<sha>` (description)

## Rollback Strategy

1. **If the PR is not yet merged**: close PR and delete branch
2. **If the PR is merged**: revert the merge commit, force-reindex Memtrace, re-run base suite
3. **Files affected** (N total): <list>
4. **Documentation rollback**: <which docs to revert>
```
