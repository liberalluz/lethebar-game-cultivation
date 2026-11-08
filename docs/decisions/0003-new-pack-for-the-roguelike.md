# 0003 — A second pack for the dispatch game

Status: accepted
Date: 2026-11-08

## Context

`cultivation` is published at `1.0.0`: a five-node linear story, protocol
`linear@1`, one save key, one artifact name. It is frozen.

The next product is a different shape of play: the player is a master who sends
disciples out, reads what comes back, and keeps a sect alive between waves. The
framework is dispatch management, the unit is a site run, the accumulation is
idle growth. It is the same world and the same 修仙 vocabulary, and it uses the
same engine capabilities — `ledger`, `rules`, `checks`, `phases`, `actions`,
`clock` are all implemented.

A pack id is permanent at its first release: it names the save key, the tag and
the artifacts. A genre is the other permanent thing in a manifest: it decides
what the player does every minute.

## Decision

Add a second pack to this repository:

| Item | Value |
|---|---|
| id | `cultivation-rogue` |
| directory | `packs/cultivation-rogue/` |
| first version | `0.1.0` |
| tag shape | `pack/cultivation-rogue/vX.Y.Z` |
| save key | `save:cultivation-rogue:<slot>` |

The linear pack stays at `1.0.0` and is not touched. The two share a world, a
term list and a realm table; they do not share a manifest, a save or a release.

## Why not extend the linear pack

- `protocol` and `entry` describe one shape of play. A dispatch game under
  `linear@1` would either lie about itself or force the engine to guess.
- Every save would change meaning. `saveSchema` would have to move, and the
  published `1.0.0` players would lose their runs for a game they did not ask
  for.
- The artifact and tag names would have to carry two products at once, which
  makes a release note ambiguous.

## Consequences

- Two packs build and publish independently. The gate already loops over
  `packs/*/`; no workflow change is needed.
- Saves, tags and artifacts stay separate. A player can hold both.
- Both packs may declare the same `collection` so the engine groups them under
  one world; the names must match or the engine warns (`W-04`).
- The world bible, term list and realm table live once, in `shared/`, and both
  packs are written against it.
- The repository now has two artifacts to keep compatible with the engine
  range; the range is declared per pack.

## Alternatives

- **Extend `cultivation` in place** — rejected: it breaks the published pack's
  saves and blurs one shape of play into another.
- **Start a new repository** — rejected: the world, the terms and the tools are
  the same; splitting now would duplicate the release pipeline before there is
  a second author to justify it. The engine's boundary ADR also keeps genre and
  world splits behind a second author.
- **Wait for the engine to grow a dispatch capability** — rejected: everything
  this pack needs already exists; waiting would idle the content work.
