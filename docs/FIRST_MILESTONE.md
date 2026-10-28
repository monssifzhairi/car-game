# Exact First Implementation Milestone — M0 + M1 "Prove the machine, prove the car"

Status: **PLANNING (2026-10-28) — not started. Requires director approval of
Decisions D-01…D-08 (TDD §6).** This milestone deliberately contains **no game
content**: no district, no jobs, no garage. It answers the two questions the whole
project stands on — *can this laptop run our Godot setup at 60 fps?* and *can one
car feel great?* — with local evidence, before anything is built on top of the answers.

Estimated total: **3–5 working sessions** (Part A: 1–2, Part B: 2–3), director's
local time ≈ 30–60 min per test round.

---

## Part A — M0: Environment recon & renderer decision

### A1. Director's local fact-gathering (run once, paste outputs into the session)
```bash
nvidia-smi                 # exact GPU, VRAM (2 vs 4 GB), driver version
uname -r                   # kernel
vulkaninfo --summary       # is Vulkan healthy, and on which GPU? (install vulkan-tools if missing)
lspci | grep -i -E "vga|3d"   # single-GPU or Optimus hybrid?
free -h && nproc           # RAM / CPU threads (budgets + physics expectations)
```
Also note: built-in display resolution, gamepad model (if any), free disk space.

### A2. Install the pinned engine (candidate, confirmed by A3 results)
- Download the official **Godot 4.4 latest-patch** Linux build + export templates
  from godotengine.org (free, no account). Keep the downloaded version string
  verbatim. Install free tools alongside: **Blender** (official build) and
  **Audacity** — used from M2/M6, installed now so versions are recorded together.
- Open an *empty* Godot project; in the editor's rendering info / `--version` and
  the output log, confirm Godot is using the **NVIDIA** GPU (not an Intel iGPU).
  If Optimus mis-routes, document the working launch method (e.g. PRIME offload
  env vars) in `docs/ENGINE_VERSION.txt`.

### A3. Renderer benchmark spike (AI writes it, director runs it)
The AI creates the first (throwaway-spike) Godot project containing one stress
scene: a flat-shaded proxy town (~400 instanced boxes as "buildings", 100
"tree" cones, 20 box "cars", one shadow-casting directional light, fog, sky) and
a scripted camera flythrough logging `Performance` monitors (frame time, draw
calls, primitives) to CSV. The **same scene** is run three times — Mobile (Vulkan),
Compatibility (OpenGL), and (curiosity only) Forward+ — at 720p and 1080p,
plugged-in, after warmup, median run kept.

**Decision rule (pre-agreed):** pick the renderer with the best 1% lows that has
*zero* driver errors across all runs; if Mobile and Compatibility are within 5%,
pick Compatibility (simpler feature set = fewer surprises on old drivers) unless
a planned MPD feature needs the RenderingDevice. Forward+ is eliminated unless it
somehow beats both (document the surprise if so).

### A4. Sandbox feasibility question (AI, in Arena)
Attempt — once, timeboxed — to fetch the official Godot Linux binary from GitHub
releases into the sandbox and run `godot --headless --version` + import the spike
project. Outcome recorded either way in `AI_WORKFLOW.md`: success upgrades L1
tests to sandbox-automatable; failure changes nothing (checks run locally).
**No project decision may depend on this succeeding.**

### A5. Part A deliverables & exit gate
- `docs/ENGINE_VERSION.txt`: Godot version + templates, Blender/Audacity versions,
  GPU/VRAM/driver/kernel, chosen renderer + physics-engine candidate, launch notes.
- `docs/evidence/M0/`: the benchmark CSVs + one screenshot of the stress scene.
- TDD §4.1 amended with the *decided* versions (dated amendment).
- **Exit gate:** director confirms the editor is pleasant to use on the laptop and
  approves the renderer choice from the CSVs. Tag `known-good/m0-env`.

---

## Part B — M1: One car, one test track, two physics tracks, one decision

### B1. Files the AI will create (complete list — nothing beyond this list in M1)
```text
game/project.godot                                   (pinned settings, InputMap actions, physics ticks=60, interpolation on)
game/scenes/boot/main.tscn                           (loads test track directly for M1; menu comes in M3)
game/scenes/world/test_track.tscn                    (flat plane, 300 m straight, slalom cones, 10 cm curb, 20° ramp, banked corner, start/finish markers)
game/scenes/vehicles/car.tscn                        (physics body + 4 wheel markers + placeholder box body mesh + cylinder wheel visuals)
game/scenes/vehicles/camera_rig.tscn                 (SpringArm3D chase + hood cam)
game/scripts/vehicles/car_controller_vehiclebody.gd  (Track A)
game/scripts/vehicles/car_controller_raycast.gd      (Track B)
game/scripts/vehicles/car_input.gd                   (keyboard+gamepad → normalised inputs; synthetic-input playback for tests)
game/scripts/vehicles/camera_rig.gd
game/scripts/vehicles/telemetry_logger.gd            (speed, slip, g, physics ms → CSV in user://)
game/tests/physics_regression/run_physics_tests.gd   (drives T-PHY-01…05 with synthetic inputs, prints PASS/FAIL summary)
game/tests/physics_regression/physics_test_track.tscn (test wrapper scene)
docs/evidence/M1/                                    (telemetry CSVs + director verdict, added after local runs)
```
Placeholder visuals are Godot primitive meshes only — **no downloaded assets in
M1** (asset intake starts in M2, so physics judging isn't polluted by art).

### B2. Behaviour spec (both tracks must implement the same interface)
Inputs: steer (−1…1), throttle (0…1), brake/reverse (0…1), handbrake (bool) —
from `car_input.gd`, so switching tracks = swapping one controller script.
Shared expectations: speed-sensitive steering limit, gentle auto-centre feel,
reverse only from near-stop, handbrake cuts rear lateral grip (drift-lite),
`reset_car` (R / gamepad Y) places the car upright at the last track checkpoint
with zero velocity. Target character: **forgiving arcade** — a new player keeps
it on the road at 80 km/h; a good player can provoke a controllable slide.

### B3. Test & decide (TEST_PLAN T-PHY-01…06, T-PERF-01 adapted to the track)
1. AI marks all M1 code `[UNTESTED]`, runs every sandbox check available (L0,
   plus L1 only if A4 succeeded).
2. Director runs `run_physics_tests` for **both** tracks → returns CSVs + log.
3. Director free-drives each track 5 minutes, then answers in writing:
   (a) which feels more fun and why, (b) any instability observed (with track
   feature + speed), (c) gamepad vs keyboard preference issues.
4. Decision recorded in TDD §4.2 amendment: winning track, physics engine
   (Godot Physics vs Jolt — whichever the winner ran best on; if the winner is
   Track A, verify its behaviour under the chosen physics engine explicitly,
   since vehicle-node support can differ by engine), and the frozen T-PHY
   pass-bars measured from the winner's telemetry.
5. Losing controller is **deleted** (kept in git history), leaving exactly one
   vehicle implementation. No "keep both just in case".

### B4. Acceptance criteria (all must be LOCAL-VERIFIED to exit M1)
- [ ] T-PHY-01…06 pass on the winning track; CSVs in `docs/evidence/M1/`.
- [ ] 60 s continuous driving incl. curb/ramp abuse: no NaN, no tunnelling, no unexplained flip, reset always recovers.
- [ ] Test track holds 60 fps at Low preset/720p on the GTX 960M (frame-time CSV attached).
- [ ] Director's written verdict: winning track is *fun in an empty greybox*. If neither is fun, M1 does **not** exit — tuning iterates here, cheaply, instead of later under a full game.
- [ ] Exactly one car controller remains; TDD amended; tag `known-good/m1-drive`.

### Explicitly out of scope for M0+M1
Any CC0 asset downloads/imports, district/world building, menus beyond "the track
loads", saving, audio beyond silence, traffic, minimap, engine upgrades, addons
of any kind. If it isn't in §B1's file list, it waits for its milestone.

---

## What the director does next (when ready)

1. Reply with approval/amendments to **D-01…D-08** (TDD §6).
2. Run the §A1 commands and paste the outputs.
3. The AI then executes Part A step A3/A4 and Part B in order, in small commits,
   stopping at every local-test gate for your evidence and verdict.
