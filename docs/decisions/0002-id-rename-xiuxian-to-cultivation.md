# 0002 — Rename the pack id from xiuxian to cultivation

Status: accepted
Date: 2026-11-07

## Context

The story lived on `split/xiuxian` in the engine repository: manifest id
`xiuxian`, version `0.1.0`, five nodes, no assets. It was never published as a
pack — the engine carried it as built-in content until the split. This
repository is its new home, and the id appears in three permanent places: the
save key `save:<id>:<slot>`, the release tag `pack/<id>/vX.Y.Z`, and the
artifact names `<id>.zip` and `<id>-<version>.json`.

## Decision

Rename the id to `cultivation` everywhere it is structural:

| Item | New value |
|---|---|
| Manifest `id` | `cultivation` |
| Directory | `packs/cultivation/` |
| Tag | `pack/cultivation/vX.Y.Z` |
| Artifacts | `cultivation.zip`, `cultivation-1.0.0.json` |

Display names do not change: `names.zh-CN` stays 修仙, `names.en` stays
Cultivation, and `defaultLocale` stays `zh-CN`.

## Why now

A pack id becomes permanent at its first release. Nothing has been published
under `xiuxian`, so this is the only window in which the rename costs nothing.
After `pack/cultivation/v1.0.0` exists, the id is frozen.

## Consequences

- Saves written by the built-in version, `save:xiuxian:<slot>`, become
  unreachable. That build is not a released pack and no published pack used the
  id, so no third party is affected.
- The source branch keeps its old name `split/xiuxian`; it only supplied
  content and is not referenced by this repository.
- Any script or document that still says `packs/xiuxian` is wrong and is fixed
  in the same change rather than carried forward.

## Alternatives

- Keep `xiuxian` — rejected: the id would be permanent and pinyin in a save key
  and a tag is a lasting cost.
- Use `xiulian` or `xianxia` — rejected: still pinyin, with the same problem.
- Rename after the first release — rejected: not possible without breaking
  every save and every tag.
