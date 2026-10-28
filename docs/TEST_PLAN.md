# Test Plan

Status: **PLANNING (2026-10-28). No tests exist or have been run yet.** This plan
defines what will be tested, where (Arena sandbox vs director's laptop), and what
"passing" means, so AI claims stay honest. Terminology: **UNTESTED** /
**SANDBOX-STATIC** / **LOCAL-VERIFIED** (see TDD header).

## 1. Principles

- The sandbox can prove *text and logic*; only the GTX 960M laptop can prove
  *feel, frame rate, driver behaviour, audio and gamepad*. (Split detailed in
  `AI_WORKFLOW.md` §3.)
- No test framework dependency at the start: M1–M3 use zero-dependency scripted
  test scenes + assert scripts runnable headlessly **if/when** a Godot binary is
  available in the sandbox/CI. GdUnit4 or GUT (both MIT, both support headless/CLI
  runs) is adopted later only if hand-rolled asserts become the bottleneck —
  Decision at M3 exit, recorded in the milestone notes.
- Every milestone exit requires: (a) its acceptance checklist run **locally** by
  the director, (b) evidence (log/CSV/short screen recording description) attached
  to the commit/PR, (c) a git tag `known-good/<milestone>-<date>`.
- Failed tests are filed as issues/bug entries with: commit hash, Godot version,
  graphics preset, repro steps (≤5), actual vs expected, log excerpt. The AI never
  "fixes" a bug it cannot reproduce from that report — it asks for the missing log.

## 2. Test levels

### L0 — Static / sandbox checks (automatable, no Godot binary needed)
| ID | Check | Tool |
|---|---|---|
| T-L0-01 | Repo hygiene: no `.zip` asset archives, no `.godot/` cache, file sizes within budget | Python script in `tools/` (created when first needed) |
| T-L0-02 | Asset manifest completeness: every file under `game/assets/` has a manifest row; every row has licence + evidence URL; SHA-256 matches | Python script |
| T-L0-03 | Save/settings schema: sample JSON/CFG fixtures validate against the documented schema; corrupt-fixture handling spec reviewed | Python + code review |
| T-L0-04 | GDScript style/consistency review (naming, no absolute `res://` paths to assets outside manifest, no debug prints left in release paths) | AI review checklist |

### L1 — Headless Godot checks (need a Godot binary: local machine, or sandbox *if* a headless download proves feasible in M0 — not assumed)
| ID | Check | Pass criteria |
|---|---|---|
| T-L1-01 | Project imports cleanly headlessly (`godot --headless --import`) | Exit 0, zero ERROR lines in log |
| T-L1-02 | All scripts parse (`--check-only` style validation / headless scene load of every `.tscn`) | Zero parse errors |
| T-L1-03 | Pure-logic unit asserts: save round-trip (write→read→equal), settings defaults, mission state-machine transitions, upgrade math | All asserts green, log printed summary |
| T-L1-04 | Resource integrity: every `CarDefinition`/`MissionDefinition` loads, referenced scenes exist | Zero missing-resource errors |

### L2 — Physics regression (scripted, local or headless-with-physics)
The physics-regression scene drives the car with **recorded synthetic inputs**
(no human variability) on the test track and logs telemetry CSV.
| ID | Scenario | Pass criteria (tuned once in M1, then frozen as regression bars) |
|---|---|---|
| T-PHY-01 | Launch 0→100 km/h, flat straight | Reaches 100 within target band; no wheelie/spin; top speed within ±5% of definition |
| T-PHY-02 | Emergency brake 100→0 | Stopping distance within band; stays straight (yaw drift < 5°) |
| T-PHY-03 | Slalom at 60 km/h, cones | Completes without spin; lateral-g peaks within band |
| T-PHY-04 | Curb (10 cm) + ramp (20°) + speed bump at 30/60 km/h | No tunnelling, no launch-to-orbit, no stuck state; suspension settles < 1.5 s |
| T-PHY-05 | 60 s mixed circuit, both physics tracks (M1 spike) then winner only | No NaN transforms, no flip without cause; avg physics step time recorded per car (sets the future traffic budget) |
| T-PHY-06 | Reset-car from roof/side/water-edge poses | Car returns upright on road, velocity zeroed, mission state consistent |

### L3 — Performance (local GTX 960M only — sandbox numbers would be meaningless)
| ID | Scenario | Pass criteria |
|---|---|---|
| T-PERF-01 | Benchmark route 60 s, Low preset, 720p | Avg ≥ 60 fps, 1% low ≥ 50 fps (median of 3 runs, plugged-in, warmed up) |
| T-PERF-02 | Worst-view static cameras (harbour overlook, main street) | Draw calls ≤ 250, visible tris ≤ 900k (Performance monitors) |
| T-PERF-03 | 10-minute free-drive soak, district loop | No memory growth trend (VRAM/RAM sampled per minute), no hitch > 100 ms unexplained |
| T-PERF-04 | Cold start → menu interactive; menu → drivable | ≤ 3 s / ≤ 5 s on target laptop (MPD scope) |

### L4 — Gameplay/UX acceptance (director, manual checklist per milestone)
Representative MPD checklist (each milestone gets its own in its doc/PR):
- [ ] Start each of the 3 jobs from its marker; objective text correct; complete each; fail one by timeout; abandon one from pause; restart one.
- [ ] Credits increase by the exact reward; best medal/time saved; quit & relaunch → progress intact.
- [ ] Garage: repaint persists into world; buy upgrades until broke (cannot overspend); locked car cannot be selected until unlocked.
- [ ] Settings: each graphics preset applies visibly; volume sliders affect the right buses; FOV/shake options work; settings survive relaunch.
- [ ] Gamepad: full loop (menu→job→garage) without touching keyboard/mouse; disconnect mid-drive doesn't crash.
- [ ] Edge abuse: drive off map edge / into sea boundary / hold reset / alt-tab during job / pause during countdown — no crash, no soft-lock (a documented recovery exists for each).

### L5 — Export smoke (from first exportable milestone)
Export Linux build with pinned templates → run the *exported binary* (not the
editor) through L4's core path on the target laptop. Editor-only success never
counts as release evidence.

## 3. Bug severity & milestone blocking

- **Blocker** (crash, save corruption, physics explosion, <30 fps Low): milestone cannot exit.
- **Major** (job soft-lock, wrong rewards, camera through world persistently): milestone cannot exit unless director explicitly waives in writing in the PR.
- **Minor** (visual pop-in, audio click, typo): logged, scheduled, non-blocking.

## 4. Evidence storage

`docs/evidence/<milestone>/` holds: benchmark CSVs, physics telemetry CSVs,
checklist results (checked markdown), and a one-paragraph director verdict
("fun / not fun, because…"). Screen recordings are described/linked by the
director rather than committed if large. No evidence folder → milestone is not done,
regardless of code state.
