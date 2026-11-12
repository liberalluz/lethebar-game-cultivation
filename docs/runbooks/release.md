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

## Compose the changelog

Fragments live in `changelog.d/`, one per change. Fold them into `CHANGELOG.md`
before building, so the notes and the archive describe the same release:

```bash
python infra/tool/release/release.py --root . --check
python infra/tool/release/release.py --root . --write --stream cultivation --version v1.0.0
```

`--stream` names what the version counts, and it becomes the heading:
`## cultivation v1.0.0` for the pack, `## repo v0.1.0` for the repository
itself. A pack release and a repository release are separate lines; the pack
line is the one that must agree with `manifest.json` and the tag.

`--check` validates the pending fragments and fails when there are none — that
is the normal state right after a release. `--write` removes only the fragments
it consumed. The pack's version passed here must equal the one in
`manifest.json` and the tag.

## Write the release note

The text the release page shows is a file in this repository:
`product/release-notes/<id>/<version>.en.md`, one file per pack and version,
English only. Write it before tagging, keep it to what a player needs (what
changed, what still does not work), and pass the same file to
`gh release edit --notes-file` after publishing; `closeout.py --release` then
copies the published body into the evidence directory byte for byte. A note
assembled in two languages, or written after the fact from memory, is how a
release ends up describing a build that does not exist.

## Build and check

```bash
python infra/tool/release/pack.py build packs/cultivation --out dist
python infra/checks/check_pack.py dist/cultivation.zip
python infra/checks/check_pack_data.py packs/cultivation
python infra/tool/release/pack.py hash dist/cultivation.zip
python infra/tool/release/pack.py badge . --check README.md
```

`build` names the archive from the manifest id; `check_pack` reads the archive,
not the tree, and rejects anything the envelope does not allow; `check_pack_data`
reads the tree and rejects ids, references and label lines the engine would
refuse at install time; `hash` writes `dist/cultivation-1.0.0.json` beside it;
`badge --check` fails when the generated table in a README no longer matches the
manifests. A green envelope alone does not mean the archive installs.

Both tools have a self-test, and both run from this repository's copies:

```bash
python infra/tool/release/pack.py self-test
python infra/checks/check_pack.py --self-test
```

The copies are byte-identical to the engine tag recorded in
`infra/vendor.json`, which also states the `ENGINE_REF` the gate checks out.
A copy that drifts from that tag judges packs by rules the engine no longer
has, so re-vendor all four files together and update the record in the same
commit. The envelope caps are the engine's: 500 entries, 4 MiB per entry,
32 MiB unpacked.

## Preflight

`preflight.py` reads a pack **directory** (not the archive) and checks six
things in order: the manifest, the version contract, the archive, the
descriptor, the release, and whether the published asset can be fetched over
the network.

```bash
python infra/tool/release/preflight.py \
  --pack packs/cultivation \
  --repo liberalluz/lethebar-game-cultivation \
  --tag pack/cultivation/v1.0.1
```

```
[1/6] manifest - ok: manifest.json names cultivation
[2/6] version and contract - ok: version 1.0.1, specVersion 2.0.0, engine >=4.7.0 <5.0.0
[3/6] artifact - ok: dist\cultivation.zip (2715 bytes)
[4/6] descriptor - ok: dist\cultivation-1.0.1.json names sha256 2157bf94...
[5/6] release - ok: ... has a release for pack/cultivation/v1.0.1
[6/6] asset over the network - missing: ... answered HTTP 504
preflight: 5/6 item(s) ready
```

The last two items are about the published release, so they can only pass after
`publish` has run; running it before that is how you find out the first four
are fine. Exit code 1 with `5/6` after a real publish means the network, not
the release: in this checkout `github.com` sometimes resolves to an address
that answers `504`, and the check passes again from a machine that can reach the
download endpoint. On Windows the tool may also print a `UnicodeDecodeError`
traceback from its `gh` subprocesses while the six-line report still prints;
that is a decoding warning in the vendored script, not a failed check, and the
copy is kept byte-identical to the engine's.

## Publish

Either let CI do it — push the tag and the `publish` step creates the release
and uploads both assets:

```bash
git tag pack/cultivation/v1.0.0
git push origin pack/cultivation/v1.0.0
```

or publish from the workstation, which creates the tag at the default branch
head if it does not exist yet. The engine's own `publish.py` publishes engine
releases only; a pack is published by `pack.py publish`:

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

## Record the release

The release itself is evidence, not a note to write by hand. `closeout.py`
records it the same way it records a batch:

```bash
python infra/tool/batch/closeout.py --release pack/cultivation/v1.0.1
python infra/tool/batch/closeout.py --release pack/cultivation/v1.0.1 \
  --apply --commit-docs
```

It writes `records/<YYYY-MM>-release-<pack>-v<version>/` with `release.json`
(tag, annotated tag object, tag commit, assets, pack bytes and sha256),
`release-notes.md` fetched back from the published release, and a README; then
it adds the two index rows, corrects the front-page counts, runs the three
checkers, and commits. The notes file it wants is the one that was published;
with no notes file it stops instead of inventing a body.

## Closing a batch

A batch ends when its exit record is frozen in the docs repository, not when the
pull request merges. `infra/tool/batch/closeout.py` runs the seven steps in one
pass: copy the live record into the batch directory, drop the
`freeze-manifest.json` the freezer leaves behind, write the batch README table,
add the index row, correct the two counts on the front page, run the three
checkers, and commit. `--delete-branch <branch>` also removes the merged branch
on origin and locally; it refuses the default branch and any branch an open
pull request still points at.

```bash
python infra/tool/batch/closeout.py --batch 2026-11-B12 --commit a5388dc
python infra/tool/batch/closeout.py --batch 2026-11-B12 --commit a5388dc \
  --apply --commit-docs
```

Without `--apply` it prints the counts it would write and touches nothing. With
`--apply` it stops at the first failed checker and commits nothing, so a record
with a broken section cannot reach the docs repository quietly.

Four habits are cheaper than the mistakes they prevent:

- Run `python infra/checks/check_commit_body.py` on the commit before the push.
  It is the same check the gate runs, and a rejection after the push costs a
  whole CI round trip.
- Merge with a body file, never an empty body:
  `python infra/tool/merge/pr_merge.py --pr 16 --body-only --out dist/body.txt`,
  then `gh pr merge 16 --squash --body-file dist/body.txt`. Squashing with an
  empty body drops the lines the verify step reads.
- Wait on `gh pr checks --watch` instead of a fixed sleep: the watch returns when
  the run ends, and a guessed interval is either early or wasted.
- Delete the remote branch after the merge, because `batch.py` does not.
  `closeout.py --delete-branch <branch>` does it in the same pass as the record;
  for a pull request that is not a batch, the repository's
  `delete_branch_on_merge` setting already covers the usual case.
