# cultivation-rogue — the version ladder

Status: draft
Date: 2026-11-08
Batch: B2

The pack starts at `0.1.0` and walks minor versions until `1.0.0`. Every step
is one batch and one pull request. A step is done when its exit line is true,
not when its files exist.

## Ladder

| Version | Batch | What it adds | Exit |
|---|---|---|---|
| `0.1.0` | B3 | a pack that installs: manifest, one entry node, one end node, English cover | the archive builds, passes `check_pack`, installs, walks to the end and saves |
| `0.2.0` | B4 | first act slice: three scenes, believe / doubt / turn, two believed-technique builds, one ending | two players reach different builds and different endings from the same entry |
| `0.3.0` | B6 | inner voice: double text, two characters who hear it, reactions that change | the same spoken line, with a different inner voice, draws a different reply |
| `0.4.0` | next | dispatch: three disciples, three dispatches, injury, doubt, greed | every dispatch changes at least one disciple's state, not only the ledger |
| `0.5.0` | not registered | economy and waves: return multiplier, a wave every three years, end-of-run settlement | the snowball rolls, and the wave can stop it |
| `0.6.0` | not registered | across-run meta: nine disciples who reach the top, a final unlock | the ninth run has a place to end |
| `0.7.0` | not registered | content: eight to ten disciples, twenty dispatches, three waves, three endings | three to five hours of play without a dead end |
| `1.0.0` | not registered | balance and polish | no blocking defect; manual and release notes match the build |

A batch number is assigned when the batch is planned, not when the version is
imagined. The column holds a real number only where a batch already happened,
`next` for the version a batch is being written for now, and `not registered`
for everything after that — a batch inserted in between moves one cell, not a
column of numbers.

## Three-part numbering

| Part | Means | Rule |
|---|---|---|
| major | a contract break: save, protocol or id | `0.x` may break at each minor; after `1.0.0` a break needs `2.0.0` |
| minor | new content or a new mechanism, backward compatible | `0.2.0` → `0.3.0` |
| patch | a fix, no addition | `0.2.0` → `0.2.1` |

Rules that follow:

1. During `0.x`, a save break is allowed, but it must bump `saveSchema` and say
   so in `CHANGELOG.md`.
2. After `1.0.0`, a save break is a major version, not a minor.
3. Tags are never moved. `pack/cultivation-rogue/v0.3.0` is history the moment
   it is published.

## Two version axes

| Axis | Example | Moves when |
|---|---|---|
| pack | `pack/cultivation-rogue/v0.3.0` | something a player can see changed |
| repository | `repo/v0.2.0` | tools, CI, docs or process changed |

`repo/*` does not rebuild a pack; `pack/*` does.

## What is not on the ladder

| Item | Why |
|---|---|
| 2D rendering, `map@1`, `dungeon@1` | engine work, not pack work; a report may be written, no date promised |
| art and audio | no assets yet; after `0.6.0` |
| a genre repository | waits for a second author |
| marketplace listing | waits for a third author |

## The first version that can fail

`0.2.0` is the bet. If the believe / doubt / turn loop is not interesting with
three scenes, stop and rethink before any dispatch work. Everything after
`0.2.0` assumes that loop holds.
