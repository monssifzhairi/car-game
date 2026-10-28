# Asset Shortlist & Licence Evidence

Status: **PLANNING (2026-10-28). Nothing below has been downloaded, imported, or
inspected yet.** Every entry is SHORTLISTED based on its publisher's licence page
(fetched/searched during planning). Before any file enters the project it must pass
the **Asset Intake Gate** (§3) and be recorded in `assets/ASSET_MANIFEST.csv`.

Format policy: Godot recommends glTF 2.0 (`.gltf`/`.glb`) for 3D imports; FBX works
via the built-in ufbx importer (4.3+) and `.blend` imports via a local Blender
install, but our canonical committed format is **`.glb`** — anything else is
converted once at intake (Blender, free) so the project never depends on FBX/Blend
tooling at build time. Source: Godot docs, "Available 3D formats"
(https://docs.godotengine.org/en/4.4/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html).

Licence policy (Decision D-07): **CC0 and MIT only by default** (OFL for fonts).
CC-BY is acceptable only if a credits line is added to `THIRD_PARTY_LICENSES.md` in
the same commit. CC-BY-NC, "free for personal use", editorial-only, and any model
depicting a real branded car (trademark survives even a CC0 *copyright* release)
are banned.

---

## 1. Shortlist — models & environment

| # | Asset (role in game) | Source | Licence & evidence (checked 2026-10-28) | Formats (publisher-stated; verify at intake) | Fit / unknowns to verify at intake |
|---|---|---|---|---|---|
| A1 | **Kenney Car Kit** — starter/placeholder hero cars, parked cars, cones/debris | https://kenney.nl/assets/car-kit | **CC0.** Pack page: "Files 45×, License: Creative Commons CC0". Kenney support page: "all game assets on the asset pages are public domain licensed (CC0)… even in commercial projects"; attribution not required (do not use Kenney logo). https://kenney.nl/support | ZIP of models (Kenney 3D kits typically ship GLB/FBX/OBJ — **verify**) | Chunky stylised proportions. **Must verify:** wheels as separate meshes/pivots (needed for steering/spin visuals), scale (metres?), tri counts, material count. If wheels are merged, car is usable for parked/traffic only until split in Blender. |
| A2 | **Kenney Racing Kit** — barriers, track dressing, checkpoint props | https://kenney.nl/assets/racing-kit | **CC0.** Pack page: "Download this package (110 assets) for free, CC0 licensed" + support page above | As A1 — verify | Useful for checkpoint/slalom dressing on the test track from M1. |
| A3 | **Kenney City Kit (Roads)** — town road pieces, signs, traffic lights | https://kenney.nl/assets/city-kit-roads | **CC0.** Pack page: "Files 90×, License: Creative Commons CC0", v2.2. Publisher notes single-material optimisation in 2.0 update | As A1 — verify | Grid sizes/snapping to define our town block size around the kit (measure at intake). Dutch-style variation exists; we'll recolour materials toward the Cap Sirocco palette. |
| A4 | **Kenney City Kit (Commercial / Suburban / Industrial)** — buildings for 3 districts | https://kenney.nl/assets (City series) | **CC0** per each pack page + support page (re-check each pack page on download day and save its included licence file) | As A1 — verify | Building footprints/heights define chunk massing. Verify per-model tri counts; merge static geometry per chunk regardless. |
| A5 | **Kenney Nature Kit** (and similar Kenney kits) — trees/rocks | https://kenney.nl/assets | **CC0** per support page; verify pack page on download day | As A1 — verify | Must be MultiMesh-instanced, never individual nodes, past a few dozen instances. Palm-type trees may need a Quaternius/other CC0 supplement. |
| A6 | **Quaternius LowPoly Cars** — more realistic-proportioned hero car candidates (sports car, SUV, taxi, hatchback…) | https://quaternius.itch.io/lowpoly-cars ; mirror/bundle: https://poly.pizza/bundle/Cars-Bundle-FE5IWe6OMk ; OpenGameArt: https://opengameart.org/content/lowpoly-cars | **CC0.** itch page: "CC0 License https://creativecommons.org/publicdomain/zero/1.0/" and author comment: "I use a CC0 license, so you can even use them in commercial projects". Poly Pizza bundle lists "Licence: Public Domain (CC0)". ⚠ The **Cop SUV is Patreon-only ($1) — excluded** (zero budget + not part of the free CC0 drop). | FBX/OBJ/Blend (itch); FBX+GLB via Poly Pizza bundle | Best hero-car silhouettes in the free CC0 pool. **Must verify:** wheel separability, interior/exterior detail cost, tri counts (these are "low-poly" by 2018 standards). GLB via Poly Pizza avoids an FBX conversion step; still record original author (Quaternius) in manifest. |
| A7 | **Quaternius environment/props packs** (as needed per-pack) | https://quaternius.com / itch | Quaternius packs are **stated per pack** (most CC0) — no blanket approval: each pack's licence line is copied into the manifest at intake | Usually FBX/GLB/Blend | Only pulled in per-need (e.g. palms, street props) to keep style coherent with A1–A5. |
| A8 | **Poly Haven** — HDRI skies (1k only), a few ground/asphalt PBR texture sets | https://polyhaven.com/license | **CC0.** Licence page: "Our assets are all licensed as CC0… You can use our assets for any purpose, including commercial work. You do not need to give credit… You can redistribute them." (Note: their *website* ToS still applies to site use/API; asset files are CC0.) | HDR/EXR HDRIs; PNG/JPG texture maps; models glTF etc. | Download **1k** variants only (VRAM budget). Photoreal textures can clash with flat low-poly — use sparingly (road/ground detail, sky), keep saturation controlled. |
| A9 | **ambientCG** — asphalt, pavement, sand, ground PBR sets (1k) | https://ambientcg.com (licence: https://docs.ambientcg.com/books/website-licensing/page/license-information ) | **CC0.** Site: "All assets are released under the Creative Commons CC0 license, making them free to use without attribution — even in commercial circumstances." | PNG/JPG map sets (ZIP per material) | As A8: 1k max, few hero surfaces only. Road ribbon + terrain detail are the intended uses. |
| A10 | **Godot "Truck Town" demo** — *study reference only* for VehicleBody3D baseline & follow camera | https://github.com/godotengine/godot-demo-projects (3d/truck_town); Asset Library #524/#2752 | Godot demo projects are MIT-licensed (repo LICENSE); we will read and re-implement, not wholesale-copy scenes/assets into the game. If any snippet is adapted, MIT notice goes into `THIRD_PARTY_LICENSES.md`. | Godot project (GDScript) | Values are tuned for trucks/demos, not our cars; treat as documentation with moving pictures. |

## 2. Shortlist — code addons (each gated, none adopted yet) & audio

| # | Item (role) | Source | Licence & evidence | Gate before adoption |
|---|---|---|---|---|
| C1 | **Godot Road Generator** (TheDuckCow) — spline roads/highways + lane data | https://github.com/TheDuckCow/godot-road-generator | **MIT** (repo/Asset Library listings) | Spike on pinned Godot version: build our coastal segment, export test, measure editor + runtime cost, confirm roads still work if addon removed after baking. Alternative: in-house ribbon tool. |
| C2 | **Terrain3D** (TokisanGames) — clipmap terrain | https://github.com/TokisanGames/Terrain3D | **MIT.** README: "This addon has been released under the MIT License"; C++ GDExtension, 64 m–65 km terrains, up to 10 LOD levels | Only if the simple heightfield approach demonstrably fails. Costs: binary GDExtension dependency per Godot version, requires RenderingDevice renderer (rules out Compatibility), binary size on old hardware unmeasured. |
| C3 | **ProtonScatter / HungryProton scatter** — vegetation/prop scattering | https://github.com/HungryProton/scatter | **MIT** (addon licence listings) | Only when hand-placed + MultiMesh painting becomes the bottleneck (Alpha). Demo-folder assets have their own licence notes — do not import demo assets blindly. |
| C4 | **GdUnit4 or GUT** — automated tests | https://godotengine.org/asset-library/asset/1522 (GdUnit4); GUT on GitHub/AssetLib | Both MIT (verify at intake) | Not needed for M1: start with zero-dependency scripted test scenes. Adopt ONE framework later only if test count justifies it (see TEST_PLAN). |
| S1 | **Kenney audio packs** (Interface/Impact/etc.) — UI clicks, impacts, jingles | https://kenney.nl/assets (Audio category) | **CC0** per support page (covers audio packs) + licence file inside each download | Verify engine-suitable loops probably absent — UI/impact only. |
| S2 | **Freesound (CC0-filtered only)** — engine loop, skid, wind, ambience | https://freesound.org | **Per-file licensing** (CC0 / CC-BY / CC-BY-NC mixed library) — there is NO blanket approval. Only files individually confirmed **CC0** (or CC-BY with credits line) may be imported; each gets its own manifest row with the sound's URL + licence. Free account required to download. | Director downloads (account) → intake gate → loop-point editing in Audacity (free). Silence placeholder until then. |
| S3 | **OpenGameArt (CC0-filtered only)** — spare SFX/music candidates | https://opengameart.org | Per-file licensing; use CC0 filter only, manifest per file | Same as S2. Music is out of MPD scope regardless. |

**Deliberately NOT shortlisted:** Sketchfab/CGTrader/TurboSquid "free" cars (mixed
licences, real-brand trademark traps, inconsistent topology/scale), Textures.com
free tier (redistribution restrictions clash with an open repo), any "GTA/Forza-style
pack", ripped game models, and AI-asset marketplaces with unclear training/licence
terms. Finding a car there "for free" would cost more in legal/styles risk than the
CC0 route costs in charm.

## 3. Asset Intake Gate (applies to every file, no exceptions)

1. Licence line + evidence URL + download date entered in `ASSET_MANIFEST.csv`;
   included `LICENSE.txt` (if any) copied next to the asset. **No row → no import.**
2. Open in Blender (free, local): check scale (1 unit = 1 m, car ≈ 4.2–4.8 m long),
   forward axis, origin at ground-centre, wheels separate (cars), tri count vs
   budget, material/texture count, no brand badges/logos (remove/replace if any).
3. Export canonical `.glb`; textures resized to budget (≤1024 world / ≤512 props;
   HDRIs 1k) with mipmaps; set Godot import compression (VRAM) at first import.
4. Drop into the **asset test scene** (created in M2): greybox lighting, turntable,
   draw-call/tri readout screenshot attached to the PR/commit message.
5. SHA-256 of the committed file recorded in the manifest (sandbox-checkable; see
   `AI_WORKFLOW.md`) so any later silent file swap is detectable.

*Template: `docs/assets_manifest_template.csv`.*
