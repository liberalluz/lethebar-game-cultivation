# cultivation-rogue — the pack

Status: shipping — published as `pack/cultivation-rogue/v0.6.2`
Date: 2026-11-12
Batch: B17

`cultivation-rogue` is the second pack in this repository: the same 修仙 world
as `cultivation`, a different genre. `cultivation` is linear reading. This one
is a dispatch game with nine generations inside one run.

## Identity

| Field | Value | Note |
|---|---|---|
| `id` | `cultivation-rogue` | permanent at first release |
| directory | `packs/cultivation-rogue/` | one directory per pack id |
| display names | `names.zh-CN` 修仙·派遣, `names.en` Cultivation: Dispatch | display only |
| version | `0.6.3` | the ladder is in `roguelike-roadmap.md` |
| tag shape | `pack/cultivation-rogue/vX.Y.Z` | the gate publishes on this prefix |
| artifacts | `cultivation-rogue.zip`, `cultivation-rogue-<version>.json` | named from `id` |
| save key | `save:cultivation-rogue:<slot>` | separate from the linear pack |
| collection | `cultivation` (修仙 / Cultivation) | the engine groups the two packs by it |

## What a run is

Act one is twelve nodes (`a1-s01` … `a1-s12`). Two visible beliefs —
`belief_sword` and `belief_body` — rise as the master and the second brother
insist, and turn into `qi` or `insight`. Four inner-voice scenes sit on the same
graph; only the senior sister can hear them, so what a character says and what
that character thinks are two different scenes. The act ends on four possible
endings, and each ending offers one choice: put the three names on the table,
which raises `gate` and leads to `a2-hub`.

Act two is the dispatch loop. `a2-hub` has no choices; the run continues because
the manifest declares a phase machine. Each action is one day. Twelve days make
a year, three years make a generation, nine generations make a run — 324
actions, nine rank titles, one name carved between generations. Three disciples
(`apan`, `aying`, `asu`) can be sent to the herb valley or the ruins, or made to
rest; a field and a wall can be built with stone. A wave arrives every year and
breaks through when the wall is shorter than the generation's threshold. A
disciple whose `injury` reaches 3 does not come back, an empty larder at the end
of a year ruins the sect, and a breached wall ends the run.

Everything is deterministic: the same choices in the same order produce the same
run. There is no dice, no clock outside the turn counter, and no randomness in
act one.

## Envelope

The engine only reads the zip. The rules that matter here:

- the archive root holds `manifest.json` and nothing else; every other file
  starts with `data/`, `assets/` or `i18n/`
- no executable suffix, no symlink, no `..`, no backslash
- 500 entries, 4 MiB per entry, 32 MiB in total
- paths are lower case with `[a-z0-9._/-]`

`infra/checks/check_pack.py` enforces the envelope; `infra/checks/check_pack_data.py`
enforces the data rules below. The gate runs both for every pack in the
repository.

## Layout

```
packs/cultivation-rogue/
├─ manifest.json
└─ data/
   ├─ nodes.json      scenes, choices, inner voice
   ├─ ledger.json     resources: beliefs, turn, qi, insight, gate, stone, wall,
   │                  field, year, day, seat, breach, ruin, and per disciple
   │                  trust_<name>, injury_<name>, greed_<name>
   ├─ actions.json    nine actions: six dispatches, rest, dig_wall, tend_field
   ├─ rules.json      twenty-two ordered rules: beliefs, the calendar, the
   │                  field, the yearly cost, the waves, ruin, the rollover
   ├─ phases.json     three hundred and twenty-four turns, nine ranks, seven
   │                  failures
   └─ i18n/en.json    English cover for every node, choice, action, rank,
                      failure and labeled resource value
```

No other data file exists, and none should be added without a consumer: a data
file the engine does not read is dead weight in the archive.

## Naming

| Thing | Rule | Example |
|---|---|---|
| action id | `^[a-z][a-z0-9_]*$` (engine V-16) | `send_apan_herb`, `dig_wall` |
| resource id | `^[a-z][a-z0-9_]*$` (engine V-14) | `belief_sword`, `trust_apan` |
| node id | `<act>-<scene>`, one hyphenated level | `a1-s01`, `a2-hub` |
| translation key, node | the node id | `en.json` → `"a1-s01"` |
| translation key, choice | `strings` under the node, by index | `en.json` → `a1-s01.choices[0]` |
| translation key, label | `action.<id>`, `rank.<at>`, `failure.<index>`, `resource.<id>.<value>` | `action.dig_wall`, `resource.stone.5` |

Dots and hyphens were acceptable in `0.1.0` and are not acceptable now: the
engine validates action and resource ids against `^[a-z][a-z0-9_]*$` and rejects
the archive otherwise. `0.6.2` is the first build where every id passes.

A node id that reaches a save is permanent. Renaming one is a save break and
needs `saveSchema` + 1.

## Manifest

```json
{
  "id": "cultivation-rogue",
  "version": "0.6.3",
  "specVersion": "2.0.0",
  "kind": "bundle",
  "engine": ">=4.7.0 <5.0.0",
  "names": { "zh-CN": "修仙·派遣", "en": "Cultivation: Dispatch" },
  "defaultLocale": "zh-CN",
  "locales": ["en"],
  "protocol": "linear@1",
  "capabilities": [
    "narrative@1", "text@1", "locale@1", "ledger@1", "rules@1",
    "actions@1", "phases@1", "clock@1", "save@2"
  ],
  "mechanics": ["progress"],
  "entry": "a1-s01",
  "saveSchema": 1,
  "clock": { "per": "turn" },
  "collection": { "id": "cultivation", "names": { "zh-CN": "修仙", "en": "Cultivation" } },
  "meta": { "audience": "teens", "minutes": 22 }
}
```

`linear@1` is still the protocol: act two walks one node with no choices, and
the declared phase machine keeps that node from ending the run. `clock@1` with
`per: turn` is what makes `tick` advance, and every calendar rule reads it.

## Checks the data has to pass

`check_pack_data.py` mirrors the engine's fatal checks that the envelope check
cannot see:

- `V-14`: every resource id matches `^[a-z][a-z0-9_]*$`
- `V-16`: every action id matches the same pattern, has a non-empty `effects`
  array, and limits are only `per_run` or `per_turn`
- every `when`, `set`, `costs` and `requires` names a declared resource
  (`tick` is provided by the engine, `roll.*` and `persist.*` are reserved)
- `V-22`: every label the data declares — `action.*`, `rank.*`, `failure.*`,
  `resource.<id>.<value>` — has a line in `strings`

It prints `ok (N actions, N resources, N references, N of N label lines)` and
exits non-zero on the first violation.

## Build and release

```
python infra/tool/release/pack.py build packs/cultivation-rogue --out dist
python infra/checks/check_pack.py dist/cultivation-rogue.zip
python infra/checks/check_pack_data.py packs/cultivation-rogue
python infra/tool/release/pack.py hash dist/cultivation-rogue.zip
```

The release note lives in `product/release-notes/cultivation-rogue/<version>.en.md`;
`docs/runbooks/release.md` has the rest of the sequence. The gate builds every
`packs/*/` and publishes only on a `pack/*` tag.

## What must not change

- the id, once `pack/cultivation-rogue/v0.1.0` exists
- node ids that have reached a save
- the meaning of a resource once a release reads it
- the linear pack: it stays at `1.0.1`
