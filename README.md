# Cultivation

English · [简体中文](README.zh-CN.md)

> A Lethebar pack: five realms, one choice at a time.
> The story is data, the rules are the engine's, and this repository is the
> story's only home.

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Pack](https://img.shields.io/badge/pack-cultivation-c0392b.svg)](packs/cultivation/manifest.json)
[![Version](https://img.shields.io/badge/version-1.0.0-97ca00.svg)](https://github.com/liberalluz/lethebar-game-cultivation/releases/tag/pack/cultivation/v1.0.0)
[![Spec](https://img.shields.io/badge/spec-2.0.0-007ec6.svg)](packs/cultivation/manifest.json)
[![Engine](https://img.shields.io/badge/engine-%3E%3D4.7.0%20%3C5.0.0-478cbf.svg)](https://github.com/liberalluz/lethebar)

Protocol: `linear@1` — one node, one choice, the next node; a node with no
choices ends the run.

## Status

**v1.0.0, unshipped.** The pack holds the full five-node story in Chinese and
English, ready to be built into the archive the engine installs. It is the
story that used to live inside the engine as a built-in; from engine `v0.6.0`
on, built-in stories are gone and a pack like this one is the only way to
carry it.

- `mechanics`: `progress` — the engine reads the step count from the visited
  nodes; the pack declares no rules of its own (`data/mechanics.json` is empty).
- `locales`: `zh-CN` (default) and `en`; every node has an English line.
- No assets. No pictures, no sound, no font — the engine draws the text with its
  own font, so the pack carries none.

## The story

Five nodes, `x1` to `x5`, about fifteen minutes end to end. `x1` through `x4`
each offer two choices; both choices lead to `x2` today. That is deliberate:
this batch proves the pack loads, advances, saves and reloads. Branching is a
content change, made later, in `packs/cultivation/data/nodes.json`.

The visible name is `修仙` in Chinese and `Cultivation` in English. The id is
`cultivation`; a player never sees it.

## Using the pack

The installable form is the release asset `cultivation.zip`. The engine reads
`manifest.json` from the archive root, validates it, and then interprets the
protocol the manifest declares. A pack is data — the engine never executes code
from inside it.

The save key is `save:cultivation:<slot>`, derived from the manifest id. Saves
written by the old built-in pack (`save:xiuxian:<slot>`) do not carry over; the
id changed once, before any pack had been published.

## Build and publish

```bash
python infra/tool/release/release.py --root . --check
python infra/tool/release/release.py --root . --write --version v1.0.0
python infra/tool/release/pack.py build packs/cultivation --out dist
python infra/checks/check_pack.py dist/cultivation.zip
python infra/tool/release/pack.py hash dist/cultivation.zip
python infra/tool/release/pack.py publish dist/cultivation.zip \
  --repo liberalluz/lethebar-game-cultivation \
  --tag pack/cultivation/v1.0.0 --apply
```

`release.py` folds the `changelog.d/` fragments into `CHANGELOG.md` and deletes
only the fragments it consumed; run it first, so the notes and the archive
describe the same release. `build` names the archive from the manifest id, so the directory name and the
id can never disagree. `check_pack` reads the archive, not the source tree: the
root may hold only `manifest.json`, and everything else lives under `data/`,
`assets/` or `i18n/`. `hash` writes the descriptor that travels beside the
archive. `dist/` is git-ignored and never committed.

The tag shape is `pack/<id>/v<version>`; the version inside the archive and the
version in the tag must match. Publishing needs `gh` authenticated with write
access to this repository.

CI runs the same three steps. `.github/workflows/gate.yml` builds and checks with
the copies of `pack.py` and `check_pack.py` that live in `infra/`, so the gate
and the repository move together. On a `pack/*` tag it also publishes.

## Commands

| Command | What it does |
|---|---|
| `python infra/tool/release/release.py --root . --check` | Validate the `changelog.d/` fragments without changing anything |
| `python infra/tool/release/release.py --root . --write --version v1.0.0` | Fold the fragments into `CHANGELOG.md` and delete the consumed ones |
| `python infra/tool/release/pack.py build packs/cultivation --out dist` | Zip the pack into `dist/cultivation.zip` |
| `python infra/checks/check_pack.py dist/cultivation.zip` | Check the archive against the pack envelope |
| `python infra/tool/release/pack.py hash dist/cultivation.zip` | Write the `id-version.json` descriptor beside the archive |
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
| `packs/cultivation/` | The pack: `manifest.json`, `data/nodes.json`, `data/mechanics.json`, `data/i18n/en.json` |
| `infra/checks/` | The pack envelope check, the author-gate check, the commit-body check |
| `infra/tool/release/` | `pack.py`: build, hash, publish; `release.py`: compose the changelog |
| `infra/tool/merge/` | `pr_merge.py`: build and verify the squash-merge message |
| `infra/tool/batch/`, `infra/tool/repo/` | Vendored Nebula batch and repository tooling |
| `docs/` | Specs, decisions, intent, runbooks ([docs/README.md](docs/README.md)) |

The repository root holds only what that table lists, plus the conventional root
files (`README`, `CONTRIBUTING`, `CONTRIBUTING.ai`, `SECURITY`, `LICENSE`,
`CHANGELOG`, `AGENTS`, `.gitignore`, `.gitattributes`, `.nebula-scaffold.json`).

## Documentation

| Looking for | Where |
|---|---|
| Why this repository exists | [docs/intent/](docs/intent/) |
| What the pack promises | [docs/specs/](docs/specs/) |
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

This pack is licensed under the [Apache License 2.0](LICENSE). Use, modification
and redistribution are allowed, provided the copyright notice and the licence
text are kept. The engine that plays it is licensed separately, in its own
repository.

No third-party material is bundled — no font, picture or sound — so there is no
`NOTICE` file. If the pack ever ships an asset that came from somewhere else,
its notice and licence terms arrive in the same pull request.
