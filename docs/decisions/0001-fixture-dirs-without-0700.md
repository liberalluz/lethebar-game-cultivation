# 0001. Build self-test fixtures without mode 0700

Status: accepted
Date: 2026-11-08

## Context

`infra/tool/release/pack.py` and `infra/checks/check_pack.py` were copied from
the engine, byte for byte, when this repository was created. Both were known to
pass their self-tests on Linux CI.

On Windows they failed before testing anything:

```
pack.py:        PermissionError: [WinError 5] Access is denied
                tempfile._resetperms -> _dont_follow_symlinks(_os.chmod, path, 0o700)
check_pack.py:  PermissionError: [Errno 13] Permission denied: ...\clean.zip
```

Both self-tests built their fixtures through `tempfile.mkdtemp()` or
`tempfile.TemporaryDirectory()`, which create the directory with mode `0o700`.
On Windows `os.mkdir(path, 0o700)` produces a DACL with inheritance removed:

```
NT AUTHORITY\SYSTEM:(OI)(CI)(F)
BUILTIN\Administrators:(OI)(CI)(F)
OWNER RIGHTS:(OI)(CI)(F)
```

Under a restricted token — a sandbox, a container, some CI agents — the process
that just created that directory has no matching ACE, so it cannot write into
it, cannot read its ACL, and cannot `chmod` it during cleanup. `0o755` and
`0o777` keep the inherited ACEs and work. The engine's own comment in
`check_pack.py` (fixtures placed beside the checker so a sandbox cannot refuse
the system temporary directory) was defeated one line later by `mkdtemp`.

The same failure reproduces with a three-line script:

```python
import os, pathlib
p = pathlib.Path("x700"); os.mkdir(p, 0o700); (p / "a.txt").write_text("hi")
```

## Decision

Create the fixture directories with the default mode instead of `0o700`:

- `infra/checks/check_pack.py` — `scratch / f"fixtures-{os.getpid()}"`, created
  with `Path.mkdir()`, removed with `shutil.rmtree(..., ignore_errors=True)`.
- `infra/tool/release/pack.py` — a local `scratch_dir()` context manager that
  does the same, replacing the three `TemporaryDirectory` instances.

The fixtures hold no secrets; `0o700` bought nothing. Nothing else in either
tool changed: the archive rules, the hash, and the publish commands are the
engine's.

## Consequences

- Both self-tests now pass under the Windows sandbox without escalation
  (`pack.py self-test` → one `[ok]` line; `check_pack.py --self-test` → 10
  cases, 0 failures).
- These two files are **no longer byte-identical to the engine**:
  `pack.py` `56ed4758` → `7c67e478`, `check_pack.py` `dfa6c590` → `66a9dfd3`.
  The blob comparison that proved the copy was faithful no longer holds for
  them.
- CI runs the copies in this repository, so the gate exercises the changed
  fixtures rather than the engine's originals.
- The same defect exists upstream; it was reported to the engine repository.
  When the engine ships the fix, re-copy these two files and delete this
  decision — the byte-for-byte property comes back.
