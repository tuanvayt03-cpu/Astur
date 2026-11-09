# ASTUR V2 | Redesign review package | 2026-11-09

**Status:** `REVIEW COMPLETE / APPROVAL-READY / IMPLEMENTATION NOT STARTED / LIVE DESKTOP UNCHANGED`

This directory is the source-controlled checkpoint for the Astur redesign review. It replaces the earlier assumption that the 70-row feature register was a complete product contract.

## Fresh baseline

- upstream `main`: `b60500f0155c1d817936b869989718299cbd3f14`
- update `.13`: `baee7b6784e0a6875dabc12cfa1a6f9ff01027ea`
- update `.19`: `4dedce4569364211264775cf89bdab2ebf93ec9a`
- PR #15 head: `69944546258e30bd9de761803999e9767dbf0101`
- PR #14 head: `126cd9ecf550941dd8e1819a985ab01c7b39f8de`
- local checkout observed during review: `release/astur-vi-update-2.4.0.12`, clean, HEAD `a3fee3807373be0b1d07e5fff319d06bc72d41fe`

Remote topology was fetched again before this package was written. PR #1-#15 remain open; #1 is non-draft and #2-#15 are draft. No PR is merged. The 16 VI update tags remain `.1, .2, .5, .6, .8, .9, .10-.19`.

## Critical corrections

1. CS1 full-screen background is a user requirement **inside the described overlay mode**, not an optional feature to vote away.
2. Empty-slot-first and then N-1 non-focused replacement is also a user requirement inside that mode.
3. `1/2/4/5` must not be inferred from `scroll_default_width` or current `pinned_slot_count`; visible geometry must be approved explicitly.
4. The 70-row register is a feature-family inventory, not a complete control manifest.
5. Seven Settings groups, a clean fork, and one centralized state machine are proposals until approved, not facts.
6. PR #15 and release `.19` diverge 4/4; PR #15 is not a superset of PR #14/`.19`.
7. CI success is not desktop acceptance.
8. Historic runtime trace still proves a foreground, visible, non-minimized Telegram HWND could remain physically parked offscreen. Exact live binary-to-source attribution remains unknown.

## New engine finding

The redesign audit found one additional **CONFIRMED_SOURCE_GAP** in PR #15 lineage:

- Native move state is globally stored in `NATIVE_DRAG*` atomics.
- `EVENT_SYSTEM_MOVESIZEEND` uses `NATIVE_DRAG.swap(0)`.
- If a delayed END for HWND A arrives after START for HWND B, END(A) can clear B's active drag context. The later `source == h` check prevents A from being treated as B's move, but it does not restore B's context.
- Runtime occurrence is unproven; the source race is real and requires a fail-first event-order test before implementation.

See `WIN32_ENGINE_AUDIT_V2.md`.

## Documents

- `PRODUCT_INTENT_V2.md` — corrected user intent, source evidence, hypotheses and genuinely open decisions.
- `WIN32_ENGINE_AUDIT_V2.md` — event/lifecycle audit and the four R2 hypotheses.
- `GUI_CONTROL_MANIFEST_V2.md` — 14-page control-surface manifest and parity requirements.
- `BASELINE_COMPARISON_V2.md` — main vs .13 vs .19 vs PR15/PR14 evidence and future-base ranking.
- `ASTUR_CONTRACT_V2.md` — behavior contract, state/event truth table, acceptance matrix and decision register.

## Safety and release boundary

This package makes **no runtime change**. It does not install or restart Astur, does not run a second window manager, and does not interact with MT5, SignalOps, Chatwoot or private user windows.

A future V2 implementation may start only after the product decisions in `ASTUR_CONTRACT_V2.md` are approved. A future release may not be promoted until isolated Windows desktop acceptance passes in addition to code CI.
