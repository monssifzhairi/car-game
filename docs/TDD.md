# Technical Design Document — Zero-Budget AI Car Game

| Field | Value |
|---|---|
| Working title | **CAP SIROCCO — Open Road** (working title only; trademark-check before any public release) |
| Status | **PLANNING — awaiting director approval. Nothing in this document is implemented or tested yet.** |
| Date | 2026-10-28 |
| Engine | Godot 4 (exact patch version to be pinned in Milestone 0 — see Decision D-03) |
| Target machine | Kali Linux laptop, NVIDIA GTX 960M (Maxwell) |
| Budget | 0 DH — CC0 / MIT assets only, no paid services, no paid APIs |
| Repo state at planning time | Empty except `README.md` (verified 2026-10-28). Godot is **not** installed in the Arena cloud sandbox (verified: `which godot` returns nothing). |

Evidence discipline used throughout the project: work is labelled **UNTESTED**,
**SANDBOX-STATIC** (text/logic checked in the cloud sandbox only), or
**LOCAL-VERIFIED** (run by the director on the real GTX 960M machine, with commit hash).
No claim of "it works" is allowed without the third label.

---

## 1. Game concept (original, no copied branding/IP)

**One-liner:** a stylised low-poly open-world *driving* game on a small fictional
Moroccan Atlantic coastal enclave — a port town, a coastal ring road, and scrub
hills — where you earn a living (and better cars) as an all-purpose wheel-for-hire:
courier runs, timed checkpoint sprints, and scenic discovery.

- **Setting:** fictional "Cap Sirocco" — inspired by Atlantic-coast Morocco (light,
  whitewash-and-blue palette, palm-lined corniche, kasbah-like old town massing) but
  an invented place with invented names. No real car brands, no ripped map, no
  assets, names, or UI from any existing game.
- **Fantasy:** freedom of the open road in a place that is small enough to master,
  in cars you improve over time. Not crime, not weapons, not on-foot gameplay.
- **Why car-only is a deliberate scope decision:** removing an on-foot character
  removes character animation, interiors, combat, and pedestrian simulation — the
  four most expensive systems in open-world games — and lets 100% of effort go to
  driving feel, which is the product.
- **Core loop (5-minute sessions):** free-drive → accept a job at a job board
  marker (delivery / checkpoint run / photo spot) → drive it against the clock →
  earn credits & reputation → garage: repaint, upgrade (engine/grip/brakes tiers),
  unlock the next car → bigger/faster jobs.
- **Art direction:** flat-shaded low-poly, single warm directional light, fixed
  "golden afternoon" default. This is chosen to match CC0 asset availability and
  GTX 960M performance, not as a compromise narrative — consistency beats detail.

### Design pillars
1. **Driving feel first.** If one car on a flat greybox isn't fun, nothing else ships.
2. **Small and dense beats big and empty.** ~1 km × 1 km island, every road earns its place.
3. **60 fps on the director's GTX 960M at Low preset** is a feature, not a hope (see `PERFORMANCE_STRATEGY.md`).
4. **Every asset traceable.** CC0/MIT only, recorded in the asset manifest before import.
5. **Small testable milestones.** Each ends with a known-good tag the director has run locally.

### Explicitly NOT in any demo scope
On-foot mode, multiplayer, police/pursuit AI, pedestrians, car deformation damage,
interior cockpits, dynamic weather, day/night cycle simulation, story cutscenes,
licensed/branded cars or music, in-game economy beyond credits-for-upgrades.

---

## 2. Minimum Playable Demo (MPD) — "Demo v0.1"

The smallest thing that proves the pillars and is fun for 15 minutes:

| Area | In MPD |
|---|---|
| Map | One district of the island (~800 m × 800 m playable): town grid + short coastal road + one hill road. Parked cars and props for life; no moving traffic. |
| Cars | 1 hero car with excellent tuning + 1 unlockable second car (different `CarDefinition` stats and mesh). |
| Driving | Arcade-reliable physics, keyboard + gamepad, chase cam + hood cam, handbrake drift-lite, reset-car, reverse. |
| Missions | 3 jobs on one data-driven system: 1 delivery, 1 checkpoint sprint, 1 photo/discovery run. Bronze/silver/gold times, credit rewards. |
| Garage | Static preview rig: switch unlocked car, repaint (body colour swatches), buy 2 upgrade tiers (engine, grip) that modify the car definition at runtime. |
| UI | Main menu, pause, settings (graphics preset, resolution scale, volumes, camera FOV), HUD (speed, job timer/objective, credits), simple job-complete screen. Minimap is a *stretch* item, not committed. |
| Audio | Engine loop (pitch by RPM proxy), skid/wind-lite if assets verify, UI clicks, job jingles. All CC0 per-file verified. No radio music in MPD. |
| Save | Settings persist; progress persists (credits, unlocks, best times). Versioned save schema. |
| Performance | Low/Balanced presets; Low targets 720p60 on GTX 960M (acceptance measured, § Test Plan). |

**MPD exit criteria:** director completes all 3 jobs in one sitting on the local
machine at Low preset, no crash, no physics explosion, save survives restart,
frame-time log captured for the benchmark route.

## 3. Long-term expansion plan (each stage gated, none pre-committed)

| Stage | Adds | Gate to enter |
|---|---|---|
| Alpha (v0.2–0.3) | Full 1–2 km island in 4–9 chunks, spline coastal/highway roads, 4–6 cars, 10–15 jobs, day presets (morning/noon/sunset/night-lite with headlights as fake emissive + 1 spotlight), minimap from road-graph data | MPD exit criteria met; perf budget still green on fuller map |
| Beta (v0.4–0.6) | Kinematic lane-following traffic (Path3D agents, not full physics), more districts dressing, drift/score events, photo mode-lite, rebindable keys, localisation-ready strings (EN/FR/AR discussion at that point) | Traffic cost measured on 960M; job completion fun confirmed by external tester(s) |
| 1.0-candidate | Polish, accessibility (steering assists, colour-blind-safe markers), exports (Linux first; Windows export only if a test machine exists), itch.io page, full third-party credits screen | Zero known crash/data-loss bugs; legal sweep of manifest |

Anything beyond (pursuits, multiplayer, on-foot) is **out of roadmap** until 1.0 ships,
to protect the zero-budget solo+AI reality.

---

## 4. Godot 4 architecture

### 4.1 Engine version & renderer (Decision D-03/D-04, resolved by spike, not by opinion)
- As of the planning date the latest stable line is Godot 4.7.x, but addon
  compatibility (if any addon is adopted) and driver behaviour on Kali matter more
  than newness. **Candidate baseline: the latest patch of Godot 4.4** (Jolt integrated,
  Terrain3D/Road Generator target 4.3/4.4), upgraded only *between* milestones after
  re-running the full test plan. The exact version string is pinned in the repo
  (`docs/ENGINE_VERSION.txt`, created in M0) together with the export-template version.
- **Renderer:** the project must pick one renderer early (an exported game cannot
  meaningfully swap renderers from a settings menu). M0 benchmarks the same greybox
  scene on the local GTX 960M under **Mobile (Vulkan)** and **Compatibility (OpenGL)**.
  Working hypothesis to be *tested, not assumed*: for flat-shaded low-poly,
  Compatibility may be fastest and most robust on an ageing Maxwell driver stack;
  Mobile may win if Vulkan is healthy and if any GPU-particle or clipmap-terrain
  addon is adopted (Terrain3D requires the RenderingDevice-based renderers — adopting
  it would rule Compatibility out). Forward+ (SDFGI, volumetric fog, SSR…) is
  **not targeted** on a 960M and is used at most for director-curiosity screenshots.
- **Physics engine:** Godot Physics vs integrated Jolt (4.4+) is likewise a spike
  question, because the vehicle implementation interacts with it (§4.2). One engine
  is pinned for the project before tuning begins; physics is never switched after
  cars are tuned.

### 4.2 Vehicles & vehicle physics (highest-risk system — see Risk Register R-01)
Godot's own documentation states `VehicleBody3D` "has known issues and isn't designed
to provide realistic 3D vehicle physics". We therefore do **not** bet the game on it
un-tested. Milestone 1 runs a two-track spike on the *same* test track with the
*same* input script:

- **Track A — `VehicleBody3D` + `VehicleWheel3D`** (baseline; the official Truck Town
  demo is our study reference). Fastest to stand up; known quirks at curbs/ramps,
  limited control over tire behaviour.
- **Track B — custom raycast vehicle on `RigidBody3D`** (the expected long-term
  winner for arcade control): 4 suspension RayCast3D/ShapeCast queries in
  `_integrate_forces`, spring/damper per wheel, arcade tire model (longitudinal
  drive/brake force, lateral grip curve with slip falloff, handbrake rear-grip cut,
  anti-roll bars, speed-sensitive steering, mild downforce, ground-material grip
  multipliers). More code, but every behaviour is ours to tune and debug.

Decision gate (measured, § Test Plan T-PHY): stability 0→120→0 km/h, slalom without
spinning unless handbraked, 10 cm curb and 20° ramp behaviour, 60 s scripted drive
without NaN/flip/tunnelling, CPU physics cost per car, and "can the director tune it
from exposed parameters without reading code".

Car data is **data, not code**: `CarDefinition` resources (`.tres`) hold mass,
engine force curve, top speed, grip, brake, steering, wheel positions/radius,
mesh scene, paint material slot, price. One `car.tscn` (physics body + wheel
markers + mesh placeholder + cameras anchor points) is instanced for every car;
unlocks/upgrades modify definition values at runtime — the garage and the world
use the *same* scene so they can never drift apart.

Traffic (post-MPD) will **not** use rigid-body vehicle physics: kinematic
Path3D-following agents with simple gap-keeping, disabled/simplified when distant.

### 4.3 Camera
- `CameraRig` (Node3D, not parented to the car body): SpringArm3D chase camera with
  physics-tick smoothing and Godot 4 physics interpolation, velocity look-ahead,
  speed-based FOV kick (clamped, disable-able in settings for motion comfort),
  plus a fixed hood camera. Camera collision via the spring arm, never clipping
  into buildings knowingly. Shake: off by default, tiny and optional.

### 4.4 World, roads, streaming
- **No streaming system in MPD.** One district fits in memory on 2 GB VRAM if
  budgets are respected. What we *do* build from day 1 is the **chunk contract**:
  the world is authored as district scenes (`world/chunks/chunk_*.tscn`, ~256 m
  cells) instanced by a `WorldRoot`; chunks never reference each other; all props
  are either MultiMeshInstance3D batches or merged static geometry per chunk;
  visibility ranges (LOD/fade distances) set per category. When the island grows
  (Alpha), `WorldRoot` swaps "instance all" for threaded loading
  (`ResourceLoader.load_threaded_request`) in a ring around the player — an
  8-connected neighbourhood — without touching chunk content.
- **Roads, two kinds, one data model:**
  1. *Town grid*: modular road pieces (Kenney City Kit Roads as placeholder/final
     low-poly dressing) snapped on a grid, flat terrain beneath.
  2. *Coastal/hill roads*: Path3D spline → generated ribbon mesh + simplified
     collision. Implementation options are evaluated in a later spike: the MIT
     Godot Road Generator addon vs a small in-house ribbon tool. No addon is
     adopted until it passes the addon gate (works on pinned engine version,
     exports cleanly, source readable, removable without world rebuild).
  - Geometry is separated from routing data: a `RoadGraph` resource set
    (nodes/segments with lane direction, speed class, street name) is authored
    alongside geometry and later powers minimap, mission routing hints, and
    traffic lanes. Cheap now, priceless later.
- **Terrain:** MPD island base is a low-poly heightfield mesh + `HeightMapShape3D`
  collision, generated from a heightmap image we author. Terrain3D (MIT) is an
  *optional* Alpha evaluation only — it brings a GDExtension binary dependency and
  a renderer constraint, so it must earn its place in a spike against our simple
  approach on the 960M.
- **Environment:** fixed time-of-day presets are `Environment` resources; 1k HDRI
  sky (Poly Haven CC0) or procedural sky, distance fog tuned to hide the far-plane
  and justify culling. No dynamic weather; "night" later is a preset, not a sim.

### 4.5 Missions/jobs
- `MissionDefinition` resources: id, title key, type (`delivery|checkpoints|
  discovery`), start marker, ordered checkpoint transforms, par times (bronze/
  silver/gold), reward credits, required unlock (optional).
- `MissionManager` (autoload, single runtime state machine:
  `IDLE → OFFERED → ACTIVE → COMPLETE|FAILED → IDLE`) spawns `Checkpoint`
  Area3D triggers + beacon visuals, runs the timer, emits signals; UI and audio
  only *listen*. No per-mission scripts. Fail states: timeout, car reset
  (configurable per job), abandon from pause menu. Restart job = respawn at start
  marker with car state sanitised (velocity zeroed, upright).

### 4.6 UI
- Pure `Control` scenes + one shared `Theme` resource; gamepad/keyboard focus
  navigation from the start; screens: Boot → Main Menu → (Garage | World+HUD) with
  Pause/Settings as overlays. HUD is signal-driven (speed from car, objective from
  MissionManager) — no per-frame `get_node` fishing. All player-visible strings in
  one table from Alpha onward for future FR/AR localisation.

### 4.7 Garage
- Separate small scene: turntable pad, orbit/inspect camera, car instance in
  **preview mode** (physics frozen, same scene/definition as world), paint swatches
  writing to the shared car material, upgrade tiers writing to the runtime
  definition + save. "Drive" loads the world with the selected car definition.

### 4.8 Audio
- Buses: `Master / Music / SFX / Engine / UI` (layout saved as
  `default_bus_layout.tres`). Engine = looped CC0 sample(s), pitch/volume mapped
  from throttle & speed (RPM proxy), low-pass when off-throttle if cheap. Skid =
  loop gated by lateral slip. Everything per-file CC0-verified in the manifest;
  placeholder silence is preferred over an unverified sample. `AudioService`
  autoload owns volume application from Settings.

### 4.9 Settings & save data
- **Settings** (`user://settings.cfg` via ConfigFile): graphics preset, 3D
  resolution scale, window mode/resolution, shadow quality, camera FOV/shake,
  volumes, steering assist level. Applied at boot by `SettingsService`, before the
  world loads. Renderer and physics engine are *project*-level and not user settings.
- **Progress** (`user://save_slot_0.json`, schema `"save_version": 1`): credits,
  owned cars, selected car, paint per car, upgrade tiers, job best medals/times.
  Written atomically (write temp file → rename), loaded defensively (missing/
  corrupt/unknown-version → fresh profile + backup of the bad file, never crash).
  A "reset progress" option in Settings. Settings and progress are separate files
  so resetting one never kills the other.
- **Autoloads (kept few):** `SettingsService`, `SaveService`, `MissionManager`,
  `AudioService`, `GameState` (current mode + selected car). Everything else is
  scene-local. No global "event bus" god-object; direct signals between the above.

### 4.10 Input
InputMap actions only (`steer_left/right` also as one `steer` axis, `throttle`,
`brake_reverse`, `handbrake`, `camera_toggle`, `reset_car`, `pause`, `horn`
cosmetic). Keyboard (WASD/arrows) + gamepad (left stick, triggers) from M1.
Analog smoothing/dead-zones live in the car input layer, tunable in Settings later.

---

## 5. Proposed project folder structure (to be created in M1, not before)

```text
car-game/
├── docs/                        # this planning pack + ENGINE_VERSION.txt + test evidence logs
│   ├── TDD.md  ASSET_SHORTLIST.md  PERFORMANCE_STRATEGY.md
│   ├── TEST_PLAN.md  MILESTONES_AND_RISKS.md  AI_WORKFLOW.md  FIRST_MILESTONE.md
│   └── assets_manifest_template.csv
├── game/                        # ← Godot project root (project.godot lives here in M1)
│   ├── project.godot
│   ├── icon.svg
│   ├── addons/                  # only addons that passed the addon gate; each with LICENSE copy
│   ├── assets/
│   │   ├── ASSET_MANIFEST.csv   # every imported file: source, license, evidence URL, date, hash
│   │   ├── THIRD_PARTY_LICENSES.md
│   │   ├── models/{cars,props,buildings,roads,vegetation}/   # .glb only (canonical format)
│   │   ├── textures/            # ≤1024px world, ≤512px props unless justified
│   │   ├── audio/{engine,sfx,ui,music}/
│   │   └── fonts/               # OFL fonts only, license file alongside
│   ├── data/
│   │   ├── cars/                # CarDefinition .tres (stats, mesh, price)
│   │   ├── missions/            # MissionDefinition .tres
│   │   ├── road_graph/          # RoadGraph resources
│   │   └── environments/        # Environment presets (golden, noon, …)
│   ├── scenes/
│   │   ├── boot/                # main.tscn boot → menu/world switcher
│   │   ├── vehicles/            # car.tscn (+ wheel visuals), camera_rig.tscn
│   │   ├── world/chunks/        # chunk_*.tscn districts, world_root.tscn, test_track.tscn
│   │   ├── missions/            # checkpoint.tscn, job_marker.tscn
│   │   ├── garage/              # garage.tscn
│   │   └── ui/                  # main_menu, hud, pause, settings, job_result
│   ├── scripts/
│   │   ├── autoload/            # settings_service, save_service, mission_manager, audio_service, game_state
│   │   ├── vehicles/            # car_controller (physics), car_input, car_audio, camera_rig
│   │   ├── world/               # world_root (chunk mgmt), road_ribbon_tool (later spike)
│   │   ├── missions/            # checkpoint, job_marker
│   │   └── ui/                  # one script per screen
│   └── tests/
│       ├── physics_regression/  # scripted-input drive test scene + CSV logger
│       └── benchmarks/          # benchmark route scene + perf logger
├── tools/                       # non-game helper scripts (Python, run in sandbox): manifest checker, log summariser
└── .gitignore                   # .godot/, exports/, *.zip asset downloads (kept out of git)
```

Rules: `.glb` is the single canonical model format (Godot's recommended glTF path);
source `.blend/.fbx` stay outside the repo or in `assets/_sources/` only when tiny
and licence-clean. Downloaded asset **.zip archives are never committed**; the
manifest records the URL + hash so any pack can be re-downloaded. The `.godot/`
import cache and export builds are git-ignored. Total committed asset weight is
budgeted (<150 MB) so the repo stays cloneable on a modest connection — no Git LFS
(zero budget, quota risk).

---

## 6. Director decisions required before implementation (recommendations given)

| ID | Decision | Recommendation | Alternatives |
|---|---|---|---|
| D-01 | Concept/setting: fictional Moroccan-Atlantic town, car-only, jobs loop | **Approve** | Generic unnamed city (blander, same cost) |
| D-02 | Art style: flat low-poly (Kenney/Quaternius family) as *final* style, not placeholder-for-realism | **Approve** | Semi-realistic (unaffordable in assets + 960M perf — not recommended) |
| D-03 | Engine: pin Godot 4.4-latest-patch baseline in M0; upgrade only between milestones | **Approve pending M0 local check** | Latest 4.7.x (addon/driver unknowns) |
| D-04 | Renderer decided by M0 on-machine benchmark (Mobile vs Compatibility), Forward+ not targeted | **Approve process** | — |
| D-05 | Vehicle physics: two-track spike in M1, decision by measured criteria, not preference | **Approve process** | — |
| D-06 | No Terrain3D / Road Generator / scatter addon in MPD unless each passes the addon gate in its own spike | **Approve** | Adopt early (dependency risk on pinned version + old GPU) |
| D-07 | Licence policy: CC0 + MIT (+OFL fonts) only; CC-BY allowed only with a credits entry created at import time; NC/“personal use”/branded models banned | **Approve** | — |
| D-08 | Performance contract: design target is **720p60 Low on the GTX 960M**; prettier presets are for stronger GPUs | **Approve** | 1080p on 960M (forces even smaller world) |

*End of TDD. See `FIRST_MILESTONE.md` for the exact first implementation step once
D-01…D-08 are approved or amended.*
