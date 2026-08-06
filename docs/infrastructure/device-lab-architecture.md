# Device Lab

This document describes the device lab used to validate CandelaMoon on Android TV hardware, the compatibility tier for older Android versions, the fault-injection harness used to verify resilience, and the runner infrastructure (self-hosted containers, device runners, and the Windows host) that executes the pipeline.

## Google TV Streamer

The Google TV Streamer is the primary reference device: it is the hardware we test against first, the baseline for performance and resilience behavior, and the device on which the release validation suite must pass before any release ships.

- **Model**: Google TV Streamer (4K), current-generation Streamer hardware, used as the device-lab reference.
- **Firmware**: Android 14 (API 34), current production firmware as shipped by Google. The reference device is kept on the shipping production firmware; preview builds are not flashed on it.
- **ADB connection**: Network ADB is the primary transport (`adb connect <device-ip>:5555`). The Streamer has no USB data port, so USB ADB is not used for this device; TCP ADB is enabled over the dedicated device-lab LAN (see Windows Host for the LAN topology). Each runner pairs to the device once per job and tears the pairing down afterwards.
- **CI trigger**: Release-validation workflows dispatch a `device-test` job with label `device-tv`. The job powers the Streamer via a mains-controlled smart PDU (power off/on), waits for boot completion via `adb wait-for-device` plus the boot-completed property, installs the APK with `adb install -r`, and runs the instrumentation suite (`connectedAndroidTest`) plus the smoke scenario suite.
- **Artifact capture**: Every device job captures `adb exec-out screencap -p` screenshots at defined checkpoints and `adb logcat -d` (buffered to file) on failure and on teardown. Screenshots, logcats, and `dumpsys` outputs are zipped per scenario, uploaded with a stable naming scheme (`device-<serial>-<scenario>-<timestamp>`), and posted to the evidence pipeline as build artifacts alongside the test report.

## Compatibility

The API 28-30 tier guarantees CandelaMoon works on older Android TV hardware that cannot run API 31+. This tier runs a reduced test set (core journey only) because full-suite runs on emulators are slow and the tier's purpose is compatibility, not feature regression.

- **Emulator configurations**: three emulator profiles are provisioned as named AVDs: `api28-tv` (API 28, Android TV image), `api29-tv` (API 29), and `api30-tv` (API 30). Each runs with software rendering (no GPU passthrough in CI) and 2 GB RAM, matching low-end TV hardware.
- **Hardware requirement**: at least one representative physical device in this tier must be present before public release — an older Android TV device running API 28, 29, or 30 — to catch emulator-vs-hardware divergence (codec support, Wi-Fi latency, display quirks) that emulators cannot represent. The lab will acquire one such device before the release candidate phase; until then the tier is emulator-only and release is blocked on this item.
- **Boot/snapshot strategy**: emulators boot cold at the start of the compatibility job and are snapshotted after first boot. Subsequent runs restore from snapshot (`-snapshot-load`) to cut boot time. Snapshots are invalidated when the AVD system image or kernel changes; a cold boot is forced at least once per week to verify snapshot fidelity.
- **Test selection**: the API 28-30 tier runs only the core journey: install, launch, first-run setup with PIN, connect to a test host, stream a short session, and graceful teardown. The full regression suite runs exclusively on the Google TV Streamer reference device. Compatibility failures on emulators are triaged by the platform team and require a decision (fix vs. documented known divergence) before release.

## Fault Injection

The fault-injection harness (`scripts/fault-injection/`) verifies that CandelaMoon degrades gracefully and recovers when its environment misbehaves. Each fault is executed on the reference device against a controlled test host, and the app must exhibit the expected behavior, recover, and produce evidence. The 13 fault types split into host faults, network faults, pairing faults, media faults, and lifecycle faults.

| # | Fault | Trigger method | Expected behavior | Recovery verification | Evidence capture |
|---|-------|----------------|--------------------|------------------------|------------------|
| 1 | Host offline | Stop the test-host service; confirm the host LAN IP is unreachable from the device | App shows a disconnect state; no crash; user-visible retry affordance | Restart the host; app reconnects without relaunch within the retry timeout | logcat disconnect+reconnect window, screenshot of error UI |
| 2 | Host reboot | Reboot the test host mid-session | Session marked ended; app returns to idle/home state | Post-reboot the app relaunches cleanly and can start a new session | boot-time logcat, screenshot of home state |
| 3 | Network loss | Drop traffic between device and host via `tc`/`iptables` rules in the host's network namespace | Stream stalls or ends with an explicit error; no hang, no crash | Remove the rules; session re-establishes after the error clears | packet-loss window, logcat of stall/error, screenshot of error state |
| 4 | Certificate mismatch | Serve the test host with a self-signed certificate not in the trust store | App refuses to connect; certificate error surfaced to the UI | Install the correct certificate; connection succeeds on retry | logcat TLS error lines, screenshot of error UI |
| 5 | Invalid PIN | Submit a deliberately wrong PIN at pairing | Pairing rejected with a retry prompt; no lockout panic | Enter the correct PIN; pairing succeeds | logcat pairing attempt log, screenshot of retry prompt |
| 6 | Pairing conflict | Attempt a second concurrent pairing from a different client while a session is active | Second pairing rejected or queued; first session unaffected | Terminate the rogue client; new pairing succeeds | logcat of both clients, screenshot of conflict UI |
| 7 | Busy session | Start a new session while the existing session is still active | App refuses with a "session in progress" state; no session takeover | End the active session; new session starts cleanly | logcat session-state transitions, screenshot of busy-state UI |
| 8 | Unsupported codec | Configure the test host to stream a codec the device lacks | Fallback negotiation or a clear "unsupported media" error; no decoder crash | Stream a supported codec; playback succeeds | logcat codec negotiation, screenshot of fallback/error UI |
| 9 | Unsupported HDR | Force an HDR stream (e.g., HDR10+) on the non-HDR display path | Graceful fallback to SDR or an explicit unsupported-HDR message | HDR-capable stream plays correctly after fallback | logcat HDR negotiation lines, screenshot |
| 10 | Decoder failure | Induce a decoder error by corrupting the stream mid-playback (test host sends malformed packets) | App recovers with error UI or automatic retry; no hard crash | Subsequent valid stream plays; process stays alive | logcat decoder error + recovery, `dumpsys media` state |
| 11 | No artwork | Test host returns success with empty/null artwork metadata | App renders a placeholder; no NPE/crash | Artwork present on the next load | logcat null-metadata handling, screenshot of placeholder |
| 12 | Malformed response | Test host returns truncated/JSON-invalid responses for key API calls | App validates the response, shows a graceful error, does not crash | Valid response accepted on the next attempt | logcat parse-error handling, screenshot |
| 13 | Low-memory recreation | Trigger memory pressure via `adb shell am send-trim-memory` / `am kill` while the app is backgrounded | App restarts to the previous meaningful state without data loss; no blank screen | Post-recreation state verified via saved state | logcat of kill + recreation, screenshot of restored state |

Every fault run produces a per-fault evidence bundle (logcat, screenshots, dumpsys) uploaded under `fault-injection/<fault-id>/`. A fault that crashes the app, hangs longer than 30 s, or fails recovery verification is a release-blocking failure.

## Self-Hosted Runners

CandelaMoon runs GitHub-hosted runners for ordinary build and unit-test jobs, and self-hosted runners wherever real hardware or special networking is required.

- **Label-to-capability mapping**:
  - `container-linux` — Podman container jobs (Ubuntu 24.04 host, rootless Podman). Used for build, unit tests, SBOM, and vulnerability scans.
  - `device-tv` — jobs that talk to the Google TV Streamer reference device over network ADB.
  - `device-emu` — emulator jobs for the API 28-30 compatibility tier.
  - `windows-host` — the Windows runner that executes the LuminalShine integration suite.
- **Runner OS**: container and device runners run Ubuntu 24.04 LTS; the Windows runner runs Windows 11 (see below).
- **Self-hosted vs GitHub-hosted**: GitHub-hosted runners handle anything needing no hardware access (pure builds, lint, unit tests, scans). Self-hosted runners are used only where the job needs a real device, emulators on a controlled host, or the Windows/LAN setup. This split keeps the self-hosted fleet small and auditable.
- **Security posture**: self-hosted runners are ephemeral with respect to jobs — every job runs in a fresh workspace, no persistent secrets are stored on any runner (credentials arrive per-job via GitHub Actions and are scoped to the job), runners are firewalled to the device-lab LAN with egress restricted to what the pipeline needs (GitHub, package registries, the test host), and runner registration tokens are rotated on reinstall. Device/container runners are re-imaged weekly.
- **Podman invocation**: container jobs use rootless Podman (`podman run --userns=keep-id` on the `container-linux` runner). Podman is used rather than Docker for rootless-by-default execution: images are referenced by digest, pulled through the registry proxy, and run with `--read-only` rootfs where possible, never `--privileged`, and `--cap-drop=ALL` with only the required capabilities re-added.

## Windows Host

The Windows host runs the official LuminalShine integration tests, which require the LuminalShine client and its media-stack behavior on Windows.

- **OS and runner**: Windows 11 (23H2 or later), registered as a self-hosted runner with the `windows-host` label only.
- **LuminalShine install/config**: LuminalShine is installed to a fixed path (`C:\LuminalShine`) at the release version pinned in the workflow (`LUMINALSHINE_VERSION` input). Configuration (endpoint, ports) is generated per job from the `luminalshine.toml` template; the install directory is re-verified per run and re-installed from the pinned installer artifact when the version changes.
- **Network path to device**: the Windows host sits on the same LAN as the Google TV Streamer (device-lab VLAN). The Streamer reaches the LuminalShine host by IP over unicast; multicast discovery is stubbed. Firewall rules on the Windows host allow only the device-lab subnet on the streaming ports.
- **Streaming test validation**: the integration suite drives a full end-to-end stream: CandelaMoon on the Streamer pairs with the LuminalShine host over the LAN, starts a real playback session, and the suite verifies stream lifecycle (start, render, stop) plus error paths (host stop mid-stream, codec negotiation with LuminalShine's default profile). Evidence (screenshots, host-side logs, device logcat) is uploaded to the evidence pipeline like any device test.
- **Difference from containerized Linux runners**: unlike `container-linux` jobs (ephemeral Podman containers, disposable state, headless), the Windows host is long-lived, has a fixed install, and exercises the real Windows networking stack against real hardware. It is consequently the least disposable runner: any change to it goes through the runner-update checklist (installer hash verify, config diff, smoke stream), and it never runs jobs other than the LuminalShine integration suite.
