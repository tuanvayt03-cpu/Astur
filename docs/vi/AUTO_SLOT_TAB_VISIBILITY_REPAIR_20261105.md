# Astur scrolling: Auto Slot Stack / Manual Tab / Physical Reveal repair

Date: 2026-11-05. Execution baseline: released 2.4.0.15 at `507be759e81c06fe04a122c9d7c6dd8313e5e114`. Isolated branch `fix/astur-auto-slot-separate-20261105` in `D:\Project\Astur-auto-slot-repair-20261105`. Existing user desktop, 2.4.0.15 release, PR #9 and unrelated worktrees are preserved.

## Diagnosis

1. `Cmd::Add` called `col.tabbed = true` whenever a visible viewport was full. It therefore bypassed the documented explicit `Alt+Shift+T` manual tab toggle and displayed an unsolicited black Astur tab bar above Explorer. `tabbed` was overloaded with two meanings: "overflow slot holds multiple occupants" and "user explicitly enabled tab presentation".
2. When a column had only one member, manual tab metadata could remain, and `tab_bars_build` did not independently refuse to draw a singleton.
3. `Cmd::Focused` pre-set `ws.focused = h`, then `strip_reveal` asked `tile_slot()` for a future layout classification, returned `Vis::Full`, and skipped placing the HWND that was physically parked off the virtual desktop. Several taskbar clicks were sometimes needed to re-enter a path that actually retiled.
4. `Manager::insert_window` performed `ensure_visible` before the auto slot member and presentation were committed. The later offset correction could not undo a premature focus/scroll side effect.
5. `Cmd::TabClick` built its tab index using `tiled_windows` (minimized HWNDs removed), but the tab UI was built from `scroll_layout_windows` (minimized HWNDs reserved). Mixed lists could address a wrong tab after minimize.

## New contract / decisions

- **Manual Tab**: only `toggle_tabbed` (`Alt+Shift+T`) sets `ColMeta.tabbed` and may draw Astur's tab bar. With only one member, no bar is painted or vertical space reserved, even if manual tabbed metadata is set.
- **Automatic Slot Stack**: when no free column fits, a new window occupies the previous N-1 or other non-anchor column as the shown member, and the older occupant remains a managed, taskbar-recoverable window; `ColMeta.auto_stack` is separate from `tabbed`. No Astur tab bar, no fake new workspace, and no synthetic minimize. A singleton ceases to be an automatic stack.
- Manual ON/OFF clears automatic state; turning manual Tab OFF returns to ordinary stacked geometry, not a second hidden auto mode.
- Layout uses shared rectangle for either manual tab or automatic stack, but reserves the title/bar region **only** for manual tab. The bar builder additionally checks manual state and >=2 members.
- Admission in an explicitly selected slot must not preemptively recenter. Preserve existing focused slot offset until all placement metadata is committed; legacy scrolling reveal is retained only for fallback admissions where no policy slot was found.
- Revealing a previously hidden/parked occupant requires a real retile/unpark even if predicted layout geometry reports Full. Detect stale last-visible slot, physical parked position and Astur-owned active-workspace SW_HIDE. Never unhide an app's intentional hide or a scratchpad. Preserve a bounded guard for the immediate synthetic focus echo of a new admission.
- `TabClick` must use the same minimized-placeholder window list as the rendered tab UI. Minimized windows keep slot geometry, without being physically placed until restore.
- Hidden workspace activation retains switch-before-restore order to avoid showing windows on the wrong workspace.

## DAG and evidence

P0 source baseline / ownership: clean release branch, new isolated worktree; no existing primary writer in this target.
P1 split state: `ColMeta.auto_stack`, manual `tabbed`, geometry and tab-bar visibility.
P2 physical reveal: parked/owned-hide checks, correct manager retile, no premature admission recenter, minimized restore order.
P3 regression tests: implicit overflow (A focus -> C in B slot; B survives); single Explorer no tab bar; explicit tab toggle; one-click parked activation model; pure geometry; normal/manual behavior.
P4 Windows CI: rustfmt, Clippy -D warnings, all Rust tests, Settings VI/EN, release build; no pass before fresh evidence.
P5 optional prerelease preview/installer only after clean CI plus in-place/rollback smoke, never overwrite 2.4.0.15 or silently install.
P6 desktop E2E gate: **PENDING** until physically observed on user's one/two-monitor Windows session with disposable windows; do not touch active MT5 or Zalo unless explicitly safe. Includes opening CS3 while CS1/CS2 in different anchor slots, 1/2, 1/4 and 1/5 widths, taskbar once, minimize/restore, drag, top-edge maximize and exit/rescue.

## Security and recovery

Single primary writer, no destructive changes, no forced Git operations, no run of second WM alongside installed instance. Keep logs free of secrets and account data. Use source CI and package smoke as separate evidence from live UX. If runtime QA exposes a defect, fix on this branch and fresh verify before stable promotion. Status, branch SHA, CI, PR and remaining gates are updated after verification.
