# Cultivation

English · [简体中文](README.zh-CN.md)

> A Lethebar world: one story, told two ways.
> The story is data, the rules are the engine's, and this repository is where
> the world lives.

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
<!-- pack-badges:begin -->
![packs](https://img.shields.io/badge/packs-2-6f42c1)
![spec](https://img.shields.io/badge/spec-2.0.0-007ec6)
![engine](https://img.shields.io/badge/engine-%3E%3D4.7.0%20%3C5.0.0-478cbf)

| Kind | Pack | Version | Spec | Engine |
| --- | --- | --- | --- | --- |
| `bundle` | `cultivation` | `1.0.1` | `2.0.0` | `>=4.7.0 <5.0.0` |
| `bundle` | `cultivation-rogue` | `0.6.3` | `2.0.0` | `>=4.7.0 <5.0.0` |
<!-- pack-badges:end -->

## Status

Two packs of one world, both released. `cultivation` carries the five-node
linear story that used to be built into the engine; `cultivation-rogue` is the
dispatch experiment, where a weak master sends stronger disciples out over nine
generations and only one person hears what anyone really thinks. They share the
collection `修仙 / Cultivation`, so the engine's pack page shows one world with
two ways to play.

The table above is generated from the two manifests by
`python infra/tool/release/pack.py badge . --write README.md`; the gate runs the
same command with `--check` and fails when a row drifts. It is the only place
this file states a version — dates live on the
[releases page](https://github.com/liberalluz/lethebar-game-cultivation/releases).

## The story

`packs/cultivation/` holds the five-node story, `x1` to `x5`, about fifteen
minutes end to end. `x1` through `x4` each offer two choices; both choices lead
to `x2` today. That is deliberate: that pack proved the engine loads, advances,
saves and reloads a pack. Branching is a content change, made later, in
`packs/cultivation/data/nodes.json`.

`packs/cultivation-rogue/` is the other way to play. Its first act is twelve
nodes and four endings; two visible beliefs (`belief_sword`, `belief_body`) turn
into `qi` or `insight`, and four inner-voice scenes decide which ending you get.
Only the senior sister hears the inner voice, so the same sentence spoken aloud
can mean two different things. An ending opens the gate to a second act: three
disciples, a field, a wall, and a wave that arrives every year, for nine
generations and three hundred and twenty-four days.

The visible names are `修仙` and `修仙·派遣` in Chinese, `Cultivation` and
`Cultivation: Dispatch` in English. The ids are `cultivation` and
`cultivation-rogue`; a player never sees them.

## Installing a pack

Install the archive from the releases page through the engine's own install
action; how that works, and why a link cannot install one, is in the engine's
[publishing guide](https://github.com/liberalluz/lethebar/blob/main/docs/guide/publishing.md).

The save keys are `save:cultivation:<slot>` and
`save:cultivation-rogue:<slot>`, derived from each manifest id. Saves written by
the old built-in pack (`save:xiuxian:<slot>`) do not carry over; that id changed
once, before any pack had been published.

## Building and releasing

The commands, the tag shape, the pre-publish check and the release evidence are
in [docs/runbooks/release.md](docs/runbooks/release.md); the engine's
[publishing guide](https://github.com/liberalluz/lethebar/blob/main/docs/guide/publishing.md)
is the authority on what a valid archive and a valid release look like. This
repository's gate builds and checks every pack on each pull request, and
publishes only on a `pack/*` tag.

## Project structure

| Path | Holds |
|---|---|
| `packs/cultivation/` | The five-node story: `manifest.json`, `data/nodes.json`, `data/mechanics.json`, `data/i18n/en.json` |
| `packs/cultivation-rogue/` | The dispatch game: `manifest.json`, `data/nodes.json`, `data/ledger.json`, `data/actions.json`, `data/rules.json`, `data/phases.json`, `data/i18n/en.json` |
| `infra/checks/` | The envelope check, the data check, the author-gate check, the commit-body check |
| `infra/tool/release/` | `pack.py`: build, hash, badge, publish; `release.py`: compose the changelog; `preflight.py`: check before publishing |
| `infra/tool/merge/` | `pr_merge.py`: build and verify the squash-merge message |
| `infra/tool/batch/`, `infra/tool/repo/` | Vendored Nebula batch and repository tooling |
| `product/release-notes/` | One note per pack and version, the text the release page shows |
| `docs/` | Specs, decisions, intent, runbooks ([docs/README.md](docs/README.md)) |

The repository root holds only what that table lists, plus the conventional root
files (`README`, `CONTRIBUTING`, `CONTRIBUTING.ai`, `SECURITY`, `LICENSE`,
`CHANGELOG`, `AGENTS`, `.gitignore`, `.gitattributes`, `.nebula-scaffold.json`).

## Documentation

| Looking for | Where |
|---|---|
| What a pack promises | [docs/specs/](docs/specs/) |
| Why this repository exists | [docs/intent/](docs/intent/) |
| What was decided, and what was rejected | [docs/decisions/](docs/decisions/) |
| How to cut a release | [docs/runbooks/](docs/runbooks/) |
| The design source the packs grew from | [design/](design/README.md) |

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
