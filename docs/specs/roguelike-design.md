# Roguelike design — the frame

Status: draft — frame only
Date: 2026-11-08
Batch: B2

This document holds the shape, not the answers. Every section states what has
to be decided and the test that says it is decided. A section with an answer
but no test is not decided. A section with a test and no answer is the to-do
list.

Two words first, because they are easy to mix up:

- **Theme** is what the story is about. Both packs are 修仙.
- **Genre** is the shape of play. `cultivation` is linear reading;
  `cultivation-rogue` is dispatch management.

The design baseline calls this the framework / unit / accumulation split. The
engine calls it a `genre` pack. Same thing.

## How to use this document

1. Fill a section only when its test can be run.
2. If a decision needs something the engine does not have, it goes to the
   capability request list — not into a data file that cannot carry it.
3. One home per fact. Appendix C says where each fact lives; every other file
   links instead of copying.
4. Appendix A is the way back: it maps every decision group to the section that
   owns it.

# Part 1 — the seven slots

## 1. Meta

To decide:

- platform and input
- audience
- tone: cold and strange, or bright and comic
- one run, in minutes
- one unit of challenge, in minutes
- languages shipped

Done when: one sentence names who plays, on what, and for how long — and
someone who hears it can repeat it.

## 2. Profession pack

To decide:

- realm ladder and the breakthrough points
- the term list: realms, energy, sects, tribulation
- sects and factions that exist in the world
- lifespan and what aging does

Done when: someone who has not read this document can follow 炼气, 筑基, 金丹,
and the three words are used the same way in every text file.

## 3. Genre pack

To decide:

- framework layer: how a run advances
- unit layer: what one challenge is
- accumulation layer: what makes you stronger
- why this combination, not another

Done when: each layer answers "what is the player doing this minute" without
referring to another layer.

## 4. Mechanism mods

To decide:

- which mods this pack carries (for example a system panel, or a
  believed-technique layer)
- which already-declared fields each mod touches
- what each mod does **not** do

Done when: no mod adds a resource, an action, a card shape or a field. It only
reinterprets what the base pack already declares.

## 5. Content layer

To decide:

- person and tense
- number of viewpoint characters
- voice and information density
- arc length
- how much external consistency the world promises
- pacing of payoffs

Done when: any paragraph taken from the pack can be matched against at least
five of the seven items above.

## 6. Asset pack

To decide:

- scene elements and their style
- term sheet for art
- payoff material
- level material
- prompt format for generated art

Done when: an artist can draw from this section without asking what something
looks like.

## 7. Engine

To decide:

- protocol and the capability list
- which data file carries which fact
- what is deliberately not built

Done when: every design decision maps to a data file or an existing capability.
Anything that does not map becomes a capability request, with the five
questions from `docs/specs/capabilities.md` answered.

# Part 2 — the loop

## 8. A run

To decide:

- how long a run is, in in-game time and in real minutes
- how many acts
- how many dispatches
- how many waves
- how a run ends and what is settled

Done when: a run can be told in thirty seconds and the listener can repeat it.

## 9. Dispatch

To decide:

- who can be sent
- where they can be sent
- what they carry
- what comes back
- what changes in a disciple: injury, doubt, greed, loyalty

Done when: every dispatch changes at least one disciple's state, not only the
ledger.

## 10. The lie

To decide:

- who lies to the player, and why
- what "believe", "doubt" and "turn it back" each do
- how believed techniques stack
- what believing costs

Done when: the same lie, believed in two different combinations, produces two
different effects.

## 11. Death and return

To decide:

- what death is in this world
- what is lost
- what carries across runs

Done when: a player can say why this run failed and what they will change next
time.

## 12. Randomness

To decide:

- what is random: disciples, sites, lies, events
- at which layer randomness is rolled
- what is guaranteed, and what is never rolled

Done when: two runs open differently, and both can be won.

## 13. Difficulty curve

To decide:

- what the first hour looks like
- what the third hour adds
- what the tenth hour adds
- where the numbers stop growing

Done when: each of those three windows introduces something that was not there
before, and the last one does not rely on bigger numbers alone.

# Appendix A — where each decision lives

| Group | Decisions | Lives in | Also appears in |
|---|---|---|---|
| A Positioning | platform, audience, tone, run length, unit size, languages | §1 | — |
| B World and story | premise, energy rules, taboos, geography, timeline, protagonist, three-act outline, truth, voice, text budget | §2 (terms and realms only), §8 (act outline) | `shared/world.md`, `shared/terms.json` |
| C Realms and growth | ladder, breakthroughs, formulas, per-run vs across runs, meta list, inflation | §2, §11, §13 | `shared/realms.json` |
| D Play loop | run structure, decision points, death, randomness, resources, checks, builds, curve, save meaning | §3, §8–§13 | — |
| E Content library | sites, encounters, items, enemies, events, terms, names, hooks | §2, §6, §10 | `roguelike-dungeon.md` |
| F Presentation | 2D shape, resolution, UI, motion, audio, size budget | §1, §6, §7 | — |
| G Engineering | pack boundary, protocol, capabilities, data map, CI, release, compatibility | §3, §7 | `cultivation-rogue-pack.md`, `roguelike-roadmap.md` |
| H Governance | batch split, acceptance, document homes | not in this document | batch cards, `docs/process/` |

# Appendix B — reverse index

| Section | Asked by |
|---|---|
| §1 | A, F |
| §2 | B, C, E |
| §3 | D, G |
| §4 | D |
| §5 | B, E |
| §6 | E, F |
| §7 | D, F, G |
| §8 | B, D |
| §9 | D |
| §10 | D, E |
| §11 | C, D |
| §12 | D |
| §13 | C, D |

# Appendix C — single source of truth

| Fact | Only home | Elsewhere |
|---|---|---|
| the seven slots, the loop, the group map | this document | — |
| world, terms, realm table | `shared/world.md`, `shared/terms.json`, `shared/realms.json` | link only |
| site schema | `roguelike-dungeon.md` | link only |
| pack identity, data map, naming | `cultivation-rogue-pack.md` | summary in README |
| version ladder | `roguelike-roadmap.md` | batch cards cite it |
| why a second pack | `decisions/0003-new-pack-for-the-roguelike.md` | — |
| batch scope and acceptance | batch cards | this document does not track progress |

# Appendix D — what this document is not

- It is not a schedule. Batches own the order; `roguelike-roadmap.md` owns the
  versions.
- It is not a story bible. That is `shared/world.md`.
- It is not a capability list. That is the engine's, and this pack only names
  what it needs.
