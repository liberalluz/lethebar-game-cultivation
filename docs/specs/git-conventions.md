# Git conventions

One-page defaults. Change this file when the team changes the rule.
Detail belongs here, not in `CONTRIBUTING.md`: that file is the door, and a rule
copied into two places drifts in one of them.

## 1. Branches

```text
main                 long-lived
feat/<topic>         user-visible change
fix/<topic>          bug fix
process/<topic>      process or tooling only
```

- One branch = one change.
- Delete the branch after merge.
- `main` is protected: a change lands as a pull request with one approval from
  a code owner, and the branch stays linear. A maintainer cannot push to it,
  including for a workflow file; §8 says how that commit travels.

## 2. Commits

```text
<type>(<scope>): <subject>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`.
Scopes: pick exactly one from the closed list below.

| Scope | Covers |
|---|---|
| `pack` | The pack itself: `packs/<id>/` manifest, nodes, mechanics, translations |
| `infra` | Build and CI: `infra/checks/`, `infra/tool/release/`, `.github/workflows/` |
| `docs` | Everything under `docs/` except this file: specs, decisions, intent, runbooks |
| `repo` | Repository conventions and root files: `README`, `CONTRIBUTING`, `CONTRIBUTING.ai`, `SECURITY`, `LICENSE`, `CHANGELOG`, `AGENTS`, `CODEOWNERS`, `.github/` templates, `changelog.d/`, `.gitignore`, `.gitattributes`, `.nebula-scaffold.json`, `docs/specs/git-conventions.md` |
| `tools` | Vendored Nebula tooling under `infra/tool/`: `batch`, `repo`, `merge` |

- One scope per commit, no second level. `docs(srs)` is not allowed; write
  `docs(docs): add the save-compatibility note`.
- The scope follows what the change is about, not where the file sits:
  `git-conventions.md` lives in `docs/` but its changes are `repo`.
- Vendored tooling splits by who runs it: what the gate runs is `infra`
  (`infra/tool/release/`), what a person runs is `tools` (`batch`, `repo`,
  `merge`).
- Adding a scope means editing this table first, in the same pull request as
  its first use.
- Five scopes cover everything in the repository today: `packs/cultivation/`
  is `pack`; the checks, the release tool and the workflow are `infra`; the
  documentation tree is `docs`; the root files and the templates are `repo`;
  the vendored tooling is `tools`. A `shared/` directory does not exist yet —
  if one appears, for material several packs use, its first change adds a
  `shared` scope to this table.

- Subject is imperative and short.
- Body explains why, not what.
- The body carries two labelled lines, checked by
  `infra/checks/check_commit_body.py`:
  - `Why:` is required: one or more lines saying what problem the commit
    solves. Without it the reason for a change lives only in the pull request,
    which is a different document.
  - `Batch:` is required: `Batch: B<n>` when the commit implements a batch
    card, `Batch: none` when it does not. The card decides scope, so the link
    belongs in history.
- Batch numbers belong to this repository. They start at `B1` and do not
  continue the engine's numbering; a message never cites an engine batch, an
  engine issue number or an engine commit.
- A batch number is assigned by `batch.py plan`, when the card exists. A
  roadmap or a plan never numbers a batch that has not been planned: it writes
  `next` for the one being written now and `not registered` after that, so an
  inserted batch moves one cell instead of a column of numbers.
- Until the split from the engine is finished, commits go straight to `main`
  and no pull request is opened. The pull request flow in §3 and §4 starts
  with the second reviewer.
- The check reads only the commits a branch adds (`origin/main..HEAD`). It
  never rewrites or rejects merged history.
- A squash merge makes a commit that no branch precedes, so the range check
  cannot see it. After merging, judge that one commit directly:
  `python infra/checks/check_commit_body.py --ref origin/main` and
  `python infra/tool/merge/pr_merge.py --verify-only --ref origin/main`.
- No secrets, no generated build output.
- The body is plain text. A commit message is never rendered, so backticks,
  `**bold**` and `__bold__` reach the reader as characters: write `kind`, not
  a backticked `kind`. A fenced block is data and is left alone; the prose
  around it is what a reader takes as the reason.
- Every paragraph is wrapped at 72 columns. A message is read in a terminal,
  in `git log` and in the commit list of a pull request, and none of them
  re-flow a line. `pr_merge.py --body-only` flattens what it writes: inline
  code and bold lose their markers and every paragraph is filled at 72 columns
  before it reaches `gh pr merge --body-file`.

## 3. Pull requests

- From B2 on, a change walks one order: batch card in `process/batches/<id>.md`
  → branch → commits (each with `Why:` and `Batch:`) → pull request → one
  code-owner approval → squash merge → exit record in `records/live/`. B1 and
  earlier landed directly and are not retrofitted.
- One PR = one batch = one behaviour that changed, and how it was verified. Not
  one day of work, and not one commit.
- The PR body is `.github/PULL_REQUEST_TEMPLATE.md`, filled in: summary, impact,
  verification with the lines that decide the outcome, risks and rollback,
  self-check. An empty body, or a template still holding its comments, is a
  blocking fault, not a shortcut — the reviewer has nothing to approve.
- Link the batch card, the issue or the record this PR serves. A PR that cannot
  name its batch is either paperwork (say so in the self-check) or out of order.
- Reference another pull request as a written link. A bare `#<n>` is expanded
  by the renderer into that pull request's title; the written link
  (`[#<n>](https://github.com/<owner>/<repo>/pull/<n>)`) is the only form that
  stays a link and stays a reference.
- Required checks must be green.
- Do not rewrite history after review unless asked.
- Fix the syntax, never the meaning. Deleting a reference or a sentence to make
  a page look right is not a fix.

## 4. Merge

- Squash merge by default.
- A squashed commit takes its subject from the branch commit, so the subject
  stays English and the PR title stays in the PR.
- Pass the body on its own: `pr_merge.py --body-only --pr <n> --out <file>`
  writes what goes into `--body-file`, and `--show` without `--out` writes the
  whole message for reading. Handing the whole message to `--body-file` puts
  the subject on the first body line as well.
- Do not build the body through a shell pipe: the pipe decodes UTF-8 as the
  local code page and turns every character outside ASCII into U+FFFD. `--out`
  writes the file from Python and has no such step.
- The author does not self-approve.
- No direct push to `main`.
- Protection on `main` asks for one approving review, counts code owners only,
  dismisses a stale approval, and keeps history linear. `@liberalluz` and
  `@wilkommel` are the code owners; either can approve the other's pull request.
- A failed check is fixed, not bypassed.
- After merging, run `python infra/tool/merge/pr_merge.py --verify-only`; §2
  says what it reads and why nothing else checks that commit.

## 5. Release

- A change adds one fragment under `changelog.d/`; `release.py --write` folds the
  fragments into `CHANGELOG.md` and removes the ones it consumed. Batches never
  edit `CHANGELOG.md` by hand, and a release without a fragment is a release
  nobody can read.
- `CHANGELOG.md` carries two streams, told apart by the heading: `## cultivation
  vX.Y.Z` counts the pack, `## repo vX.Y.Z` counts everything that only touches
  this repository. `release.py --stream` writes the heading; without it the
  heading is the version alone.
- The pack's version lives in `packs/<id>/manifest.json`.
- Tags: `pack/<id>/vX.Y.Z` for a pack release, `repo/vX.Y.Z` for a repository
  release. The version in a pack tag and the version in the manifest must match.
- The archive is named from the manifest id; the descriptor `<id>-<version>.json`
  travels beside it and both are uploaded to the release.
- `dist/` is generated and git-ignored. A release is cut from a clean tree.
- CI publishes on a `pack/*` tag; a local publish is the same two assets.

## 6. Language

- `README`, `CONTRIBUTING` and `SECURITY` exist in English and Chinese; the
  English file is authoritative and the Chinese file carries a
  `translation-of` marker.
- `docs/` is English; a translation is `<name>.zh-CN.md` in the same directory.
- Commit subjects and bodies are English, including the squashed commits on
  `main`.
- The pull request template stays English. So does the body written from it:
  `language.external` is `en-US`, and the body follows the batch card, which is
  English.
- A prepared body carries a translation for every `supported` locale other than
  `external`; here that is `zh-CN`. `batch.py pr --prepare` writes both under
  `.batch/<id>/`: `pr-body.md`, `pr-body.<locale>.md`, and
  `pr-body.manifest.json` with the body's sha256. `.batch/` is local execution
  state, never committed, and pasting the translation into the pull request is a
  person's step, not the tool's.
- The translate hook reads `LETHEBAR_TRANSLATION_FILE` first: point it at a
  finished translation and no API key is needed. Without that variable the hook
  falls back to the API and fails when neither is present.
- `check_translation.py` turns the batch red when a prepared body has no
  manifest, when the body changed after the last prepare, or when a listed
  translation is missing or empty.

## 7. Generated files

| Kind | Examples | Tracked |
|---|---|---|
| Written by a person | `*.json`, `*.md`, `*.py`, `.github/workflows/*.yml` | yes |
| Produced by a tool | `dist/`, `.agents/skills/`, `.codex/`, `.nebula-skills.json`, `__pycache__/` | no; the ignore rule lands in the same pull request |

- Run `git status` after any build or install. An untracked file is either a
  new source file to add or a generated file to ignore; it is never left
  unexplained.

## 8. Workflows

A workflow file can read the repository's secrets and run arbitrary commands,
so GitHub guards it with a scope of its own. This repository answers by never
giving a command-line token that scope.

- A commit that touches `.github/workflows/` goes over SSH, not with the `gh`
  token: `git push git@github.com:liberalluz/<repository>.git <branch>:<branch>`,
  then a pull request. SSH authenticates the person, so the OAuth restriction
  does not apply to it.
- Since `main` is protected, that pull request takes the same one approval as
  any other. A workflow change no longer reaches `main` without a second person
  reading the diff; the SSH route only carries it to the branch.
- Never `gh auth refresh -s workflow`. `gh auth status` shows `gist`,
  `read:org`, `repo` — and nothing else. A rejected HTTPS push of a workflow
  commit is the rule working, not a defect to work around.
- Without an SSH key, fall back to the GitHub web editor on the branch, then
  `git fetch` and `git merge --ff-only`. Never reset over the editor's commit,
  and never re-create the file locally to "keep the tree level".
- The rest of §2 still applies: the subject keeps its shape, and a change that
  touches only the workflow is `ci(infra)`.
