# Release runbook

Cutting `pack/<id>/v<version>` from a clean `main`. The archive is built from
the source tree; the descriptor is derived from the archive, so it can never
describe different bytes than the ones that ship.

## Before you start

- `git status` is clean and `main` is level with `origin/main`.
- The version in `packs/<id>/manifest.json` is the version you are about to
  tag; `check_pack.py` and the tag must agree.
- `gh auth status` shows the account that may create releases, with `repo`
  scope. The token must not carry the workflow scope — workflow files are
  edited in the web editor, see §8 of the git conventions.

## Build and check

```bash
python infra/tool/release/pack.py build packs/cultivation --out dist
python infra/checks/check_pack.py dist/cultivation.zip
python infra/tool/release/pack.py hash dist/cultivation.zip
```

`build` names the archive from the manifest id; `check_pack` reads the archive,
not the tree, and rejects anything the envelope does not allow; `hash` writes
`dist/cultivation-1.0.0.json` beside it.

Both tools have a self-test, and both run from this repository's copies:

```bash
python infra/tool/release/pack.py self-test
python infra/checks/check_pack.py --self-test
```

## Publish

Either let CI do it — push the tag and the `publish` step creates the release
and uploads both assets:

```bash
git tag pack/cultivation/v1.0.0
git push origin pack/cultivation/v1.0.0
```

or publish from the workstation, which creates the tag at the default branch
head if it does not exist yet:

```bash
python infra/tool/release/pack.py publish dist/cultivation.zip \
  --repo liberalluz/lethebar-game-cultivation \
  --tag pack/cultivation/v1.0.0 --apply
```

The tag names the release: `pack/<id>/v<version>`. The version in the tag and
the version inside the archive must match, or the release lies about what it
contains.

## Afterwards

```bash
gh release view pack/cultivation/v1.0.0 --repo liberalluz/lethebar-game-cultivation
sha256sum dist/cultivation.zip dist/cultivation-1.0.0.json
```

Compare the first hash with `sha256` in the descriptor, and the second with the
asset GitHub lists. A mismatch means the upload did not carry the file that was
checked.

`dist/` is generated and git-ignored: never commit it, and never cut a release
from a dirty tree.
