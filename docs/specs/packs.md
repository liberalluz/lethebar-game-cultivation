# Packs in this repository

One row per pack. A pack's version moves when its content moves, not when the
repository's tooling moves; the tag on the release page is the authority when
this table and a release disagree, and the disagreement is a bug.

| Pack | Kind | Version | Released | What it is |
|---|---|---|---|---|
| `cultivation` | bundle | 1.0.1 | yes | The five-node linear story, in Chinese and English |
| `cultivation-rogue` | bundle | 0.6.1 | yes | The dispatch experiment: first act, inner voice, four endings |

Both packs declare the same collection, `cultivation` with the names `修仙` and
`Cultivation`, so the engine draws one world row and offers both bundles under
it. The ids are stable; the visible names may change without touching a save.

## Adding a pack

Add a row to the table above, add the pack under `packs/<id>/`, and release it
with the tag `pack/<id>/v<version>`. Nothing else in this file changes: the
version column is the only place a version is written down outside the manifest
itself.

## What is deliberately not here

- Release dates. The releases page has them, and they are not evidence of
  anything a reader of this table needs.
- A count of nodes, choices or endings. Those belong to the pack's own spec
  under `docs/specs/`.
