# Astur: Independent fullscreen and transient media windows — Execution Plan (2026-10-30)

Status: IMPLEMENTED IN SOURCE; WINDOWS CI PENDING. Baseline feat/vi-full-update-popup-v2, clean at 8c92131 before edits. Preview target 2.4.0.7; release must remain gated by Windows fmt/Clippy/tests/install smoke. All desktop E2E states explicitly UNVERIFIED until observed.

## Contract / scope
- One opt-in checkbox in Settings > Windows & Rules: preserve native maximized (Windows square button), F11/borderless fullscreen, and transient photo/video popup windows. Default OFF for upgrade safety.
- A protected maximized/fullscreen main window MUST NOT be inserted in Astur's tiled/tab/floating registries, resized, unmaximized, or hidden by workspace management. On user restore-down/minimize, eligibility is reevaluated and the window may reenter ordinary Astur management. If the user returns it to fullscreen, it becomes independent again.
- Media viewers and PiP popup surfaces should retain native geometry, visibility, animation, viewer navigation, and OS normal z-order. Exclude owned/tool/noactivate window surfaces already handled plus strongly identified unowned popup surfaces; do NOT blacklist a whole process or ignore every Chrome/Telegram/Zalo window.
- Z-order follows normal Windows focus per HWND. Example tiled A+B, independent fullscreen F: selecting B raises only B above F; A stays below F. Switching to F raises F normally. No TOPMOST global elevation, never bring the whole tiled group forward or change topology on popup refresh.
- Home header language chooser near top-right Undo/Status as compact EN/VI menu, only alternate locale in dropdown. Remove left-sidebar language selector, preserving language file and write-error semantics.
- Preserve existing 819-entry Vietnamese translation, config and user unrelated work; no live install or desktop alteration while testing.

## DAG (single writer)
A baseline & read existing callbacks/config/UI + safety
B config parser/serialization/default/reload groups + roundtrip tests (after A)
C Settings checkbox/header language + UI tests (after B)
D WM state transitions: protect newly/maximized, untrack managed on maximize without restore, re-adopt after restore/minimize; protect popup surfaces and z-order invariants, plus synthetic tests (after B, design informed by A)
E integrate/review/reconcile lifecycle, startup/reload and 2-monitor edge cases (after C,D)
F fresh Windows CI fmt/Clippy/unit tests/release build; visual EN/VI renders; avoid release before green (after E)
G checkpoint, commit, push; publish prerelease only if F PASS and packaging safe. Real-world media popup/F11/maximize tests need observed HWND/desktop so mark explicitly UNVERIFIED if unavailable.

## Acceptance and safety
- OFF is old behavior; ON protects maximize/fullscreen; a restored normal main window reenters tile management; no phantom duplicate entries, lost HWND on destroy, or managed window restoration on fullscreen.
- Open/close/next image/video popup does not alter tiled main windows' geometry/count.
- OS focus/z-order only per window, normal app windows on same process remain tiled.
- Mixed displays, existing fullscreen before Astur starts, on/off live reload, minimize/re-show, workspace switching and animation cancellation covered where verifiable.
- Fresh Windows machine evidence after final change required to claim PASS. If real Zalo/Telegram media popup HWND is not observed, do not claim its E2E fixed.
