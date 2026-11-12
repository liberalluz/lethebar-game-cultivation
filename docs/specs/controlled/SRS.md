# Software Requirements Specification — Cultivation packages

Status: draft. First baseline is taken when this batch lands.
Batch: B12
Date: 2026-11-10

This document states what the two packages in this repository must do. It
describes behaviour that already ships (`cultivation@1.0.1`,
`cultivation-rogue@0.5.0`); it is not a plan for new behaviour. Design
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
other worlds (`lethebar-game-sanguo`); the second act's content volume
(`0.8.0`, not designed yet); localisation into languages other than `en`.

## Requirements — P1

| ID | Requirement | Acceptance |
|---|---|---|
| `REQ-001` | Each directory under `packs/` builds one package whose manifest `id` equals the directory name, and no two packages share an id. | Building every pack directory yields one archive each; every archive's manifest id matches its directory name; the ids are distinct. |
| `REQ-002` | An installable archive holds `manifest.json` at its root and nothing else; every other entry sits under `data/`, `assets/` or `i18n/`; no entry is executable, a symlink, or uses `..` or a backslash; an archive holds at most 500 entries, 4 MiB per entry and 32 MiB in total. | A checker accepts both shipped archives and rejects a copy of one that gains a second root file, a symlink, or an entry over a cap. |
| `REQ-003` | A package declares a display name for its default locale and for every locale it lists, and a player sees the name for the current interface language, never the id. | With the interface switched between Chinese and English, the package list shows 修仙 and then Cultivation, and shows no package id. |
| `REQ-004` | For every locale a package declares, every node, every choice label and every label the engine can print from the package's own data has a translation in that locale. | A copy of a package with one node or one label missing from its English table is refused at install; both shipped packages install and show English text on every screen they can reach. |
| `REQ-005` | A linear package starts at its declared entry node, a choice moves the run to the node it names, and a node with no choices ends the run — unless the package declares a phase machine, in which case a node with no choices does not end it. | Playing the linear package from the first screen reaches an end screen after five nodes; in the dispatch package, the gate node offers no choices and the run continues. |
| `REQ-006` | A package that declares progress shows the reader how far the run has come, as visited nodes over total nodes; the package itself carries no rules. | The linear package shows 第 2/5 步 (2/5) on its second node; its rules file declares zero rules. |
| `REQ-007` | The dispatch package records two belief numbers that choices change, and the first act ends in one of four endings selected by those numbers. | Two playthroughs of the first act with opposite replies end on different endings, and the belief numbers recorded at the end differ. |
| `REQ-008` | A scene may carry a second text that only appears when a listener is present, and one choice can change what the listener believes. | The same scene shows different text with the listener present and absent; a run that takes the revealing choice records a different belief than one that does not. |
| `REQ-009` | The dispatch package offers six dispatches and one rest; every dispatch changes at least one disciple's injury, trust or greed; a disciple whose injury is 2 or more cannot be sent, and the refusal names the reason; rest can make a disciple sendable again. | Sending a disciple twice to the ruins leaves them at injury 2 and the next dispatch is refused with a reason that names the injury key; resting once allows the dispatch again. |
| `REQ-010` | The dispatch package gives a run thirty-six days, three year titles and one failure per disciple; a run ends in failure when a disciple's injury reaches 3, and the failure names that disciple. | Thirty-six actions exhaust the days; a disciple at injury 3 ends the run with that disciple's own reason, and the day counter no longer accepts actions. |
| `REQ-015` | The dispatch package turns one year every twelve days, pays out what the field has grown, charges one stone of upkeep for every year it has entered, and ends a run when a wave finds the wall too low or the store empty. | The thirteenth action reads year 2 and has charged the first year's upkeep; one field level pays a stone on every action after it is built; a run that enters year 2 with fewer than six wall levels ends on that year's breach line; a run that starts a day with an empty store ends on the empty-store line. |
| `REQ-011` | Each package saves to three slots under a key built from its id, and a save can be loaded back to the node and ledger state it captured. | A save made in the dispatch package is listed in its own pack only, and loading it returns to the saved node with the same ledger numbers. |
| `REQ-012` | Both packages declare the same collection id and the same collection names, so the interface can group them as one world. | The package list shows both packages under one world entry; a copy with the collection block removed is listed separately. |
| `REQ-013` | A release is a git tag `pack/<id>/v<version>` that carries the built archive and a descriptor recording the archive's sha256. | For a published tag, downloading both assets and hashing the archive reproduces the value stored in the descriptor. |
| `REQ-014` | Every pack directory is built and envelope-checked when main moves, and a rejected archive fails the build. | A commit that breaks a pack turns the workflow red; the current main is green on both packages. |
| `REQ-016` | A name earned in one run outlives it: a run that ends with a living mountain records one name, and the next run starts with the advantages that count buys, while a run that ends in failure records nothing. | A run that reaches the end of its third year leaves the mountain's name count one higher and the next run starts with one field level already worked; a run that loses a disciple leaves the count and the next run's start unchanged. |
| `REQ-017` | The yearly wave weighs the same every time the same turn is reached: its weight comes from the draw the package declares, and reloading the run does not redraw it. | Reaching a given turn twice, with and without a reload, yields the same wave weight, and that year's tribute equals the weight. |

## Notes

`REQ-016` and `REQ-017` describe `0.7.0`, not the current build: the data
the data still predates them: a reader who checks them against `0.6.3`
will find the older shape, where nothing is remembered between runs. They stay here because they are what
the next build is judged against.

`REQ-006` is the only requirement that names engine behaviour rather than data:
the engine computes the step count from the visited nodes, so a package cannot
get it wrong except by declaring progress it does not want. The phrase stays
because a player can see it.

`REQ-004` is stricter than it reads: the engine treats a missing label as a
fatal install error, not a cosmetic gap. `0.2.0` and `0.3.0` of the dispatch
package failed exactly this way; `0.4.0` is the first version that covers it.

`REQ-015` is settled inside one action: the engine turns the year, pays the
field, charges upkeep and checks the wall in that order, so the wall has to be
standing before the action that crosses a year boundary. A wall raised after the
crossing does not save that year, and the field pays before the upkeep is taken,
so a run can spend its last stone on the field and still lose the store to the
year.
