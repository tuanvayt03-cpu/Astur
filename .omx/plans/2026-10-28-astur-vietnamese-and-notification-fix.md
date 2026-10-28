# OMX Execution Plan — Astur Vietnamese + Notification Popups

Date: 2026-10-28 · State: PLANNED (fork complete; code changes not yet completed)
Owner: one primary integrator/writer · Upstream: Page011/Astur
Fork: https://github.com/tuanvayt03-cpu/Astur · Baseline: b60500f0155c1d817936b869989718299cbd3f14 · Main: unchanged
References: docs/vi/SDD.md and docs/vi/CONTRACT.md.

## Target
Fork Astur 2.4.0 and create a maintainable bilingual English/Vietnamese version with near-complete first-party localization, preserving upstream updateability. Fix improper adoption/tiling/tab grouping of transient notifications and overlays including Telegram, Zalo, Windows notifications and screen-capture toasts, without ignoring their normal application windows.

## Baseline evidence
- Cargo workspace: crates/astur (native Windows manager/launcher/status bar/tray), crates/astur-config (config), crates/astur-settings (egui GUI) [Cargo.toml; CLAUDE.md].
- Hundreds of user-facing strings are inline in crates/astur-settings/src/main.rs, including GUI labels/tooltips. Action protocol names and English labels share arrays in crates/astur-config/src/lib.rs [main.rs:1800+, config lib.rs:298+].
- No established i18n subsystem observed in inspected source; no Language selector in settings source.
- Notification risk: crates/astur/src/main.rs:4994-5034 BLOCK_CLASSES, 5042-5150 app_surface_reject / app_window_reject / manage_reject, with checks for WS_EX_TOOLWINDOW, WS_EX_NOACTIVATE, owner, title, ignore rules. Some third-party toast surfaces may pass these checks. Do NOT blindly block whole framework classes or app exe. Current root cause remains UNCONFIRMED until HWND metadata and reproduction are captured.
- Windows upstream CI: cargo fmt --all --check; cargo clippy --workspace --all-targets -- -D warnings; cargo test --workspace; cargo build --release --workspace [.github/workflows/ci.yml].
- Upstream code guidance prohibits Win32 input-hook blocking and requires updated plan/ docs alongside changes [CLAUDE.md; CONTRIBUTING.md].

## DAG — gates and dependencies
G0 Baseline [required]: verify fork upstream commit, Git status, toolchain and clean builds; preserve existing Astur installation/config. Collect event evidence of Zalo/Telegram/screenshot transient(s): HWND, process/exe, class, styles/exstyles, owner/parent, title, visibility, cloaking, lifetime and exact event path. Reproduce with 1, 2, 4, 6 tiled normal app windows and notification screenshots.
G1 Specs [G0]: classify all visible strings by surface and translatable/external/protocol; glossary and persistent locale design; confirm notification defect mechanism with traces and failing regression tests.
G2 Localization engine [G1]: add small pure-Rust i18n boundary with en/vi catalogs, typed keys or verifiable key manifest, placeholders, fallback and locale preference; no locale call in hooks; avoid changing astur.conf semantics.
G3 Parallel independent work [G2]: (A) Settings/pages/validation/help/search; (B) WM shell status/launcher/tray/menu; (C) read-only translation+Unicode visual QA.
G4 Notification fix [G1]: fix eligibility at the narrowest safe pre-adoption point based on captured window signature. Never blanket-ignore Zalo.exe, Telegram.exe, ApplicationFrameWindow, WinUIDesktopWin32WindowClass, Chromium classes or Windows-owned main app windows. No global suppression of notification delivery.
G5 Integration [G3,G4]: one primary integrator; reconcile shared catalogs and config, update upstream plan/ architecture notes and release docs.
G6 Fresh validation [G5]: fmt/clippy/test/release build; EN/VI rendered screenshots at common DPIs; complete transient-window matrix and manual Windows desktop regression; no missing keys, broken buttons, windows orphaned on exit.
G7 Release [G6]: separate installer/package identifying fork, clean upgrade/rollback, LICENSE/third-party notices, checksums, CI evidence, GitHub release/tag, recovery handoff. No production replace until smoke tested.

Critical path: G0 → G1 → G2 → G3/G4 → G5 → G6 → G7. G3 and G4 may progress in isolation but must not modify the same source file concurrently. The shared tree has exactly one primary writer.

## Dispatch contracts
Investigation: Goal reproduce notification tab grouping; Evidence screenshot plus HWND/style/exe/event trace; Autonomy read-only; Boundaries no changing notification settings or running live manager on current desktop without separate isolation; Verification failing test and reproducible trace.
Localization: Goal cover every owned string, EN/VI toggle; Evidence inventory and fixture snapshot; Autonomy edit scoped i18n/settings files; Boundaries preserve config identifiers and hooks; Verification key/placeholder equality, cargo checks, screenshot comparison.
Notification implementation: Goal filter transient surfaces only; Evidence discriminating HWND predicate, repro; Autonomy scoped source+tests; Boundaries app main windows remain tiled, no broad class/exe exemptions; Verification both false-positive and false-negative test cases, live OS smoke.
Integration/QA: Goal prove merged system; Evidence diff, CI, desktop manual case matrix; Autonomy tests/review only until primary writer reconciles; Boundaries no destructive operations; Verification fresh after final change.

## Milestones and blockers
M0 FORKED: GitHub fork created and verified, no implementation claim.
M1 SPEC_READY: baseline + notifications reproduction + string inventory + documented design.
M2 ENGINE_READY: EN/VI catalogs and locale persistence test pass.
M3 FEATURE_READY: Settings, WM and notification filter implemented in branch.
M4 QA_PASS: all CI+manual checks passed on final commit.
M5 RELEASED: independent downloadable installer and exact SHA/recovery point.

Hard blockers only: unable to identify safe transient vs app windows with evidence, missing required runtime privilege for reproducible test, or integrity/destructive risk. If blocked, leave explicit exact checkpoint. No blind retries, no false PASS.
