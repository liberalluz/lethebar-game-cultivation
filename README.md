# Cultivation

English · [简体中文](README.zh-CN.md)

> A Lethebar world: one story, told two ways.
> The story is data, the rules are the engine's, and this repository is where
> the world lives.

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Packs](https://img.shields.io/badge/packs-2-6f42c1.svg)](docs/specs/packs.md)
[![Spec](https://img.shields.io/badge/spec-2.0.0-007ec6.svg)](packs/cultivation/manifest.json)
[![Engine](https://img.shields.io/badge/engine-%3E%3D4.7.0%20%3C5.0.0-478cbf.svg)](https://github.com/liberalluz/lethebar)

## Status

Two packs of one world, both released. `cultivation` carries the five-node
linear story that used to be built into the engine; `cultivation-rogue` is the
dispatch experiment, where a weak master sends stronger disciples out and only
one person hears what anyone really thinks. They share the collection
`修仙 / Cultivation`, so the engine's pack page shows one world with two ways to
play.

Versions live in [`docs/specs/packs.md`](docs/specs/packs.md) and on the
[releases page](https://github.com/liberalluz/lethebar-game-cultivation/releases);
this file says what the repository is, not what each pack is at.

## The story

`packs/cultivation/` holds the five-node story, `x1` to `x5`, about fifteen
minutes end to end. `x1` through `x4` each offer two choices; both choices lead
to `x2` today. That is deliberate: that pack proved the engine loads, advances,
saves and reloads a pack. Branching is a content change, made later, in
`packs/cultivation/data/nodes.json`.

`packs/cultivation-rogue/` is the other way to play. Its first act is seven
nodes and four endings; two visible beliefs (`belief.sword`, `belief.body`) turn
into `qi` or `insight`, and four inner-voice scenes decide which ending you get.
Only the senior sister hears the inner voice, so the same sentence spoken aloud
can mean two different things.

The visible names are `修仙` and `修仙·派遣` in Chinese, `Cultivation` and
`Cultivation: Dispatch` in English. The ids are `cultivation` and
`cultivation-rogue`; a player never sees them.

## Installing a pack

The installable form of each pack is its release asset, `<id>.zip`. The engine
reads `manifest.json` from the archive root, validates it, and then interprets
the protocol the manifest declares. A pack is data — the engine never executes
code from inside it.

Download the archive and use the engine's install action. A link on the web
cannot install a pack: the browser's CORS rules stop the engine from reading the
bytes. The two published archives are on the
[releases page](https://github.com/liberalluz/lethebar-game-cultivation/releases).

The save keys are `save:cultivation:<slot>` and `save:cultivation-rogue:<slot>`,
derived from each manifest id. Saves written by the old built-in pack
(`save:xiuxian:<slot>`) do not carry over; that id changed once, before any pack
had been published.

## Build and publish

```bash
python infra/tool/release/release.py --root . --check
python infra/tool/release/release.py --root . --write --stream <stream> --version v<version>

python infra/tool/release/pack.py build packs/<id> --out dist
python infra/checks/check_pack.py dist/<id>.zip
python infra/tool/release/preflight.py --pack packs/<id>
python infra/tool/release/pack.py hash dist/<id>.zip
python infra/tool/release/pack.py publish dist/<id>.zip \
  --repo liberalluz/lethebar-game-cultivation \
  --tag pack/<id>/v<version> --apply
```

`release.py` folds the `changelog.d/` fragments into `CHANGELOG.md` and deletes
only the fragments it consumed; run it first, so the notes and the archive
describe the same release. The stream is `cultivation`, `cultivation-rogue` or
`repo`, and it picks which heading the entry lands under.

`build` names the archive from the manifest id, so the directory name and the id
can never disagree. `check_pack` reads the archive, not the source tree: the root
may hold only `manifest.json`, and everything else lives under `data/`,
`assets/` or `i18n/`. `preflight` takes the pack **directory** and checks the
manifest, the version contract, the archive, the descriptor, and — the last two
— that the release exists and its assets can be fetched. Run it before `publish`
knowing that its last two checks only pass after the release exists. `hash`
writes the descriptor that travels beside the archive. `dist/` is git-ignored and
never committed.

The tag shape is `pack/<id>/v<version>`; the version inside the archive and the
version in the tag must match. Publishing needs `gh` authenticated with write
access to this repository.

CI runs the same steps. `.github/workflows/gate.yml` builds and checks every
pack in `packs/` with the copies of `pack.py` and `check_pack.py` that live in
`infra/`, so the gate and the repository move together. On a `pack/*` tag it also
publishes, and on a pull request it first checks that the branch's commits say
why they exist.

## Commands

| Command | What it does |
|---|---|
| `python infra/tool/release/release.py --root . --check` | Validate the `changelog.d/` fragments without changing anything |
| `python infra/tool/release/release.py --root . --write --stream <stream> --version v<version>` | Fold the fragments into `CHANGELOG.md` and delete the consumed ones |
| `python infra/tool/release/pack.py build packs/<id> --out dist` | Zip the pack into `dist/<id>.zip` |
| `python infra/checks/check_pack.py dist/<id>.zip` | Check the archive against the pack envelope |
| `python infra/tool/release/preflight.py --pack packs/<id>` | Check manifest, contract, archive, descriptor, release and assets |
| `python infra/tool/release/pack.py hash dist/<id>.zip` | Write the `id-version.json` descriptor beside the archive |
| `python infra/tool/release/pack.py publish ...` | Create the release and upload the archive and descriptor |
| `python infra/tool/release/pack.py self-test` | Check the release tool itself |
| `python infra/checks/check_pack.py --self-test` | Check the envelope checker itself |
| `python infra/checks/check_author_gate.py --template .github/workflows/gate.yml` | Check that the CI template still builds, checks, publishes |
| `python infra/checks/check_commit_body.py` | Check that new commits carry `Why:` and `Batch:` |
| `python infra/tool/merge/pr_merge.py --self-test` | Check the merge-message tool itself |

Both `self-test` commands create and remove their own fixtures; they need a
writable repository and nothing else.

## Project structure

| Path | Holds |
|---|---|
| `packs/cultivation/` | The five-node story: `manifest.json`, `data/nodes.json`, `data/mechanics.json`, `data/i18n/en.json` |
| `packs/cultivation-rogue/` | The dispatch experiment: `manifest.json`, `data/nodes.json`, `data/state.json`, `data/rules.json`, `data/i18n/en.json` |
| `infra/checks/` | The pack envelope check, the author-gate check, the commit-body check |
| `infra/tool/release/` | `pack.py`: build, hash, publish; `release.py`: compose the changelog; `preflight.py`: check before publishing |
| `infra/tool/merge/` | `pr_merge.py`: build and verify the squash-merge message |
| `infra/tool/batch/`, `infra/tool/repo/` | Vendored Nebula batch and repository tooling |
| `docs/` | Specs, decisions, intent, runbooks ([docs/README.md](docs/README.md)) |

The repository root holds only what that table lists, plus the conventional root
files (`README`, `CONTRIBUTING`, `CONTRIBUTING.ai`, `SECURITY`, `LICENSE`,
`CHANGELOG`, `AGENTS`, `.gitignore`, `.gitattributes`, `.nebula-scaffold.json`).

## Documentation

| Looking for | Where |
|---|---|
| The packs, their versions and what each one is | [docs/specs/packs.md](docs/specs/packs.md) |
| Why this repository exists | [docs/intent/](docs/intent/) |
| What a pack promises | [docs/specs/](docs/specs/) |
| What was decided, and what was rejected | [docs/decisions/](docs/decisions/) |
| How to cut a release | [docs/runbooks/](docs/runbooks/) |

## Contributing

- Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.
- Changing text or code with AI? Read [CONTRIBUTING.ai.md](CONTRIBUTING.ai.md)
  too: an AI change needs a human reviewer and evidence, and the author cannot
  self-approve.
- Do not edit the story to make a test pass; the two choices that both lead to
  `x2` are intentional.

## Security

See [SECURITY.md](SECURITY.md). The engine treats a pack as untrusted input;
this repository treats the engine's envelope rules as the authority on what a
pack may contain.

## License

The packs in this repository are licensed under the
[Apache License 2.0](LICENSE). Use, modification and redistribution are allowed,
provided the copyright notice and the licence text are kept. The engine that
plays them is licensed separately, in its own repository.

No third-party material is bundled — no font, picture or sound — so there is no
`NOTICE` file. If a pack ever ships an asset that came from somewhere else, its
notice and licence terms arrive in the same pull request.
