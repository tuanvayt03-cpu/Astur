# Astur notification + mouse input recovery execution plan

Date: 2026-11-02
Owner/integrator: one CodeLocal writer
Baseline: `fix/zalo-notification-maximize-input` at `b79b9e7`, working tree clean
Release: 2.4.0.11 preview (`ef970ea`) remains UNVERIFIED for live mouse blocking

## Scope / evidence
- User reports a notification remains at monitor top and prevents clicks in the screen region beneath. Screenshot says "Cộng đồng: Hội Kín"; this might be Facebook/Chrome notification, **not proven Zalo**.
- CodeLocal accessible RDP session does not expose Astur or Zalo processes; not the verified failing session.
- Owned: `crates/astur/src/main.rs`, `scripts/capture_zalo_click_blocker.py`, corresponding targeted tests, this plan/handoff and CI test invocation.
- Preserve: installed Astur, system mouse state, notification app windows, existing config, backups, unrelated repo files and release tags.

## DAG / critical path
A. Inspect existing Win32 hook / popup rejection and baseline (read-only)
  -> B. Add read-only process-agnostic HWND, DWM frame and hook reason evidence
  -> C. Fix any **demonstrable** input swallowing defect (e.g. stale menu HWND post failure)
  -> D. Fresh Python smoke / Rust fmt + tests + clippy + build (GitHub Windows CI)
  -> E. Review diff, checkpoint commit, push, record terminal state
  -> F. Run real notification reproduction in the affected Windows desktop + A/B with Astur off/on (external hardware dependency)
  -> G. Only after F and passing packaging gates, release a new reversible preview installer.

Parallel read-only lane: compare Windows docs, current diagnostic scripts and similar WM ignore rules.
Critical path: B -> C -> D -> E -> F -> G. F is NOT satisfied by CI or screenshot alone.

## Acceptance criteria
1. Diagnostic capture names the **actual notification owner**, can identify an app's invisible input shield even if the visible DWM frame is smaller; no screenshot or message/title collection.
2. Low-level mouse hook diagnostics report exact swallow reasons at debug level without allocating, locking or disk I/O in the hook. Ordinary clicks must pass through when dismissal target HWND is stale / message cannot be posted.
3. Unit tests cover reason labels and stale-post policy. Python self-test, --smoke and syntax pass.
4. Windows CI `cargo fmt --all --check`, `cargo clippy --workspace --all-targets -- -D warnings`, `cargo test --workspace`, `cargo build --release --workspace` PASS **after final changes**.
5. Real acceptance requires target desktop toast origin + 20+ underlying click/scroll actions, monitoring popup position, mouse capture and NCPC fullscreen. No claim of final fix until that evidence exists.

## Safety and recovery
- No global `WS_EX_TRANSPARENT` changes, `ClipCursor` writes, `ReleaseCapture`, mouse injection, arbitrary HWND moving, killing apps, installer deployment, PR merge or force push.
- No deployment to installed Astur until real E2E proves the owner and behavior.
- One writer, one scoped branch; save a commit / exact SHA and clean git status at checkpoint.
- Diagnostic hook reason counters are active only when Astur's log level is `debug`, published via existing watchdog counters. They distinguish swallowed input from hit-test shields without logging coordinates or message text.
- Read-only probe now compares Win32 window/input rectangles to DWM visible frame bounds. A minimized/absent DWM frame is recorded as null.
- If real session inaccessible: terminal status for the **whole live-fix objective** is BLOCKED while code-level diagnostics may be completed and verified.
