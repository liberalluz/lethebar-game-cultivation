#!/usr/bin/env python3
"""Read a pack's data files the way the engine reads them, and refuse what it refuses.

The engine validates a package when it loads one: `Ledger.problems` refuses a resource
id the grammar forbids (V-14), `Menu.problems` refuses an action id the grammar forbids
(V-16), and the package validator refuses a label key the English table does not carry
(V-22).  `check_pack.py` only looks inside the envelope, so an archive can pass it and
still be rejected on install.  This script closes that gap for the files a data-only
pack carries.

Usage:
    python infra/checks/check_pack_data.py packs/cultivation-rogue [packs/cultivation]

Exit code 0 when every pack passes, 1 when any does not.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

# Keys the engine itself puts into a rule's scope; a pack may read them without
# declaring a resource of that name.
SCOPE_KEYS = frozenset({"tick"})


def load(path: Path):
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def read_pack(pack: Path) -> dict:
    data = pack / "data"
    return {
        "manifest": load(pack / "manifest.json") or {},
        "ledger": load(data / "ledger.json"),
        "actions": load(data / "actions.json"),
        "rules": load(data / "rules.json"),
        "phases": load(data / "phases.json"),
        "nodes": load(data / "nodes.json"),
        "strings": (load(data / "i18n" / "en.json") or {}).get("strings", {}),
    }


def when_entries(when) -> list[dict]:
    if when is None:
        return []
    return when if isinstance(when, list) else [when]


def check_pack(pack: Path) -> tuple[list[str], dict[str, int]]:
    files = read_pack(pack)
    problems: list[str] = []
    counts = {"actions": 0, "resources": 0, "strings": 0, "references": 0}

    ledger = files["ledger"] or {}
    resources = ledger.get("resources", [])
    counts["resources"] = len(resources)
    declared: set[str] = set()
    labels: dict[str, list[str]] = {}

    for resource in resources:
        rid = str(resource.get("id", ""))
        if not ID_PATTERN.match(rid):
            problems.append(
                "V-14 %s: the resource id is not a lowercase id the engine can read "
                "(^[a-z][a-z0-9_]*$)" % rid
            )
        declared.add(rid)
        keys = resource.get("labels")
        if isinstance(keys, dict) and keys:
            labels[rid] = [str(k) for k in keys]

    def reference(where: str, key, *, scope: bool = True) -> None:
        if not isinstance(key, str):
            problems.append("%s: a key that is not a string" % where)
            return
        counts["references"] += 1
        if scope and key in SCOPE_KEYS:
            return
        if key.startswith("roll.") or key.startswith("persist."):
            return
        if key not in declared:
            problems.append("%s: names %r, and the ledger declares no such resource" % (where, key))

    actions = files["actions"] or {}
    for action in actions.get("actions", []):
        counts["actions"] += 1
        aid = str(action.get("id", ""))
        if not ID_PATTERN.match(aid):
            problems.append(
                "V-16 %s: the action id is not a lowercase id the engine can read "
                "(^[a-z][a-z0-9_]*$)" % aid
            )
        effects = action.get("effects")
        if not isinstance(effects, list) or not effects:
            problems.append("V-16 %s: effects must be a non-empty array" % aid)
        else:
            for effect in effects:
                if not isinstance(effect, dict):
                    problems.append("V-16 %s: an effect is not a table of keys" % aid)
                    continue
                for key in effect:
                    reference("action %s" % aid, key)
        for key in (action.get("costs") or {}):
            reference("action %s costs" % aid, key, scope=False)
        for entry in action.get("requires", []):
            reference("action %s requires" % aid, entry.get("key"), scope=False)
        limit = action.get("limit")
        if limit is not None and (not isinstance(limit, dict) or set(limit) - {"per_run", "per_turn"}):
            problems.append("V-16 %s: limit may only name per_run or per_turn" % aid)

    rules = files["rules"] or {}
    for index, rule in enumerate(rules.get("rules", [])):
        where = "rule %d" % (index + 1)
        for entry in when_entries(rule.get("when")):
            reference("%s when" % where, entry.get("key"))
        for key in (rule.get("set") or {}):
            reference("%s set" % where, key, scope=False)

    phases = files["phases"] or {}
    for index, entry in enumerate(phases.get("fail", [])):
        for condition in when_entries(entry.get("when")):
            reference("phase fail %d" % index, condition.get("key"), scope=False)

    # A choice may carry effects, and the engine applies them without asking the ledger
    # first, so they are not part of what an install refuses; the four files above are.

    strings = files["strings"]
    counts["strings"] = len(strings)
    wanted: list[str] = []
    for action in actions.get("actions", []):
        wanted.append("action.%s" % action.get("id", ""))
    for rank in phases.get("ranks", []):
        wanted.append("rank.%s" % rank.get("at"))
    for index in range(len(phases.get("fail", []))):
        wanted.append("failure.%d" % index)
    for rid, values in labels.items():
        for value in values:
            wanted.append("resource.%s.%s" % (rid, value))

    if strings:
        for key in wanted:
            if key not in strings:
                problems.append("V-22 %s: the English table has no line for it" % key)
    counts["wanted_strings"] = len(wanted)

    return problems, counts


def main(argv: list[str]) -> int:
    packs = [Path(a) for a in argv[1:]] or [Path("packs/cultivation-rogue")]
    failed = False
    for pack in packs:
        if not pack.is_dir():
            print("not a pack directory: %s" % pack)
            return 2
        problems, counts = check_pack(pack)
        name = pack.name
        if problems:
            failed = True
            print("[data] %s: %d problem(s)" % (name, len(problems)))
            for line in problems:
                print("  " + line)
        else:
            print(
                "[data] %s: ok (%d actions, %d resources, %d references, "
                "%d of %d label lines)"
                % (
                    name,
                    counts["actions"],
                    counts["resources"],
                    counts["references"],
                    counts["wanted_strings"],
                    counts["wanted_strings"],
                )
            )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
