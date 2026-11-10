# Software Design Description — Cultivation packages

Status: draft. Describes what ships as `cultivation@1.0.1` and
`cultivation-rogue@0.5.0`.
Batch: B12
Date: 2026-11-10

Requirements are in `SRS.md`. This document says where each one lands: which
file, manifest field or data key carries it. It is a map, not a rationale —
the reasons are in `docs/decisions/` and in the pack specs under
`docs/specs/`.

## Mapping

| REQ | Design |
|---|---|
| `REQ-001` | One directory per id under `packs/`, and `manifest.id` repeated inside it. `infra/tool/release/pack.py` takes the directory as the build unit and names the archive from `manifest.id`. |
| `REQ-002` | `infra/checks/check_pack.py` — `MAX_ENTRIES = 512`, `MAX_FILE_BYTES = 8 * 1024 * 1024`, `MAX_TOTAL_BYTES = 32 * 1024 * 1024`; the root allowlist is the single name `manifest.json`. |
| `REQ-003` | `manifest.names` (one key per locale), `manifest.defaultLocale`, `manifest.locales`. The engine prints `names[currentLocale]`. |
| `REQ-004` | `data/i18n/<locale>.json` — one entry per node id, each with `text` and `choices`, plus a `strings` map for every label the engine can print (`resource.<id>.<value>`, `action.<id>`, `rank.<n>`, `failure.<n>`). |
| `REQ-005` | `manifest.protocol: "linear@1"`, `manifest.entry`, and `data/nodes.json` where each choice carries `next`. A node with `choices: []` ends the run unless `data/phases.json` exists. |
| `REQ-006` | `manifest.mechanics: ["progress"]` in both packs; `packs/cultivation/data/mechanics.json` holds `{"rules": []}` so the linear pack declares progress and no rules. |
| `REQ-007` | `data/state.json` resources `belief.sword` and `belief.body` (0..3), `data/rules.json` three rules that read them, and the four ending nodes in `data/nodes.json`. |
| `REQ-008` | A second node graph, not a text field: the listener choices lead to `a1-voice-sword-believe`, `a1-voice-sword-turn`, `a1-voice-body-believe`, `a1-voice-body-turn`, each a scene only that listener produces. |
| `REQ-009` | `data/actions.json` — six `send-*` and one `rest`; every `send-*` writes `stone` plus `injury.<d>` and one of `trust.<d>`/`greed.<d>`; every dispatch carries `requires` on `gate >= 1` and `injury.<d> <= 1`. |
| `REQ-010` | `data/phases.json` — `turns: 36`, ranks at days 1/13/25, three `fail` rules on `injury.<d> >= 3`, one on `ruin` and three on `breach`; `packs/cultivation-rogue/data/nodes.json` `a2-hub` with `choices: []` is kept alive by the declared machine. |
| `REQ-015` | `manifest.clock: {"per": "turn"}` with `clock@1` in `capabilities`; `data/rules.json` — three `tick >= 12/24/36` rules that set `year`, three `field >= 1/3/6` rules that add a stone each, three `year >= 1/2/3` rules that take one each, three `[year >= N, wall < 3/6/9]` rules that set `breach`, and one `[year >= 1, stone <= 0]` rule that sets `ruin`; `data/actions.json` `dig-wall` (4 stone) and `tend-field` (3 stone) as the only ways to raise `wall` and `field`. |
| `REQ-011` | `manifest.saveSchema: 1` in both packs; the engine builds the slot key from `manifest.id`, so `cultivation` and `cultivation-rogue` never see each other's saves. |
| `REQ-012` | `manifest.collection` with the same `id` (`cultivation`) and the same `names` in both manifests; the engine groups by `collection.id`. |
| `REQ-013` | `.github/workflows/gate.yml` publishes on a `pack/<id>/v*` tag; `pack.py build` writes the archive and `pack.py hash` writes `<id>-<version>.json` holding the sha256. |
| `REQ-014` | `.github/workflows/gate.yml` loops `packs/*/` through `pack.py build` and `check_pack.py`, failing the job on the first rejection. |

## Repository shape

Three kinds of content, three homes: `packs/<id>/` is the product,
`infra/` is the tooling the gate runs, `docs/` is the description. A batch
changes one of them at a time; the allowed-paths list in the batch card is
what makes that enforceable rather than aspirational.

## Package envelope

`check_pack.py` is the only authority on what an archive may contain, and it
reads the zip without extracting it. Two consequences shape the packs: no pack
may carry a second root file (so `README.md` inside a pack is not possible),
and the per-file cap is 8 MiB, which is why both packs are under 8 KiB today.

## Locale coverage

`data/i18n/en.json` is a translation of the Chinese text that lives in
`nodes.json`. The engine merges them at load time and treats a missing node or
a missing label as fatal, not cosmetic. Labels come from state resources,
actions, ranks and failures, which is why `strings` exists in `0.4.0` and not
before: the `0.3.0` pack declared labels (resources) it never translated.

## Linear play

`linear@1` reads `nodes.json`, draws `text`, offers `choices`, and follows
`next`. The linear pack's five nodes are one chain; its two choices on most
nodes point at the same next node on purpose, because the batch that wrote
them proved the pipeline, not the branching. Branching lives in the dispatch
pack.

## Belief and inner voice

Belief is two bounded numbers (`0..3`), changed by choice effects and read by
three rules. The inner voice is a second graph: four scenes that only the
listener's presence unlocks. This is a deliberate design landing — the engine
has no parallel-text primitive, so "he hears what you do not say" is modelled
as extra nodes rather than extra lines.

## Dispatch loop

A dispatch is an action with costs in injury and returns in stone, trust and
greed. Three disciples make the choice legible: the same site pays differently
depending on who goes. The refusal path is data, not code: `requires` on
`injury.<d> <= 1` makes the engine grey the button and print the reason.

Two more actions spend stone without sending anyone: `dig-wall` and
`tend-field`. Both are gated with `requires` on the price rather than by `costs`
alone, because the engine does not refuse an action whose costs exceed the
store — it applies the cost and clamps the result at zero.

## Day machine

Thirty-six turns, three years, five ways to fail. The gate node is the hinge:
it has no choices, so under a pure linear reading it would end the run.
Declaring `phases.json` changes that — the machine owns the ending, and the hub
stays alive while days remain. The ranks sit at days 1, 13 and 25 because that
is where the years turn; the engine prints a rank as a title, never as a gate.

The clock is what makes the years real. `clock.per` is `turn`, so every action
bumps `tick`; a rule turns `tick >= 12` into `year 1`. The economy hangs off
`year` and runs in file order inside the single action that ends the day: the
year turns, the field pays, upkeep is charged, the wave is checked, then the
store is checked. That order is why a wall has to be standing before the day
that crosses a year, and why a run can pay itself one last stone before the
year takes it.

## Saves and collection

`saveSchema: 1` in both packs. The schema is a promise about field meaning, not
about layout: node ids that reach a save are permanent, and a rename needs
`saveSchema` + 1. The collection block is metadata only; it changes grouping,
never play.

## Release and CI

A release is a tag plus two assets. The gate builds every pack on push, so a
broken pack cannot reach `main` silently; the tag job reuses the same two
commands, which is why a local build and a released archive hash the same.
