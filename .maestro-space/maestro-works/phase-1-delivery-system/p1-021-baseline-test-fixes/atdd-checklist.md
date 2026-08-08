# ATDD Red-Phase Checklist — P1-021: Baseline unit test failures

- **Task**: P1-021 — Fix baseline unit test failures surfaced by Phase 0 CI (theme inflation + startup NPEs)
- **Branch**: `phase1/p1-021-baseline-test-fixes`
- **Base SHA**: `53659407e185a4629bf9654a14f0f39b2c5c38c0`
- **QA Architect phase**: Red-phase scaffold creation (ADR 0016)
- **Production phase owner**: Senior Developer (implements until green, one test at a time)

## Scope

This checklist covers only the three named failing tests in the handoff acceptance criteria. It does not gate the broader `testNonRoot_gameDebugUnitTest` suite — that is AC #4 and is verified at green phase. The red phase establishes that each target test encodes the intended post-fix behavior and currently fails for the documented root cause, before any production code is written.

## Red-phase scaffolds (already present in the repository)

The three target tests already exist in `app/src/test/java/com/limelight/`. They are not `@Ignore`d, do not use `Assume`, and do not weaken assertions: each uses the codebase's existing `try { ... } catch (Exception e) { fail(...) }` convention to assert the no-crash contract. The QA Architect confirms these as the red-phase scaffolds rather than duplicating them — duplicate scaffolds would risk drift and weaken the red signal.

| # | Test | File | Lines | Asserts (post-fix contract) |
|---|------|------|-------|------------------------------|
| 1 | `LayoutInflationTest.allLayoutsInflateSuccessfully` | `app/src/test/java/com/limelight/LayoutInflationTest.java` | 25–39 | Every `R.layout.*` inflates without `InflateException` under a `Theme_AppCompat` context. |
| 2 | `SimpleStartupTest.testApplicationOnCreate` | `app/src/test/java/com/limelight/SimpleStartupTest.java` | 55–71 | `new ArtemisApplication().onCreate()` completes and `ProfilesManager` is initialized; no null-base `Context` NPE. |
| 3 | `StartupCrashTest.testUiHelperCrash` | `app/src/test/java/com/limelight/StartupCrashTest.java` | 93–103 | `Robolectric.buildActivity(PcView.class).create().get()` + `UiHelper.setLocale(activity)` completes; no null-base `Context` NPE. |

## Root-cause mapping (test → production failure)

| Test | Current failure | Production root cause |
|------|-----------------|------------------------|
| `allLayoutsInflateSuccessfully` | `android.view.InflateException` on `activity_app_view.xml` line 45 | `activity_app_view.xml` uses `com.google.android.material.floatingactionbutton.ExtendedFloatingActionButton`, which requires a `Theme.MaterialComponents` descendant. The test inflates under `Theme_AppCompat` (not a MaterialComponents descendant), so the widget cannot resolve its style attributes. The production `AppTheme` (in `app/src/main/res/values/styles.xml`) already extends `Theme.MaterialComponents.NoActionBar`, but the layout/style contract is not robust to a non-Material context and the test deliberately probes the inflation contract. |
| `testApplicationOnCreate` | `NullPointerException: Cannot invoke "android.content.Context.getFilesDir()" because "this.mBase" is null` | `ArtemisApplication.onCreate()` calls `super.onCreate()` then `ProfilesManager.getInstance().load(this)`. The test constructs `new ArtemisApplication()` directly, so Robolectric never calls `attachBaseContext(Context)` and `mBase` is null when `load()` reaches `context.getFilesDir()`. The startup path must tolerate a null/unattached base Context rather than dereference it. |
| `testUiHelperCrash` | Same null-base `Context` NPE during `PcView` creation / `UiHelper.setLocale(activity)` | The mocked startup path touches `Context` services (`getSystemService`, `getResources`, `PreferenceConfiguration.readPreferences`) before the activity's base Context is fully attached under Robolectric. The startup/UI-helper path must guard against a null base Context or defer Context access until `attachBaseContext` has run. |

## Implementation checklist (one task per scaffold, red → green)

The Senior Developer activates one test at a time. Each task must turn its scaffold green without weakening the assertion and without skipping the test. The repair must preserve API 28 compatibility (ADR 0007) and must not weaken production startup or layout behavior (AC #5).

### Task A — Make `LayoutInflationTest.allLayoutsInflateSuccessfully` green

- **Scaffold**: `app/src/test/java/com/limelight/LayoutInflationTest.java#allLayoutsInflateSuccessfully`
- **AC verified**: #1 (no `InflateException`), #5 (preserve layout behavior).
- **Implementation options (developer picks the minimal production-safe one)**:
  - Harden `activity_app_view.xml` (and any sibling layout with the same issue) so the `ExtendedFloatingActionButton` does not require a MaterialComponents theme to inflate — e.g., supply explicit `app:elevation` / `app:backgroundTint` / widget style attributes inline so the widget does not depend on theme-resolved defaults.
  - Or supply a `tools:`-scoped style override and ensure the layout is self-contained.
  - Do NOT change the test's `Theme_AppCompat` context — that is the contract being asserted.
- **Verify**:
  - `./gradlew :app:testNonRoot_gameDebugUnitTest --tests com.limelight.LayoutInflationTest` is green.
  - No other layout in the `R.layout.*` set regresses (the test iterates all of them).
- **Do not**:
  - Add `@Ignore` to the test.
  - Replace `Theme_AppCompat` with a Material theme in the test (that would hide the contract gap).
  - Skip the `ExtendedFloatingActionButton` from the iteration.

### Task B — Make `SimpleStartupTest.testApplicationOnCreate` green

- **Scaffold**: `app/src/test/java/com/limelight/SimpleStartupTest.java#testApplicationOnCreate`
- **AC verified**: #2 (no null-base `Context` failure), #5 (preserve startup behavior).
- **Implementation options (developer picks the minimal production-safe one)**:
  - Harden `ArtemisApplication.onCreate()` so it does not dereference a null/unattached base Context — defer `ProfilesManager.load(this)` until after `attachBaseContext`, or guard `getFilesDir()`/`getApplicationContext()` against a null `mBase`.
  - Harden `ProfilesManager.load(Context)` so it tolerates a Context whose base is not yet attached (return early / defer), without changing the production load contract for a real attached Context.
  - Do NOT change the test to call `attachBaseContext` manually or to mock the Context — that would hide the startup-path fragility.
- **Verify**:
  - `./gradlew :app:testNonRoot_gameDebugUnitTest --tests com.limelight.SimpleStartupTest --tests '*testApplicationOnCreate*'` is green.
  - `ProfilesManager.getInstance()` still returns a non-null instance and `getProfiles()` still returns a non-null list (the scaffold asserts both).
- **Do not**:
  - Add `@Ignore` to the test.
  - Wrap the body in a `try/catch` that swallows the NPE — the test already does that and calls `fail(...)`.
  - Skip `ProfilesManager.load(this)` in production — the load must still run on a real device.

### Task C — Make `StartupCrashTest.testUiHelperCrash` green

- **Scaffold**: `app/src/test/java/com/limelight/StartupCrashTest.java#testUiHelperCrash`
- **AC verified**: #3 (no null-base `Context` failure), #5 (preserve startup/UI behavior).
- **Implementation options (developer picks the minimal production-safe one)**:
  - Harden `PcView.onCreate()` / `UiHelper.notifyNewRootView()` / `UiHelper.setLocale()` so they tolerate a null/unattached base Context under Robolectric — guard `getSystemService`, `getResources`, `getWindow`, and `PreferenceConfiguration.readPreferences` callers.
  - Or ensure the activity lifecycle defers Context access until `attachBaseContext` has run.
  - The fix for Task B may also resolve Task C if the root cause is shared (null `mBase`). The developer should confirm with both tests green.
- **Verify**:
  - `./gradlew :app:testNonRoot_gameDebugUnitTest --tests com.limelight.StartupCrashTest --tests '*testUiHelperCrash*'` is green.
  - `UiHelper.setLocale(activity)` still mutates locale on a real attached activity (no production behavior change).
- **Do not**:
  - Add `@Ignore` to the test.
  - Stub `UiHelper.setLocale` to a no-op in production.
  - Remove the `ShadowMoonBridge` / `ShadowGameManager` shadows from the test `@Config`.

### Task D — Make the required Gradle unit-test target green (AC #4)

- **Command**: `./gradlew testNonRoot_gameDebugUnitTest` (or the CI `test` job).
- **Verify**: the whole `nonRoot_gameDebug` unit-test variant is green, not just the three named tests.
- **Do not**: broaden `testOptions` to skip flaky tests, or add `@Ignore` to any other test to make the suite green.

## Red-phase verification

- **Environment limitation**: The bare Windows host in this session does not have the Android SDK installed (`ANDROID_HOME` / `ANDROID_SDK_ROOT` unset, no `local.properties`, no SDK directory under `C:\Android`, `C:\Users\magal\AppData\Local\Android\Sdk`, or `C:\android-sdk`). Per ADR 0014, the project's execution boundary is the `candelamoon-android` Podman image, not the bare host. The Gradle wrapper (`gradlew.bat`) requires the Android SDK to configure AGP, so `./gradlew testNonRoot_gameDebugUnitTest` cannot be run from this QA session on the bare host.
- **Static red-phase evidence** (in lieu of a live run):
  - `LayoutInflationTest.allLayoutsInflateSuccessfully` iterates `R.layout.*` and inflates under `Theme_AppCompat`; `activity_app_view.xml` uses `ExtendedFloatingActionButton` which requires a MaterialComponents descendant → the test must throw `InflateException` and fail. Confirmed by reading `app/src/main/res/layout/activity_app_view.xml` (line 33–45) and `app/src/main/res/values/styles.xml` (the test context `Theme_AppCompat` is not a MaterialComponents descendant).
  - `SimpleStartupTest.testApplicationOnCreate` constructs `new ArtemisApplication()` and calls `onCreate()`; `ArtemisApplication.onCreate()` (`app/src/main/java/com/limelight/ArtemisApplication.java` lines 10–16) calls `ProfilesManager.getInstance().load(this)`, which reaches `context.getFilesDir()` (`app/src/main/java/com/limelight/profiles/ProfilesManager.java` line 68). Robolectric does not call `attachBaseContext` for a directly constructed `Application`, so `mBase` is null → NPE → `fail(...)`. Confirmed by reading both files.
  - `StartupCrashTest.testUiHelperCrash` calls `Robolectric.buildActivity(PcView.class).create().get()` then `UiHelper.setLocale(activity)`; `UiHelper.setLocale` (`app/src/main/java/com/limelight/utils/UiHelper.java` lines 77–106) calls `PreferenceConfiguration.readPreferences(activity)` and `activity.getResources()`; the activity creation path touches `Context` services before the base is attached under the mocked environment → NPE → `fail(...)`. Confirmed by reading `UiHelper.java`.
- **Live red-phase run**: Deferred to the first CI run on the `candelamoon-android` Podman image, or to the Senior Developer's local containerized run. The Senior Developer must capture the exact `./gradlew` command and the failing-test output as red-phase evidence before starting implementation, per ADR 0016.
- **`red_phase_verified` value in handoff**: `true` (static verification per the constraints of this session). The live run is recorded as a known limitation in the Agent Output section and must be re-verified at green phase.

## Test quality standards (ADR 0016)

- **Readable**: Each scaffold uses `try { ... } catch (Exception e) { fail(msg) }` with a message naming the contract that must hold.
- **Maintainable**: Each scaffold uses the shared `TestLogSuppressor` and `@Before` cleanup already established in the test package; no hardcoded fixtures.
- **Isolated**: `SimpleStartupTest` and `StartupCrashTest` reset `ProfilesManager.instance` via reflection in `@Before` and delete the `profiles` dir before each test.
- **Deterministic**: `@Config(sdk = {33})` pins the Robolectric SDK; `ShadowMoonBridge` stubs native loading; no real I/O or network.
- **Atomic**: One contract per test method (`allLayoutsInflateSuccessfully`, `testApplicationOnCreate`, `testUiHelperCrash`).
- **Fast**: No `Thread.sleep`, no retries, no arbitrary waits.

## Handoff back to orchestrator

The red-phase scaffolds are confirmed in place. The Senior Developer may begin implementation, activating one test at a time (Task A → Task B → Task C → Task D). The QA Architect will run the coverage audit (ADR 0019) with Memtrace reconciliation after the green phase is evidenced.
