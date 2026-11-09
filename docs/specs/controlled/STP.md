# Software Test Plan — Cultivation packages

Status: draft.
Batch: B10
Date: 2026-11-09

Requirements are in `SRS.md`; each test below names what it covers and what
makes it pass. The repository has no test runner: a test is a procedure a
maintainer can walk with the tools in `infra/` and, where the engine is
needed, the web build. `STD.md` holds the steps.

Tests are grouped by what they protect rather than by when they run: identity
and envelope first, because everything else rides on a valid archive; locales
next, because a miss there is fatal at install; play after that; release last.

## Tests

| Test | Covers | Exit |
|---|---|---|
| `TC-ID-001` | `REQ-001` | Building each directory produces one archive, and each archive's `manifest.id` equals the directory name. |
| `TC-ENV-001` | `REQ-002` | `check_pack.py` accepts both archives; a copy with a second root file, a symlink or an entry over 8 MiB is rejected with the reason. |
| `TC-IDN-001` | `REQ-003` | Switching the interface language changes the displayed name between 修仙 and Cultivation, and no id appears on the package list. |
| `TC-LOC-001` | `REQ-004` | Every node id and every label key of both packages has an English string; removing any one of them makes install fail. |
| `TC-LIN-001` | `REQ-005` | The linear package reaches an end screen after five nodes; the dispatch package's gate node shows actions instead of ending. |
| `TC-PRG-001` | `REQ-006` | The linear package shows a step count that rises with each node, and its rules file declares zero rules. |
| `TC-BLF-001` | `REQ-007` | Two runs with opposite replies end on different endings and record different belief numbers. |
| `TC-VOI-001` | `REQ-008` | The four voice scenes are unreachable without the listener choice and reachable with it. |
| `TC-DSP-001` | `REQ-009` | Every dispatch changes at least one disciple key; a disciple at injury 2 is refused with a reason naming the key. |
| `TC-DSP-002` | `REQ-009` | One rest returns an injured disciple to sendable, and the next dispatch succeeds. |
| `TC-PHS-001` | `REQ-010` | Twelve actions exhaust the days; injury 3 ends the run with that disciple's own failure reason. |
| `TC-PHS-002` | `REQ-010` | The hub offers actions after the gate opens, and the day counter shows 12 at the start. |
| `TC-SAV-001` | `REQ-011` | A save is visible only in its own package and restores the node and ledger numbers it captured. |
| `TC-COL-001` | `REQ-012` | Both packages appear under one world entry; removing the block lists one of them separately. |
| `TC-REL-001` | `REQ-013` | For a published tag, hashing the downloaded archive reproduces the descriptor's sha256. |
| `TC-CI-001` | `REQ-014` | A commit with a broken pack turns the workflow red; the current main is green. |

## What is not tested here

The engine's own behaviour — how it draws a node, how it merges translations,
how it computes a step count — is tested in `lethebar`. These tests only check
that the packages carry the data the engine needs, and that a player notices
the difference.
