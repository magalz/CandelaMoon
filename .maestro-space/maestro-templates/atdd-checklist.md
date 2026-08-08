# ATDD Red-Phase Checklist Template

> The QA Architect's red-phase scaffold for a task. Maps each acceptance criterion to
> the failing test, the production root cause, the implementation task, and the
> verification command.

The companion JSON file is `atdd-checklist.json`, which is the machine-readable form.
See `agent-output.schema.json` `artifact_type: atdd-checklist`.

**File location**: `.maestro-space/maestro-works/<phase-short-desc>/<task-id>-<short-desc>/atdd-checklist.md`

---

```markdown
# ATDD Red-Phase Checklist — <task-id>: <task short title>

- **Task**: <task-id> — <task statement>
- **Branch**: `<task branch>`
- **Base SHA**: `<40-char hex>`
- **QA Architect phase**: Red-phase scaffold creation (ADR 0016)
- **Production phase owner**: <production agent name>

## Scope

[What this checklist covers and what it does NOT cover. Typically: it covers only the
task's named failing tests; it does not gate the broader test suite — that is an AC the
green phase verifies.]

## Red-phase scaffolds

[List each scaffold (test method), the file, the lines, and the post-fix contract it
asserts. If the test already exists and is well-formed, confirm it as the red-phase
scaffold rather than duplicating it.]

| # | Test | File | Lines | Asserts (post-fix contract) |
|---|------|------|-------|------------------------------|
| 1 | `<TestClass>.<testMethod>` | `app/src/test/...` | NN–NN | <what the test asserts must hold after the fix> |

## Root-cause mapping (test → production failure)

| Test | Current failure | Production root cause |
|------|-----------------|------------------------|
| 1 | <error class, message, key frame> | <which production code, which API, why it fails today> |

## Implementation checklist (one task per scaffold, red → green)

The production agent activates one test at a time. Each task turns its scaffold green
without weakening the assertion and without skipping the test. The repair must preserve
the task's safety invariants (e.g., API tier compatibility, production behavior
preservation).

### Task A — Make `<test method>` green

- **Scaffold**: `<fully qualified test name>`
- **AC verified**: <which AC(s)>
- **Implementation options** (developer picks the minimal production-safe one):
  - <option 1>
  - <option 2>
- **Verify**:
  - `<gradle command>` is green
  - <any other check>
- **Do not**:
  - <forbidden change 1>
  - <forbidden change 2>

[One Task block per scaffold.]

## Red-phase verification

- **Environment limitation** (if any): <why live run can't happen in this session>
- **Static red-phase evidence** (in lieu of a live run): <for each scaffold, the static
  reading of the test + production code that proves it must currently fail>
- **Live red-phase run** (if performed): <command, log path, observed failures>
- **`red_phase_verified` value in handoff**: `true` or `false` with justification

## Test quality standards (ADR 0016)

- **Readable**: each scaffold uses a clear assertion message naming the contract
- **Maintainable**: shares the project's test infrastructure (suppressors, shadows, etc.)
- **Isolated**: resets state in `@Before`; no shared mutable state between tests
- **Deterministic**: pins SDK and any relevant `@Config`; no real I/O or network
- **Atomic**: one contract per test method
- **Fast**: no `Thread.sleep`, no retries, no arbitrary waits

## Handoff back to orchestrator

The red-phase scaffolds are confirmed in place. The production agent may begin
implementation, activating one test at a time. The QA Architect will run the coverage
audit (ADR 0019) with Memtrace reconciliation after the green phase is evidenced.
```
