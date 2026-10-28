# car-game — CAP SIROCCO: Open Road (working title)

**Status: PLANNING ONLY (2026-10-28). No game code exists yet, and nothing has
been tested.** Zero-budget 3D open-world driving demo in Godot 4, designed
first for a GTX 960M laptop, built AI-first with a human director approving
every milestone. All assets CC0/MIT with recorded licence evidence.

## Planning pack (start here)

| Doc | Contents |
|---|---|
| [docs/TDD.md](docs/TDD.md) | Game concept, minimum playable demo, Godot 4 architecture, project folder structure, decisions D-01…D-08 awaiting approval |
| [docs/ASSET_SHORTLIST.md](docs/ASSET_SHORTLIST.md) | Free CC0/MIT cars, city kits, textures, audio & addons — with licence evidence links and the Asset Intake Gate |
| [docs/PERFORMANCE_STRATEGY.md](docs/PERFORMANCE_STRATEGY.md) | GTX 960M budgets (720p60 Low contract) and scalable graphics presets |
| [docs/TEST_PLAN.md](docs/TEST_PLAN.md) | Test levels L0–L5: static, headless, physics regression, performance, UX acceptance, export smoke |
| [docs/AI_WORKFLOW.md](docs/AI_WORKFLOW.md) | Arena-sandbox ⇄ local-laptop loop, what can honestly be automated where, version-preservation rules |
| [docs/MILESTONES_AND_RISKS.md](docs/MILESTONES_AND_RISKS.md) | Milestones M0–M7 with acceptance criteria + risk register |
| [docs/FIRST_MILESTONE.md](docs/FIRST_MILESTONE.md) | The exact first implementation step (M0+M1: prove the machine, prove the car) — starts only after director approval |

Next action: director reviews the planning pack and approves/amends decisions
D-01…D-08 in the TDD. No implementation begins before that gate.
