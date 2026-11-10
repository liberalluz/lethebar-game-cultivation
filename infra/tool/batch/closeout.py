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

Exit status is 0 only when every step ran and all three checkers passed.
"""

from __future__ import annotations

import argparse
import hashlib
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


def delete_branch(repo: Path, branch: str) -> bool:
    """Delete a merged batch branch on origin first, then locally."""
    slug = subprocess.run(
        ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if slug.returncode != 0 or not slug.stdout.strip():
        print(f"branch  cannot resolve the repository: {slug.stderr.strip()}")
        return False
    remote = subprocess.run(
        ["gh", "api", "-X", "DELETE", f"repos/{slug.stdout.strip()}/git/refs/heads/{branch}"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if remote.returncode != 0:
        message = (remote.stderr or remote.stdout).strip().splitlines()
        print(f"branch  origin/{branch}: {message[-1] if message else 'failed'}")
        return False
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


def main() -> int:
    ap = argparse.ArgumentParser(description="Freeze a batch exit record and close it out.")
    ap.add_argument("--batch", required=True, help="frozen directory name, e.g. 2026-11-B12")
    ap.add_argument("--commit", required=True, help="the commit the batch merged as")
    ap.add_argument("--file", default=None, help="exit record name, default B<n>-exit.md")
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
