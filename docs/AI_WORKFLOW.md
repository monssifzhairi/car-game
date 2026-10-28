# AI Development Workflow — Arena sandbox ⇄ director's laptop

Status: **PLANNING (2026-10-28).** Roles: **Director (human)** approves decisions,
runs everything on the real machine, judges fun. **AI (Arena Agent Mode; OpenCode
Desktop later if its free-model support unblocks)** plans, writes code/files,
reviews logs, proposes fixes. Neither pretends to do the other's job.

## 1. The loop (every milestone, no shortcuts)

```text
1. PLAN      AI drafts the milestone doc (scope, files, acceptance tests).
             Director approves / amends  ── decision gate ──
2. SPIKE     (only when a technical unknown exists) AI builds the smallest
             throwaway test; director runs it locally; evidence decides.
3. IMPLEMENT AI writes the smallest complete change on the session branch,
             in small commits, every file referenced to the milestone doc.
4. SANDBOX   AI runs everything runnable in the cloud (see §3): static checks,
   CHECKS    manifest/lint scripts, and — only if a Godot binary is present —
             headless import/parse/logic tests. Results labelled honestly.
5. LOCAL     Director pulls, runs the milestone's acceptance checklist on the
   TEST      GTX 960M (TEST_PLAN L2–L4), pastes logs/CSVs/verdict back.
6. FIX       AI fixes from evidence only (log line → cause → smallest patch).
             "Works on my sandbox" is not an acceptable sentence.
7. TAG       On director's pass: merge to main, tag known-good/<milestone>,
             update docs (decisions, evidence, risk register). Next milestone
             may now start. Broken main is reverted to the last tag, not patched
             forward under time pressure.
```

## 2. Version-control & preservation rules

- Work happens on the Arena session branch; `main` only receives director-passed
  merges. Small commits (one system/scene each) with messages that state the test
  status: e.g. `feat(car): raycast suspension v1 [UNTESTED]`,
  `fix(save): atomic write [LOCAL-VERIFIED a1b2c3d]`.
- **Preserve working versions:** every milestone exit = annotated git tag +
  exported build kept by the director locally (builds are git-ignored; the tag +
  pinned `ENGINE_VERSION.txt` make them reproducible).
- Asset .zips, `.godot/`, exports: never committed. Committed assets only via the
  Asset Intake Gate with manifest rows + SHA-256.
- Docs are code: any architecture decision that changes gets a dated amendment in
  the relevant doc in the same PR — the TDD must never silently diverge from reality.

## 3. What can genuinely be automated where

### In the Arena cloud sandbox (verified environment facts, 2026-10-28)
- ✅ Present today: git, Python 3.11, full file editing. **Godot is NOT installed**
  (`which godot` → nothing), repo was empty at planning time.
- ✅ Always automatable: writing/editing GDScript (`.gd`), scenes (`.tscn`) and
  resources (`.tres`) as text; docs; Python tooling (manifest checker, CSV/log
  summarisers, save-schema validators); git operations; web research with
  licence verification; reviewing director-pasted logs and telemetry.
- ⚠️ *Possibly* automatable, to be **proven in M0, not assumed**: downloading an
  official Godot Linux binary (+export templates) from GitHub releases into the
  sandbox and running it **headlessly** for project import, script-parse checks,
  and pure-logic test scenes (no rendering, no GPU). If the download, disk, or
  headless run fails, those checks simply move to the director's machine — the
  workflow does not depend on them. Sandbox outbound network is restricted, so
  asset downloads for the *game* (Kenney etc.) are also not assumed — the director
  downloads asset packs locally; the AI works from the manifest + file listing.
- ❌ Never provable in the sandbox: driving feel, frame rate on a GTX 960M,
  Vulkan/NVIDIA-driver behaviour on Kali, visual quality, audio mix, gamepad
  feel, editor usability. Any AI statement about these without local evidence
  must be phrased as a hypothesis with a test attached.

### On the director's laptop (Kali Linux + GTX 960M)
- Godot editor (pinned version, official build), Blender (asset intake/conversion),
  Audacity (audio loops) — all free. Local duties: run acceptance checklists,
  drive the benchmarks, record `nvidia-smi`/`vulkaninfo`/Godot version outputs
  once per environment change, export builds, play like a player and report fun.
- Local test sessions are kept short and checklist-driven (the plan budgets the
  director ≈30–60 min per milestone exit) — open-ended "try it and see" testing
  is a workflow failure, not thoroughness.

### OpenCode Desktop (when unblocked)
Same rules, second seat: local file edits + *local* headless Godot runs become
automatable on the real machine (import checks, test scenes, exports) — but GPU
perf and feel still require the director actually driving. Whichever AI tool is
used, the branch/tag/evidence discipline above is unchanged, and only one AI
writes to a branch at a time.

## 4. Anti-patterns banned by this workflow

- Generating a giant codebase before the architecture/milestone is approved.
- Marking anything "done/tested" without the LOCAL-VERIFIED label + evidence.
- Fixing bugs by rewriting whole systems instead of from a log line.
- Importing an asset "temporarily" without a manifest row.
- Engine/addon upgrades mid-milestone ("while we're at it…").
- Tuning car handling against anything except the frozen physics-regression bars
  + director feel notes.
