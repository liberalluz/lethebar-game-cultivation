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

- One PR = one behaviour that changed, and how it was verified.
- Not one day of work, and not one commit.
- Fill the PR template; no placeholders.
- Link the issue or record if one exists.
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
- A failed check is fixed, not bypassed.
- After merging, run `python infra/tool/merge/pr_merge.py --verify-only`; §2
  says what it reads and why nothing else checks that commit.

## 5. Release

- The pack's version lives in `packs/<id>/manifest.json`.
- Tag: `pack/<id>/vX.Y.Z`; the version in the tag and the version in the
  manifest must match.
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

## 7. Generated files

| Kind | Examples | Tracked |
|---|---|---|
| Written by a person | `*.json`, `*.md`, `*.py`, `.github/workflows/*.yml` | yes |
| Produced by a tool | `dist/`, `.agents/skills/`, `.codex/`, `.nebula-skills.json`, `__pycache__/` | no; the ignore rule lands in the same pull request |

- Run `git status` after any build or install. An untracked file is either a
  new source file to add or a generated file to ignore; it is never left
  unexplained.
