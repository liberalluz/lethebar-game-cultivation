# Changelog

<!-- Released versions, newest first. The release tool owns this file.
     One stream per package, plus one for the repository: `## cultivation vX.Y.Z`
     and `## cultivation-rogue vX.Y.Z` are packs (tags
     `pack/<id>/vX.Y.Z`); `## repo vX.Y.Z` is this repository itself
     (tag `repo/vX.Y.Z`). -->

## cultivation-rogue v0.6.0 - 2026-11-10

The first archive that installs. `0.4.0` and `0.5.0` were written and never
published, so this release carries all three steps in one file.

### Added

- A dispatch loop behind the four endings: three named disciples (Apan, Aying and Asu) can be sent to the herb valley or into the ruins, and each trip moves that disciple's injury, trust or greed, not only the stone pile.
- A clock: a run is 324 actions. Once the gate is open a rule counts a day per action and a year every twelfth; `manifest.json` declares `clock.per: turn` and the `clock@1` capability, and the year rules read the engine's `tick`.
- An economy: an herb field pays one, two or three stone a day as it grows, and each year adds one, two or three of upkeep, so a run that never dispatches cannot feed itself.
- Two ways to spend stone: `dig-wall` raises the wall by one for four stone, and `tend-field` breaks one more acre for three. Both are gated on the stone they cost, because the engine pays `costs` without checking them.
- Nine generations in one run: `state.json` gains `seat`, the names on the stone, and `day`, the day inside a generation.
- The rollover: when the third year ends the run seats a name — `seat` gains one, the year and the day start over, the wall gives up three courses, the field gives up two, the granary takes in ten stone, and the three disciples come back whole.
- Waves that read the seat as well as the year: the first three generations ask for a wall of three, six and nine; the next three ask four, seven and nine; the last three ask five, eight and nine.

### Changed

- The four endings of the first act no longer close the run; each one opens the gate and hands the player to the days behind it.
- A disciple at injury 2 or more cannot be sent out, and the menu says so instead of hiding the button.
- `phases.json` runs 324 actions with nine ranks at 1, 37, 73, 109, 145, 181, 217, 253 and 289; the failure list is the three wounds, the granary and the three waves, and no reason names a calendar year any more.
- `stone` keeps its labels, gains a fourth at thirty, and its ceiling rises from twenty to sixty so a good year has somewhere to go.
- `manifest.json` is `0.6.0`. The protocol, the capabilities and the collection block are unchanged.

### Fixed

- The English table names every label the data references — 98 strings, including the nineteen labels of the first act's five values. The engine refuses to install a pack whose locale table leaves a menu label unnamed, which is why `0.3.0` was turned away and why this archive is the first one that installs.

## repo v0.2.0 - 2026-11-08

### Added
- `infra/tool/release/preflight.py`: checks a pack's manifest, version contract, archive, descriptor, release and asset reachability before publishing.
- `docs/specs/packs.md`: the registry of packs, their kinds and versions.

### Changed
- The README describes the world and points to the registry, instead of naming one pack's version in two languages.
- `docs/specs/roguelike-roadmap.md` numbers a batch only where one was planned; later versions read `next` and `not registered`.

### Fixed
- The front page said `v1.0.0, unshipped` after two packs had been released.

## cultivation v1.0.1 - 2026-11-08

### Added
- Both packs now name the same collection, so the pack page draws one world row with two ways to play instead of two rows in the fallback group.

### Changed
- `cultivation` is `1.0.1`. The story, the id and `saveSchema` are unchanged; only the manifest gained the collection block.

## cultivation-rogue v0.3.0 - 2026-11-08

### Added
- The first act has an inner voice: the same spoken line, held two ways, draws two different replies from the one character who can hear it.

## cultivation-rogue v0.2.0 - 2026-11-08

### Added
- The first act of `cultivation-rogue` is playable at `0.2.0`: three scenes, two lies, two builds and four endings.
- `belief`, `qi`, `insight` and `turn` are ledger resources, so the numbers a scene leaves behind are visible in the same place the story is read.

## repo v0.1.0 - 2026-11-08

### Added
- `infra/tool/release/release.py`: composes a release section from `changelog.d/` fragments; `--stream` gives the pack and the repository a line each.
- `docs/runbooks/release.md`: the changelog step, in the order it is run.

### Changed
- `CHANGELOG.md` carries two streams: `## cultivation vX.Y.Z` for the pack and `## repo vX.Y.Z` for everything that only touches this repository.
- The gate runs `check_commit_body.py` on pull requests, and skips pull requests that cannot change a pack.
- Workflow commits are pushed over SSH, after asking the maintainer.

### Fixed
- The two `self-test` commands no longer create `0700` fixture directories, so a sandbox that refuses that mode can run them.
- `changelog.d/README.md` pointed at a `release.py` the repository did not carry; the tool lives in `infra/tool/release/` now.

## cultivation v1.0.0 - 2026-11-08

### Added
- the Cultivation story as a package: five linear nodes under `linear@1`, with an English translation for every node
- the `pack/cultivation/v1.0.0` release, carrying `cultivation.zip` and its descriptor
