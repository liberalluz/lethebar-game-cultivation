# The Cultivation pack

`packs/cultivation/` is the whole story: five nodes, one choice per node, no
assets. The engine reads the manifest; everything a player sees is under `data/`.

## Identity

| Field | Value | What depends on it |
|---|---|---|
| `id` | `cultivation` | The save key is `save:<id>:<slot>`. Renaming it orphans old saves; see ADR 0002. |
| `version` | `1.0.0` | Must match the tag `pack/cultivation/v1.0.0`, and the descriptor name `cultivation-1.0.0.json`. |
| `specVersion` | `2.0.0` | The envelope version `check_pack.py` checks the archive against. |
| `protocol` | `linear@1` | One node, one choice, the next node; a node with no choices ends the run. |
| `mechanics` | `["progress"]` | Read-out only: the engine reports `visited / nodes`, it does not gate anything. |
| `engine` | `>=4.7.0 <5.0.0` | The range this pack was written for. |
| `entry` | `x1` | Where a new run starts. |
| `saveSchema` | `1` | Bump it only together with a migration; see the save note below. |
| `locales` | `["en"]` | Each declared locale needs a full translation table. |
| `assets` | `[]` | Empty on purpose. Adding an entry means adding the file in the same change. |

Display names are `names.zh-CN: 修仙` and `names.en: Cultivation`; the player
sees `names[locale]`, never the id. `defaultLocale` is `zh-CN`, so the text in
`nodes.json` is Chinese and `i18n/en.json` carries the English.

## The five nodes

`data/nodes.json` is `{"nodes": [...]}` with `x1` … `x5`:

- `x1` → `x2`, `x2` → `x3`, `x3` → `x4`, `x4` → `x5`; each of the first four
  has two choices.
- Every pair of choices points at the same next node. That is deliberate: this
  batch proves choose, walk, save and load; branching is a content change, not
  a mechanics change.
- `x5` has `"choices": []` and ends the run.

The progress read-out is `steps / nodes` over the nodes actually visited, so
adding or removing a node changes "step N of M" without touching code.

## Translations

`data/i18n/en.json` is keyed by node id, each value holding `text` and
`choices` as a list of strings in the same order as `nodes.json`. A node id in
`nodes.json` without an entry in a declared locale is a broken pack; keep the
two files in step when a node is added or renamed.

## Saves

The engine stores a session snapshot under `save:cultivation:<slot>`: current
node, visited nodes, state values, random seed and assembly information. Two
rules follow:

- Do not delete a field or change what it means without bumping `saveSchema`.
- Do not change `id` again. `save:xiuxian:<slot>` is already unreachable; see
  ADR 0002 for why that one rename was allowed.

## What not to change

- Node ids `x1` … `x5`: they are the keys of `en.json`.
- `assets`: a non-empty list needs real files in the archive.
- `capabilities`: `render.2d@1` and `text@1` are the whole set this pack uses.
- `mechanics`: the rules table is empty; adding a rule changes gameplay and
  needs its own change, not a rename.
