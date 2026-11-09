# ASTUR | BASELINE COMPARISON V2 | 2026-11-09

**Status:** `EVIDENCE COMPLETE / RECOMMENDATION IS A PROPOSAL`

## 1. Quantitative topology

### main → .13
- .13 ahead: **63 commits**
- `crates/astur/src/main.rs`: **+1237 / -116**
- `crates/astur-settings/src/main.rs`: **+591 / -258**
- `crates/astur-config/src/lib.rs`: **+122 / -41**

### main → .19
- .19 ahead: **102 commits**
- `main.rs`: **+3938 / -275**
- Settings: **+595 / -260**
- config: **+143 / -44**

### .13 → .19
- .19 ahead: **39 commits**
- `main.rs`: **+2693 / -151**
- Settings: **+4 / -2**
- config: **+21 / -3**

### PR #15 versus .19
They are **diverged 4 ahead / 4 behind** in either direction. PR #15 is not a superset of .19.

PR #14 contains the small-utility unmanaged lineage that is present in .19 but is not automatically present in PR #15.

## 2. Candidate A — upstream main `b60500f`

### Strengths
- cleanest upstream lineage;
- least coupling to the layered window-policy/slot/overlay patches;
- easier to define new invariants before importing behavior;
- existing upstream Settings and product features remain available.

### Costs
- highest reimplementation cost for the user-specific window behaviors;
- localization/update work and many later fixes must be selectively reconstructed;
- acceptance coverage from later PRs must be ported rather than inherited.

### Risk
Lower inherited behavioral entanglement, higher scope/cost risk.

## 3. Candidate B — .13 `baee7b6`

### Strengths
- includes the early VI/localization/update lineage and background-spawn protection;
- closer to the currently observed Windows uninstall metadata than .19, although binary mapping is still unproven;
- substantially less overlay/slot complexity than .19.

### Costs
- misses much of the later Window Policy Engine, stable-slot, taskbar recovery, pinned overlay and small-utility behavior;
- still inherits multiple preview-era modifications.

### Risk
Middle ground, but does not remove enough reconstruction work to clearly dominate main.

## 4. Candidate C — .19 `4dedce4`

### Strengths
- most complete release-line implementation of the requested behaviors;
- includes pinned background/foreground-slot work and small-utility unmanaged policy;
- lowest immediate feature-porting cost.

### Costs
- highest accumulated behavior coupling;
- contains the lineage associated with the historic offscreen/park symptom;
- lacks PR #15 reconciliation fixes;
- behavior grew across many draft PR/release branches without isolated desktop acceptance.

### Risk
Highest inherited behavioral/regression risk, lowest short-term reimplementation cost.

## 5. Candidate D — PR #15 head `6994454`

### Strengths
- directly addresses parked activation, minimize successor and overlay/monitor refresh reconciliation;
- CI run 42552634051 succeeded;
- contains useful tests and repair ideas.

### Costs
- diverges from .19;
- is not a release-line superset;
- does not automatically contain PR #14 utility policy;
- has the newly identified native-drag global-state source gap.

### Risk
Good **donor/refuter branch**, poor single source-of-truth baseline.

## 6. Candidate E — selective reconstruction

Definition:
- choose a verified base;
- port only approved product behavior and tests;
- treat later PRs/tags as evidence and donor patches, not as a linear feature stack.

### Strengths
- maximum control over invariants and provenance;
- can preserve valuable upstream features without inheriting every experimental branch interaction;
- supports explicit feature-to-test traceability.

### Costs
- requires disciplined parity work;
- easy to miss small behavior unless the GUI/control and acceptance manifests are complete.

## 7. Recommendation

**PROPOSAL:** use **upstream main as the V2 implementation base**, with selective reconstruction from .13/.19/PR13-15 after product approval.

Reason:
- the user's intent is now explicit enough to reimplement behavior without using current implementation as the contract;
- .19 carries the most entangled window-lifecycle history;
- .13 does not reduce reimplementation enough to justify inheriting preview-era complexity;
- PR15 is best used as a test/fix donor, not the base;
- the GUI manifest protects against accidentally losing upstream features when rebuilding from main.

This recommendation is not permission to fork or implement. Approval of `ASTUR_CONTRACT_V2.md` remains the gate.

## 8. Donor policy if main is approved

Use later refs only in these roles:
- **tests/acceptance donor:** PR #8-#15;
- **behavior examples:** .18/.19;
- **utility signatures:** PR #14/.19;
- **park/focus repair evidence:** PR #15;
- **localization/catalog reference:** .1-.13;
- **installer/rollback lessons:** release branches;
- **never** cherry-pick a large behavior patch merely because its CI is green.

Every imported behavior must trace to one approved contract ID and one fresh test.
