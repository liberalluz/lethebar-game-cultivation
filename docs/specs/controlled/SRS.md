# Software Requirements Specification — Cultivation packages

Status: draft. First baseline is taken when this batch lands.
Batch: B10
Date: 2026-11-09

This document states what the two packages in this repository must do. It
describes behaviour that already ships (`cultivation@1.0.1`,
`cultivation-rogue@0.4.0`); it is not a plan for new behaviour. Design
landings are in `SDD.md`, tests in `STP.md` and `STD.md`.

## Intent

A player installs one package and reads, or plays, a story about a sect on a
mountain. The engine runs it; this repository supplies only data. So every
requirement below is observable through what the engine shows, what the
archive contains, or what a maintainer can hash — never through the engine's
own source.

## Scope

In scope: what a package is (identity, envelope, locales), what it plays
(linear reading, belief, inner voice, dispatch, the day machine), what it
remembers (saves, collection) and what a release is (tag, archive, descriptor,
CI).

Out of scope, deliberately not requirements of this repository: the engine and
its capabilities; art, sound and fonts (both packages ship no assets); the
other worlds (`lethebar-game-sanguo`); the cross-run nine-emperor meta
(`0.6.0`, not shipped); localisation into languages other than `en`.

## Requirements — P1

| ID | Requirement | Acceptance |
|---|---|---|
| `REQ-001` | Each directory under `packs/` builds one package whose manifest `id` equals the directory name, and no two packages share an id. | Building every pack directory yields one archive each; every archive's manifest id matches its directory name; the ids are distinct. |
| `REQ-002` | An installable archive holds `manifest.json` at its root and nothing else; every other entry sits under `data/`, `assets/` or `i18n/`; no entry is executable, a symlink, or uses `..` or a backslash; an archive holds at most 512 entries, 8 MiB per entry and 32 MiB in total. | A checker accepts both shipped archives and rejects a copy of one that gains a second root file, a symlink, or an entry over a cap. |
| `REQ-003` | A package declares a display name for its default locale and for every locale it lists, and a player sees the name for the current interface language, never the id. | With the interface switched between Chinese and English, the package list shows 修仙 and then Cultivation, and shows no package id. |
| `REQ-004` | For every locale a package declares, every node, every choice label and every label the engine can print from the package's own data has a translation in that locale. | A copy of a package with one node or one label missing from its English table is refused at install; both shipped packages install and show English text on every screen they can reach. |
| `REQ-005` | A linear package starts at its declared entry node, a choice moves the run to the node it names, and a node with no choices ends the run — unless the package declares a phase machine, in which case a node with no choices does not end it. | Playing the linear package from the first screen reaches an end screen after five nodes; in the dispatch package, the gate node offers no choices and the run continues. |
| `REQ-006` | A package that declares progress shows the reader how far the run has come, as visited nodes over total nodes; the package itself carries no rules. | The linear package shows 第 2/5 步 (2/5) on its second node; its rules file declares zero rules. |
| `REQ-007` | The dispatch package records two belief numbers that choices change, and the first act ends in one of four endings selected by those numbers. | Two playthroughs of the first act with opposite replies end on different endings, and the belief numbers recorded at the end differ. |
| `REQ-008` | A scene may carry a second text that only appears when a listener is present, and one choice can change what the listener believes. | The same scene shows different text with the listener present and absent; a run that takes the revealing choice records a different belief than one that does not. |
| `REQ-009` | The dispatch package offers six dispatches and one rest; every dispatch changes at least one disciple's injury, trust or greed; a disciple whose injury is 2 or more cannot be sent, and the refusal names the reason; rest can make a disciple sendable again. | Sending a disciple twice to the ruins leaves them at injury 2 and the next dispatch is refused with a reason that names the injury key; resting once allows the dispatch again. |
| `REQ-010` | The dispatch package gives a run twelve days, three rank titles and one failure per disciple; a run ends in failure when a disciple's injury reaches 3, and the failure names that disciple. | Twelve actions exhaust the days; a disciple at injury 3 ends the run with that disciple's own reason, and the day counter no longer accepts actions. |
| `REQ-011` | Each package saves to three slots under a key built from its id, and a save can be loaded back to the node and ledger state it captured. | A save made in the dispatch package is listed in its own pack only, and loading it returns to the saved node with the same ledger numbers. |
| `REQ-012` | Both packages declare the same collection id and the same collection names, so the interface can group them as one world. | The package list shows both packages under one world entry; a copy with the collection block removed is listed separately. |
| `REQ-013` | A release is a git tag `pack/<id>/v<version>` that carries the built archive and a descriptor recording the archive's sha256. | For a published tag, downloading both assets and hashing the archive reproduces the value stored in the descriptor. |
| `REQ-014` | Every pack directory is built and envelope-checked when main moves, and a rejected archive fails the build. | A commit that breaks a pack turns the workflow red; the current main is green on both packages. |

## Notes

`REQ-006` is the only requirement that names engine behaviour rather than data:
the engine computes the step count from the visited nodes, so a package cannot
get it wrong except by declaring progress it does not want. The phrase stays
because a player can see it.

`REQ-004` is stricter than it reads: the engine treats a missing label as a
fatal install error, not a cosmetic gap. `0.2.0` and `0.3.0` of the dispatch
package failed exactly this way; `0.4.0` is the first version that covers it.
