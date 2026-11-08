# Changelog

<!-- Released versions, newest first. The release tool owns this file.
     Two streams: `## cultivation vX.Y.Z` is the pack (tag
     `pack/cultivation/vX.Y.Z`); `## repo vX.Y.Z` is this repository itself
     (tag `repo/vX.Y.Z`). -->

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
