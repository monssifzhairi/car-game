# Milestone Plan, Acceptance Criteria & Risk Register

Status: **PLANNING (2026-10-28).** Effort is estimated in *working sessions*
(1 session ≈ one focused AI-implementation round + one director local-test round)
rather than calendar promises. A milestone is done only when its acceptance
criteria are **LOCAL-VERIFIED** and tagged (see `AI_WORKFLOW.md`, `TEST_PLAN.md`).

## 1. Milestones to the Minimum Playable Demo

| ID | Milestone | Delivers (smallest complete slice) | Acceptance criteria (local, GTX 960M) | Est. |
|---|---|---|---|---|
| **M0** | **Environment recon & engine spikes** *(exact spec: `FIRST_MILESTONE.md` Part A)* | Godot pinned & documented; GPU/driver facts recorded; renderer benchmark (Mobile vs Compatibility) on a greybox stress scene; headless-Godot-in-sandbox feasibility answered yes/no | `ENGINE_VERSION.txt` committed with Godot build, templates, driver, GPU/VRAM, renderer choice + benchmark CSVs; editor opens an empty project on the discrete GPU at usable speed | 1–2 sessions |
| **M1** | **Driveable greybox — physics decision** *(exact spec: `FIRST_MILESTONE.md` Part B)* | One car (placeholder box-mesh body, real wheel visuals), flat test track (straight, slalom cones, curb, ramp, bank), chase+hood cams, keyboard/gamepad, reset; **both** physics tracks (VehicleBody3D vs custom raycast RigidBody3D) behind a switch; telemetry logger | TEST_PLAN T-PHY-01…06 run for both tracks; decision recorded with numbers; director verdict: winner is *fun for 5 minutes of pointless driving*; ≥60 fps Low on the track | 2–3 sessions |
| **M2** | **First district greybox + asset intake** | 800×800 m district: heightfield island base, Kenney roads/buildings (intake-gated), parked cars, props via MultiMesh; asset test scene; manifest live | Drive the full district loop without falling through world/getting stuck; T-PERF-01/02 within budget at Low; every visible asset has a manifest row (T-L0-02 green) | 2–3 sessions |
| **M3** | **Game shell: menus, settings, save** | Boot→menu→world flow, pause, settings (presets/volumes/FOV), SettingsService+SaveService with versioned schema + corruption recovery, HUD skeleton | Settings persist across relaunch; corrupted-save fixture recovers to fresh profile without crash; presets measurably change frame time (CSV); gamepad can navigate all menus | 2 sessions |
| **M4** | **Jobs system (data-driven)** | MissionManager state machine, checkpoints/markers, timer, results screen; 3 jobs authored as data (delivery, sprint, discovery) | Full L4 jobs checklist passes (complete/fail/abandon/restart each); adding a 4th job requires *only* a new `.tres` + marker placement (proven by doing it in-session) | 2 sessions |
| **M5** | **Garage + second car + upgrades** | Garage scene (preview rig, paint, engine/grip tiers), 2nd CarDefinition with distinct feel, credits economy wired to jobs | Unlock→paint→upgrade→drive loop persists through save/relaunch; upgraded car measurably beats T-PHY-01 baseline; cannot overspend/select locked car | 2 sessions |
| **M6** | **Audio + feel polish** | Engine/skid/UI audio from CC0-verified files, bus volumes from settings, camera FOV-kick tuning, speed lines-off-by-default comfort options | 10-min soak (T-PERF-03) clean; no audio pops on loop points (director by ear); director signs "feels good" or issues a specific tuning list | 1–2 sessions |
| **M7** | **Demo v0.1 export & freeze** | Linux export from pinned templates, exported-binary L4 pass, credits screen from `THIRD_PARTY_LICENSES.md`, demo README with controls/known issues | Exported build (not editor) passes TEST_PLAN L5 + MPD exit criteria (TDD §2); tag `known-good/demo-v0.1`; risk register reviewed | 1 session |

Post-demo stages (Alpha/Beta/1.0-candidate) are outlined in TDD §3 and get their
own milestone docs only after Demo v0.1 is tagged.

## 2. Risk register

Probability/Impact: H/M/L. Owner = who watches it. "Trigger" = the observable
signal that the risk is materialising (so we react to evidence, not anxiety).

| ID | Risk | P | I | Mitigation (planned) | Trigger / early signal | Owner |
|---|---|---|---|---|---|---|
| R-01 | **Vehicle physics feels bad or is unstable** — Godot documents `VehicleBody3D` known issues; a custom model can also go wrong (jitter, tunnelling, fun-killing grip) | H | H | M1 two-track spike with frozen regression tests (T-PHY) *before* any world content depends on it; arcade (not sim) target; all tuning exposed as data; physics engine pinned before tuning | Either track fails T-PHY-04/05, or director's 5-minute verdict is "not fun" | AI builds, Director judges |
| R-02 | **GTX 960M / Kali driver stack can't hold 60 fps** (2 GB VRAM variant, Optimus routing, rolling-release driver breakage, thermals) | M | H | Budgets + presets designed for 720p Low (`PERFORMANCE_STRATEGY.md`); renderer chosen by M0 benchmark with Compatibility fallback; driver/kernel frozen mid-milestone; benchmark at every milestone exit | M0 benchmark <60 fps on trivial scene, Godot running on iGPU, Vulkan device-lost errors | Director (machine), AI (budgets) |
| R-03 | **Addon/engine version trap** — Terrain3D/Road Generator/test-framework lags or breaks on our pinned Godot, or an upgrade silently changes physics | M | H | Zero addons in MPD path; each adoption behind its own spike + "removable after baking" test; engine pinned in `ENGINE_VERSION.txt`, upgrades only between milestones with full TEST_PLAN re-run | Spike import/export fails on pinned version; addon repo unmaintained >1 Godot minor | AI |
| R-04 | **Asset style/scale incoherence** — Kenney chunky vs Quaternius proportions vs photoreal textures look like three different games; wheels merged into bodies; wrong scale | H | M | One art bible rule set (flat low-poly, shared palette, photoreal only for ground/sky at 1k); Asset Intake Gate checks wheels/scale/tris in Blender *before* import; asset test scene screenshot per batch | Intake finds merged wheels / >budget tris on hero cars; side-by-side screenshot reads inconsistent | AI checks, Director eyeballs |
| R-05 | **Licence contamination** — a "free" file turns out NC/personal-use/branded | M | H | CC0/MIT-only policy (D-07), no manifest row → no import, per-file check on mixed libraries (Freesound/OGA), banned sources list, credits generated from manifest | Any asset arrives without a verifiable licence page | AI |
| R-06 | **Scope creep kills the demo** (traffic, police, on-foot, "just one more district") | H | H | TDD §1/§2 explicit NOT-list; new ideas go to a post-demo parking lot in this doc's amendments, never into the current milestone; milestone exit criteria frozen at approval | A milestone gains tasks after approval; sessions-per-milestone exceed estimate ×1.5 | Director (veto), AI (flags) |
| R-07 | **AI-generated code that "looks right" but was never run** accumulates, then collapses at first local test | H | M | Small commits, UNTESTED labelling, director test round *every* milestone (not "at the end"), fixes only from logs/evidence, known-good tags to revert to | A milestone needs >2 fix rounds for the same system | Both |
| R-08 | **Save/settings corruption** loses director/tester progress | L | M | Versioned schema, atomic write-temp-rename, defensive load with backup-and-fresh-start, corrupt-fixture test (T-L1-03/L4) from M3 | Any crash on load in testing | AI |
| R-09 | **World scale outgrows the hardware** — Alpha island + traffic breaks the perf contract that the demo met | M | M | Chunk contract from day 1 (TDD §4.4) so streaming/culling is an activation change, not a rebuild; T-PERF gates every stage; traffic is kinematic by design | T-PERF-01 regression >10% at any milestone exit | AI |
| R-10 | **Single-machine/single-person bus factor** — laptop dies, director time vanishes | L | H | Everything reproducible from git + manifest URLs + `ENGINE_VERSION.txt`; exported known-good builds kept locally by director; docs written so a fresh AI session (or OpenCode) can resume from `docs/` alone | — (standing mitigation) | Director |

## 3. The three biggest technical risks (summary)

1. **R-01 Vehicle physics** — the game's entire value rides on an area where the
   engine's built-in solution is officially caveated. *Reduction:* decide it by
   instrumented spike in M1, before building anything on top; keep the losing
   track's test data so the decision is auditable.
2. **R-02 Target-hardware performance** — a 2015 2–4 GB laptop GPU on a rolling
   Linux distro is both our design target and our dev machine. *Reduction:*
   budgets and 720p-Low contract from day 1, renderer by benchmark in M0,
   per-milestone perf gates with committed CSV evidence.
3. **R-03 Version/addon dependency** — one incompatible GDExtension or physics
   change can invalidate tuning and content. *Reduction:* vanilla-Godot MPD,
   pinned engine, addons only via gated spikes with an exit path (baked output
   must survive addon removal).
