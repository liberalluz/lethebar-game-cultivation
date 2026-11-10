# cultivation-rogue — the pack

Status: draft — the pack does not exist yet
Date: 2026-11-08
Batch: B2

`cultivation-rogue` is the second pack in this repository: the same 修仙 world
as `cultivation`, a different genre. `cultivation` is linear reading. This one
is dispatch management.

## Identity

| Field | Value | Note |
|---|---|---|
| `id` | `cultivation-rogue` | permanent at first release |
| directory | `packs/cultivation-rogue/` | one directory per pack id |
| display names | `names.zh-CN` 修仙·派遣, `names.en` Cultivation: Dispatch | display only |
| first version | `0.1.0` | see `roguelike-roadmap.md` |
| tag shape | `pack/cultivation-rogue/vX.Y.Z` | the gate publishes on this prefix |
| artifacts | `cultivation-rogue.zip`, `cultivation-rogue-<version>.json` | named from `id` |
| save key | `save:cultivation-rogue:<slot>` | separate from the linear pack |

## Why a second pack

- The protocol, entry point and save meaning of a linear story and a dispatch
  game do not fit in one manifest without bending both.
- The published pack `cultivation@1.0.0` is frozen; new play must not change
  its behavior.
- Separate ids keep saves, tags and artifacts apart.

See `decisions/0003-new-pack-for-the-roguelike.md`.

## Envelope

The engine only reads the zip. The rules that matter here:

- the archive root holds `manifest.json` and nothing else; every other file
  starts with `data/`, `assets/` or `i18n/`
- no executable suffix, no symlink, no `..`, no backslash
- 512 entries, 8 MiB per entry, 32 MiB in total
- paths are lower case with `[a-z0-9._/-]`

`infra/checks/check_pack.py` enforces all of it; the gate runs it before
publishing.

## Layout

```
packs/cultivation-rogue/
├─ manifest.json
├─ data/
│  ├─ nodes.json          scenes, choices, inner voice
│  ├─ state.json          believed techniques, resources, disciples
│  ├─ rules.json          effects of believed techniques, returns, injury
│  ├─ checks.json         believe / doubt / turn, dispatch outcomes
│  ├─ pools.json          site encounters
│  ├─ phases.json         acts, waves, end of run
│  ├─ actions.json        dispatch, heal, punish, reward
│  ├─ factions.json       sect and outside relations
│  └─ i18n/en.json        English cover for every node id
└─ assets/                empty until there is art
```

Only `nodes.json` and `manifest.json` exist in `0.1.0`. Every other file is
added by the version that first reads it — a data file with no consumer is
dead weight.

## Naming

| Thing | Rule | Example |
|---|---|---|
| node id | `<act>-<scene>`, lower case | `a1-s01`, `a2-s03` |
| disciple | `d-<name>` | `d-shen` |
| state key | two dotted levels | `faith.body`, `stat.spirit` |
| flag | `flag.` prefix | `flag.told_truth` |
| translation key | the node id, one per node | `en.json` → `a1-s01` |

A node id that reaches a save is permanent. Renaming one is a save break and
needs `saveSchema` + 1.

## Manifest in 0.1.0

```json
{
  "id": "cultivation-rogue",
  "version": "0.1.0",
  "specVersion": "2.0.0",
  "kind": "bundle",
  "engine": ">=4.7.0 <5.0.0",
  "name": "修仙·派遣",
  "names": { "zh-CN": "修仙·派遣", "en": "Cultivation: Dispatch" },
  "defaultLocale": "zh-CN",
  "locales": ["en"],
  "protocol": "linear@1",
  "capabilities": ["narrative@1", "text@1", "locale@1", "save@2"],
  "mechanics": ["progress"],
  "entry": "a1-s01",
  "saveSchema": 1,
  "assets": []
}
```

`linear@1` in `0.1.0` is deliberate: the first version only proves the pipeline.
Dispatch and waves land in `0.4.0` and `0.5.0`; before then, the protocol and the
capability list are checked against the engine's `docs/specs/capabilities.md`,
not assumed.

## Build and release

```
python infra/tool/release/pack.py build packs/cultivation-rogue --out dist
python infra/checks/check_pack.py dist/cultivation-rogue.zip
python infra/tool/release/pack.py hash dist/cultivation-rogue.zip
```

The gate already builds every `packs/*/`; nothing in `.github/workflows/` needs
to change.

## What must not change

- the id, once `pack/cultivation-rogue/v0.1.0` exists
- node ids that have reached a save
- the meaning of a state key once a release reads it
- the linear pack: it stays at `1.0.0`
