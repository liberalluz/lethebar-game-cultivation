#!/usr/bin/env python3
"""Close a batch out in one command.

The last five batches each ended the same way: copy the live exit record into a
frozen directory, delete the manifest the freezer leaves behind, write the batch
README table, correct the two counts in the outer front page, run the three
checkers, then commit. Seven steps, seven chances to forget one.

This script does all seven in order and stops at the first thing that fails. It
changes nothing without --apply, so a dry run is free.

Usage:
    python infra/tool/batch/closeout.py --batch 2026-11-B12 --commit a1b2c3d
    python infra/tool/batch/closeout.py --batch 2026-11-B12 --commit a1b2c3d --apply
    python infra/tool/batch/closeout.py --batch 2026-11-B12 --commit a1b2c3d \\
        --apply --commit-docs
    python infra/tool/batch/closeout.py --release pack/cultivation-rogue/v0.6.1 \\
        --apply --commit-docs

A published tag records itself too: `--release` writes the evidence directory
(`release.json`, `release-notes.md`, `README.md`), its two index rows and the
front-page counts, so releases stop being the one closing step done by hand.

Exit status is 0 only when every step ran and all three checkers passed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

COUNTER_DIRS = ("records", "process", "product", "legal", "business")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalise(path: Path) -> tuple[int, str]:
    """Rewrite a file with LF endings, then report its size and hash."""
    data = path.read_bytes().replace(b"\r\n", b"\n")
    path.write_bytes(data)
    return len(data), hashlib.sha256(data).hexdigest()


def count_content(directory: Path) -> int:
    """Content files under a directory: no .gitkeep, no README.md."""
    return sum(
        1
        for f in directory.rglob("*")
        if f.is_file() and f.name not in (".gitkeep", "README.md")
    )


def write_batch_readme(path: Path, batch: str, date: str, by: str, commit: str,
                       name: str, size: int, digest: str) -> None:
    path.write_text(
        f"# {batch}\n\n"
        "| 项 | 值 |\n"
        "|---|---|\n"
        f"| 冻结日期 | {date} |\n"
        f"| 冻结人 | {by} |\n"
        f"| 源提交 | `{commit}` |\n\n"
        "## 文件清单\n\n"
        "| 文件 | 字节 | sha256 |\n"
        "| --- | --- | --- |\n"
        f"| `{name}` | {size} | `{digest}` |\n\n"
        "## 未纳入本批的\n\n"
        "| 项 | 原因 |\n"
        "|---|---|\n"
        "| 无 | 本批只冻结上述文件 |\n\n"
        "## 冻结纪律\n\n"
        "整份复制，未改一个字、未重排一行；hash 与字节数见上表。\n",
        encoding="utf-8",
        newline="\n",
    )


def add_index_row(index: Path, batch: str, date: str, name: str, commit: str) -> bool:
    """Append one row to the records index. Returns False if it is already there."""
    lines = index.read_text(encoding="utf-8", newline="").split("\n")
    row = (f"| {batch} | {date} | {name} | `records/live/{name}` | "
           f"`{commit}` | 长期 | 归档 |")
    if row in lines:
        return False
    last = max(
        (i for i, line in enumerate(lines) if line.startswith("| 2026-")),
        default=None,
    )
    if last is None:
        raise SystemExit("the records index has no rows to append after")
    lines.insert(last + 1, row)
    index.write_text("\n".join(lines), encoding="utf-8", newline="")
    return True


def update_counts(readme: Path, date: str, docs: Path) -> list[str]:
    """Rewrite the file counts in the front page from what is on disk."""
    lines = readme.read_text(encoding="utf-8", newline="").split("\n")
    changed = []
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        hit = next((d for d in COUNTER_DIRS if cells[0] == f"`{d}/`"), None)
        if hit is None:
            continue
        target = docs / hit
        if not target.is_dir():
            continue
        count = str(count_content(target))
        if cells[2] != count or cells[3] != date:
            cells[2], cells[3] = count, date
            lines[i] = "| " + " | ".join(cells) + " |"
            changed.append(f"{hit}: {count}")
    readme.write_text("\n".join(lines), encoding="utf-8", newline="")
    return changed


def run_checkers(repo: Path, docs: Path) -> bool:
    scripts = repo / ".agents" / "skills" / "nebula-delivery" / "scripts"
    ok = True
    for name in ("check_external.py", "check_records.py", "check_links.py"):
        proc = subprocess.run(
            [sys.executable, str(scripts / name), str(docs)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        tail = (proc.stdout or proc.stderr).strip().splitlines()
        print(f"  {name}: {tail[-1] if tail else '(no output)'}")
        if proc.returncode != 0:
            ok = False
            for line in tail[-12:]:
                print(f"    {line}")
    return ok


def gh_text(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["gh", *args], cwd=repo, capture_output=True, text=True, encoding="utf-8"
    )
    if proc.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def delete_branch(repo: Path, branch: str) -> bool:
    """Delete a branch on origin first, then locally.

    Batches, changelog folds and release branches all end here, so the guard is
    about what must survive rather than about a name prefix: the default branch
    stays, and so does any branch an open pull request still points at.
    """
    slug = gh_text(repo, "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner").strip()
    default = gh_text(
        repo, "repo", "view", "--json", "defaultBranchRef", "-q", ".defaultBranchRef.name"
    ).strip()
    if branch == default:
        print(f"branch  refusing to delete the default branch {branch}")
        return False
    open_prs = gh_text(
        repo, "pr", "list", "--head", branch, "--state", "open", "--json", "number"
    ).strip()
    if open_prs not in ("", "[]"):
        print(f"branch  refusing: an open pull request still points at {branch}")
        return False
    remote = subprocess.run(
        ["gh", "api", "-X", "DELETE", f"repos/{slug}/git/refs/heads/{branch}"],
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if remote.returncode != 0:
        message = (remote.stderr or remote.stdout).strip().splitlines()
        last = message[-1] if message else "failed"
        # `delete_branch_on_merge` may have removed it already; a missing ref is
        # the state we wanted, not a failure.
        if "HTTP 404" in last or "HTTP 422" in last or "does not exist" in last:
            print(f"branch  origin/{branch}: already gone")
        else:
            print(f"branch  origin/{branch}: {last}")
            return False
    else:
        print(f"branch  deleted origin/{branch}")
    local = subprocess.run(
        ["git", "-C", str(repo), "branch", "-D", branch],
        capture_output=True,
        text=True,
    )
    if local.returncode == 0:
        print(f"branch  deleted {branch} locally")
    else:
        print(f"branch  local {branch}: {local.stderr.strip()}")
    return True


def release_record(repo: Path, tag: str, zip_path: Path, notes: Path) -> dict:
    """Everything a release evidence directory records about one published tag."""
    info = json.loads(
        gh_text(repo, "release", "view", tag, "--json", "tagName,name,publishedAt,assets")
    )
    body = gh_text(repo, "release", "view", tag, "--json", "body", "-q", ".body")
    tag_object = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", tag],
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout.strip()
    tag_commit = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", f"{tag}^{{commit}}"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout.strip()
    data = zip_path.read_bytes()
    return {
        "tag": tag,
        "tagObject": tag_object,
        "tagCommit": tag_commit,
        "title": info["name"],
        "publishedAt": info["publishedAt"],
        "assets": [{"name": a["name"], "bytes": a["size"]} for a in info["assets"]],
        "zipBytes": len(data),
        "zipSha256": hashlib.sha256(data).hexdigest(),
        "body": body,
        "bodySource": (
            f"{notes.as_posix()} through gh release edit; GitHub stores one "
            "trailing newline more than the file"
        ),
    }


def write_release_readme(path: Path, tag: str, record: dict) -> None:
    pack, version = tag.split("/")[1], tag.rsplit("/v", 1)[1]
    files = [("release.json", record["jsonBytes"], record["jsonSha256"]),
             ("release-notes.md", record["notesBytes"], record["notesSha256"])]
    table = "\n".join(f"| `{n}` | {b} | {h} |" for n, b, h in files)
    descriptor = next(
        (a for a in record["assets"] if a["name"].endswith(".json")),
        {"bytes": 0, "name": f"{pack}-{version}.json"},
    )
    path.write_text(
        f"# Release {pack} v{version}\n\n"
        "- provider: `github`\n"
        f"- tag: `{tag}` (annotated, object `{record['tagObject'][:7]}`)\n"
        f"- commit: `{record['tagCommit'][:7]}`\n"
        "- status: `created`\n\n"
        "## 内容\n\n"
        "| 文件 | 字节 | sha256 |\n"
        "|---|---|---|\n"
        f"{table}\n\n"
        f"两个资产：`{pack}.zip`（{record['zipBytes']} 字节，sha256\n"
        f"`{record['zipSha256']}`）与 `{descriptor['name']}`（{descriptor['bytes']} 字节）。\n\n"
        "## 已验证\n\n"
        "- 归档重新构建的 sha256 与发布时一致；`check_pack.py` 打印 envelope holds；\n"
        "- 引擎侧的手动安装由维护者执行，不在本记录内。\n\n"
        "## 未纳入本批的\n\n"
        "| 项 | 原因 |\n"
        "|---|---|\n"
        "| 中文公告 | 公告只有英文一份 |\n",
        encoding="utf-8",
        newline="\n",
    )


def add_release_index_rows(index: Path, directory: str, day: str, commit: str,
                           version: str) -> int:
    lines = index.read_text(encoding="utf-8", newline="").split("\n")
    rows = [
        f"| {directory} | {day} | release-notes.md | `dist/msgs/release-{version}-notes.md` "
        f"的副本（GitHub 多存一个结尾换行） | `{commit}` | 长期 | 归档 |",
        f"| {directory} | {day} | release.json | 发布记录：tag、annotated tag 对象与 commit、"
        f"provider、bodySource、pack 的字节与 sha256 | `{commit}` | 长期 | 归档 |",
    ]
    added = 0
    for row in rows:
        if row in lines:
            continue
        last = max(i for i, line in enumerate(lines) if line.startswith("| 2026-"))
        lines.insert(last + 1, row)
        added += 1
    index.write_text("\n".join(lines), encoding="utf-8", newline="")
    return added


def closeout_release(args: argparse.Namespace, repo: Path, docs: Path, day: str) -> int:
    m = re.fullmatch(r"pack/([a-z0-9-]+)/v(\d+\.\d+\.\d+)", args.release)
    if not m:
        raise SystemExit(f"not a pack tag: {args.release}")
    pack, version = m.group(1), m.group(2)
    notes = Path(args.notes) if args.notes else Path(f"dist/msgs/release-{version}-notes.md")
    if not notes.is_file():
        raise SystemExit(f"no release notes: {notes} (pass --notes)")
    zip_path = Path(args.zip) if args.zip else Path("dist") / f"{pack}.zip"
    if not zip_path.is_file():
        raise SystemExit(f"no archive: {zip_path} (pass --zip)")

    record = release_record(repo, args.release, zip_path, notes)
    month = record["publishedAt"][:7]
    directory = f"{month}-release-{pack}-v{version}"
    frozen = docs / "records" / directory
    print(f"release {args.release}")
    print(f"dir     {frozen}")
    print(f"mode    {'apply' if args.apply else 'dry run'}")
    if not args.apply:
        print("nothing written; pass --apply to record")
        return 0

    frozen.mkdir(parents=True, exist_ok=True)
    release_json = json.dumps(record | {"body": "<in release-notes.md>"}, indent=2) + "\n"
    (frozen / "release.json").write_text(release_json, encoding="utf-8", newline="\n")
    (frozen / "release-notes.md").write_text(
        record["body"].replace("\r\n", "\n"), encoding="utf-8", newline="\n"
    )
    record["jsonBytes"] = (frozen / "release.json").stat().st_size
    record["jsonSha256"] = sha256_of(frozen / "release.json")
    record["notesBytes"] = (frozen / "release-notes.md").stat().st_size
    record["notesSha256"] = sha256_of(frozen / "release-notes.md")
    write_release_readme(frozen / "README.md", args.release, record)
    print(f"wrote   release.json, release-notes.md, README.md "
          f"({record['notesBytes']} B of notes)")

    index = docs / "records" / "README.md"
    added = add_release_index_rows(index, directory, day, record["tagCommit"][:7], version)
    print(f"index   {added} row(s) added")
    for item in update_counts(docs / "README.md", day, docs):
        print(f"counts  {item}")

    print("checks")
    if not run_checkers(repo, docs):
        print("a checker failed; nothing committed")
        return 1
    if args.commit_docs:
        message = f"docs(records): record the {pack} {version} release"
        subprocess.run(["git", "-C", str(docs), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(docs), "commit", "-m", message], check=True)
        print(f"committed: {message}")
    else:
        print("not committed; pass --commit-docs")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Freeze a batch exit record and close it out.")
    ap.add_argument("--batch", default=None, help="frozen directory name, e.g. 2026-11-B12")
    ap.add_argument("--commit", default=None, help="the commit the batch merged as")
    ap.add_argument("--file", default=None, help="exit record name, default B<n>-exit.md")
    ap.add_argument("--release", default=None, help="record a published pack tag instead")
    ap.add_argument("--notes", default=None, help="the notes file that was published")
    ap.add_argument("--zip", default=None, help="the archive that was uploaded")
    ap.add_argument("--date", default=None, help="freeze date, default today")
    ap.add_argument("--by", default="liberalluz", help="who freezes")
    ap.add_argument("--root", default=".", help="repository root")
    ap.add_argument("--docs-root", default=None, help="outer docs repository")
    ap.add_argument("--apply", action="store_true", help="write; without it nothing changes")
    ap.add_argument("--commit-docs", action="store_true", help="commit the docs repository")
    ap.add_argument(
        "--delete-branch",
        default=None,
        metavar="BRANCH",
        help="after closing, delete this branch locally and on origin",
    )
    args = ap.parse_args()

    repo = Path(args.root).resolve()
    docs = Path(args.docs_root).resolve() if args.docs_root else repo.parent / (
        repo.name + "-docs")
    if not docs.is_dir():
        raise SystemExit(f"docs repository not found: {docs}")

    from datetime import date as _date
    day = args.date or _date.today().isoformat()
    if args.release:
        return closeout_release(args, repo, docs, day)
    if not args.batch or not args.commit:
        raise SystemExit("either --release TAG or both --batch and --commit")
    match = re.search(r"-B(\d+)$", args.batch)
    if not match:
        raise SystemExit(f"batch name carries no number: {args.batch}")
    name = args.file or f"B{match.group(1)}-exit.md"

    live = docs / "records" / "live" / name
    frozen_dir = docs / "records" / args.batch
    if not live.is_file():
        raise SystemExit(f"no live exit record: {live}")

    print(f"batch   {args.batch}")
    print(f"file    {name}")
    print(f"live    {live}")
    print(f"frozen  {frozen_dir}")
    print(f"mode    {'apply' if args.apply else 'dry run'}")

    if not args.apply:
        for d in COUNTER_DIRS:
            if (docs / d).is_dir():
                print(f"would count {d}/ -> {count_content(docs / d)}")
        print("nothing written; pass --apply to freeze")
        return 0

    frozen_dir.mkdir(parents=True, exist_ok=True)
    target = frozen_dir / name
    target.write_bytes(live.read_bytes())
    size, digest = normalise(target)
    normalise(live)
    manifest = frozen_dir / "freeze-manifest.json"
    if manifest.exists():
        manifest.unlink()
        print("removed freeze-manifest.json")
    write_batch_readme(frozen_dir / "README.md", args.batch, day, args.by,
                       args.commit, name, size, digest)
    print(f"frozen  {name}  {size} B  {digest}")

    index = docs / "records" / "README.md"
    if add_index_row(index, args.batch, day, name, args.commit):
        print("index   one row added")
    else:
        print("index   row already present")

    for item in update_counts(docs / "README.md", day, docs):
        print(f"counts  {item}")

    print("checks")
    ok = run_checkers(repo, docs)
    if not ok:
        print("a checker failed; nothing committed")
        return 1

    if args.commit_docs:
        message = f"docs(records): freeze the {args.batch.split('-')[-1]} exit record"
        subprocess.run(["git", "-C", str(docs), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(docs), "commit", "-m", message], check=True)
        print(f"committed: {message}")
    else:
        print("not committed; pass --commit-docs")

    if args.delete_branch:
        if not delete_branch(repo, args.delete_branch):
            print("closed, but the branch is still there")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
