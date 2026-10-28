# Performance Strategy — designing for the GTX 960M first

Status: **PLANNING (2026-10-28). All numbers below are design budgets to be
validated on the director's machine in M0/M1 — none are measured results yet.**

## 1. Target hardware reality

- **GTX 960M**: 2015 Maxwell laptop GPU, 640 CUDA cores, 128-bit GDDR5 bus
  (~80 GB/s), shipped in **2 GB and 4 GB VRAM variants** — which one the director
  has is unknown until M0 runs `nvidia-smi`. We budget for the **2 GB variant**
  unless M0 proves otherwise. Vulkan-capable and OpenGL 4.5-capable on paper;
  real-world health depends on the installed NVIDIA driver branch on Kali and
  whether the laptop uses Optimus (hybrid Intel+NVIDIA) routing. Both are M0
  checklist items, recorded in `docs/ENGINE_VERSION.txt` alongside the Godot pin.
- Godot's own system requirements put a GTX 1050-class card as *recommended* for
  Forward+, with Vulkan 1.0 integrated graphics as *minimum* — i.e. the 960M can
  run Godot 4, but Forward+'s expensive features (SDFGI, volumetric fog, SSR,
  SSAO, TAA at high res) are not free on it. Our response is architectural, not
  hopeful: stylised flat-shaded content, one shadow-casting light, aggressive
  batching, and renderer choice by benchmark (TDD §4.1).
- **Performance contract (Decision D-08):** Low preset = **720p, 60 fps, on the
  960M**, sustained on the benchmark route (1% lows ≥ 50). Balanced aims ~900p on
  the same card / 1080p on newer cards. High exists for stronger GPUs and
  screenshots; it must never be required to make the game look "right".

## 2. Hard budgets (enforced at asset intake & in benchmark review)

| Budget | Low (960M design target) | Notes |
|---|---|---|
| Internal 3D resolution | 1280×720 (scale 1.0 at 720p; 0.67× if displayed at 1080p) | Viewport scaling is the single biggest lever on a 128-bit-bus GPU |
| Visible triangles | ≤ 600k typical, ≤ 900k worst view | Hero car ≤ 15k tris; parked/traffic cars ≤ 6k; buildings ≤ 1.5k each, merged per chunk |
| Draw calls (visible) | ≤ 250 | Merge static geometry per chunk; MultiMeshInstance3D for trees/rocks/props; one shared material atlas family (Kenney-style vertex/flat colours) wherever possible |
| Texture VRAM | ≤ 700 MB total resident | 1k HDRI sky, ≤1024px world textures, ≤512px props, VRAM compression + mipmaps on everything 3D; flat-colour materials need no textures at all |
| Lights | 1 directional (shadow-casting) + ambient/sky; ≤ 4 non-shadow omni/spot in view (garage/night-preset exceptions) | No per-streetlamp shadow lights, ever. Fake pools of light with emissive + decals if night preset arrives |
| Shadows | Single directional cascade setup; atlas 2048 (Low) / 4096 (Balanced+); tight shadow distance (~120–180 m) matched to fog | Shadow *distance* is a preset knob; distant chunks don't cast |
| Particles | CPU particles or tiny GPU emitters; dust/skid puffs budgeted ≤ 300 alive | Renderer choice affects GPU-particle availability (Compatibility = CPU fallback) — design effects that look fine as CPU particles |
| Physics | 60 Hz ticks; player car = 4 ray/shape queries + body; parked cars = static bodies; future traffic = kinematic path followers, **not** rigid bodies | A physics-regression test caps per-car physics cost before traffic is designed (TEST_PLAN T-PHY-05) |
| Scripting | GDScript everywhere; no per-node `_process` on props; one `WorldRoot` updates chunk states | Profile before optimising; C# is not adopted (mono build weight, no need) |
| Load time | Menu interactive ≤ 3 s from launch on the target laptop (cold) | District scenes preload small; threaded loading only when Alpha streaming arrives |

## 3. Scalable graphics presets (Settings menu — applied via RenderingServer/ProjectSettings APIs at runtime where Godot allows, else at next scene load; renderer itself is project-fixed)

| Setting | Low (GTX 960M) | Balanced | High (stronger GPU) |
|---|---|---|---|
| 3D resolution scale | 0.67–0.75 (≈720p at 1080p display) or native 720p | 0.85–1.0 | 1.0 (up to 1440p display) |
| MSAA 3D | Off | 2× (if renderer allows cheaply) | 4× / TAA where supported |
| Directional shadow size | 2048 | 4096 | 4096 |
| Shadow distance / camera far | ~150 m / 400 m + fog | ~220 m / 600 m | ~300 m / 900 m |
| Mesh LOD bias / visibility ranges | Aggressive (props out ~120 m, trees ~200 m) | Standard | Relaxed ×1.5 |
| Vegetation/prop density (MultiMesh counts per chunk) | 50% | 100% | 100% |
| Environment | No glow/bloom (or minimal), no SSAO/SSR, fog on | Glow optional | Glow + richer tonemap; still no SDFGI requirement |
| Texture quality | Half-res import variants if VRAM pressure measured | Full (≤1k) | Full (≤1k) |
| Physics ticks / interpolation | 60 Hz + interpolation ON (smoothness over raw rate) | same | same (tuning is preset-independent on purpose) |

Preset implementation notes: presets are data (`SettingsService` applies a
dictionary of rendering settings), first-run default = **Low** (we optimise for the
machine we own; the game can only look better elsewhere). An "Auto" mode is out of
scope until the benchmark logger exists to drive it honestly.

## 4. How we will know (measurement, not vibes)

1. **Benchmark route** (TEST_PLAN T-PERF): scripted camera/car path through the
   densest district view + coastal road, 60 s, logging frame times, draw calls,
   primitives, physics time via `Performance` monitors to CSV.
2. Run at every milestone exit on the local 960M; CSVs committed under
   `docs/evidence/` with commit hash + preset in the filename. A >10% regression
   in average frame time or 1% lows blocks the milestone until explained.
3. Worst-view screenshot points are fixed (harbour overlook, old-town main street)
   so budgets are checked where the game is heaviest, not where it's flattering.
4. Editor rendering on the same laptop is itself a cost: if the editor is sluggish,
   we develop with chunk visibility toggles and the Low preset in-editor rather
   than shrinking the design blindly.

## 5. Known platform risks specific to this setup (full register in MILESTONES_AND_RISKS.md)

- NVIDIA Maxwell driver support on a rolling-release Kali can break after kernel/
  driver updates → M0 records exact driver + kernel; director avoids mid-milestone
  driver upgrades; Compatibility-renderer fallback exists precisely for Vulkan pain.
- Optimus laptops can silently run Godot on the Intel iGPU → M0 verifies which GPU
  Godot reports; launch instructions (prime-run / `__NV_PRIME_RENDER_OFFLOAD`) are
  written into the local test checklist if needed.
- Thermal throttling on an older laptop makes benchmarks drift → benchmark runs are
  done plugged-in, after a 2-minute warmup, best-of-3 discarded (median run kept).
