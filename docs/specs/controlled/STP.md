# Software Test Plan — Cultivation packages

Status: draft.
Batch: B12
Date: 2026-11-10

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
| `TC-ENV-001` | `REQ-002` | `check_pack.py` accepts both archives; a copy with a second root file, a symlink or an entry over 4 MiB is rejected with the reason. |
| `TC-IDN-001` | `REQ-003` | Switching the interface language changes the displayed name between 修仙 and Cultivation, and no id appears on the package list. |
| `TC-LOC-001` | `REQ-004` | Every node id and every label key of both packages has an English string; removing any one of them makes install fail. |
| `TC-LIN-001` | `REQ-005` | The linear package reaches an end screen after five nodes; the dispatch package's gate node shows actions instead of ending. |
| `TC-PRG-001` | `REQ-006` | The linear package shows a step count that rises with each node, and its rules file declares zero rules. |
| `TC-BLF-001` | `REQ-007` | Two runs with opposite replies end on different endings and record different belief numbers. |
| `TC-VOI-001` | `REQ-008` | The four voice scenes are unreachable without the listener choice and reachable with it. |
| `TC-DSP-001` | `REQ-009` | Every dispatch changes at least one disciple key; a disciple at injury 2 is refused with a reason naming the key. |
| `TC-DSP-002` | `REQ-009` | One rest returns an injured disciple to sendable, and the next dispatch succeeds. |
| `TC-PHS-001` | `REQ-010` | Thirty-six actions exhaust the days; injury 3 ends the run with that disciple's own failure reason. |
| `TC-PHS-002` | `REQ-010` | The hub offers actions after the gate opens, and the day counter shows 36 at the start. |
| `TC-ECO-001` | `REQ-015` | A field level pays one stone on every later action, and the action that crosses day 12 turns the year and charges one stone of upkeep. |
| `TC-ECO-002` | `REQ-015` | A run that enters year 2 with fewer than six wall levels ends on that year's breach line; six levels let it continue. |
| `TC-ECO-003` | `REQ-015` | A run that starts a day with an empty store, after year 1, ends on the empty-store line rather than on an injury. |
| `TC-SAV-001` | `REQ-011` | A save is visible only in its own package and restores the node and ledger numbers it captured. |
| `TC-COL-001` | `REQ-012` | Both packages appear under one world entry; removing the block lists one of them separately. |
| `TC-REL-001` | `REQ-013` | For a published tag, hashing the downloaded archive reproduces the descriptor's sha256. |
| `TC-MTA-001` | `REQ-016` | A run that finishes its third year raises the name count by one and the next run starts with one field level; a run that ends in failure leaves both unchanged. |
| `TC-ROL-001` | `REQ-017` | Reaching the same turn twice, once after a reload, yields the same wave weight, and the year's tribute equals that weight. |
| `TC-CI-001` | `REQ-014` | A commit with a broken pack turns the workflow red; the current main is green. |

## What is not tested here

The engine's own behaviour — how it draws a node, how it merges translations,
how it computes a step count — is tested in `lethebar`. These tests only check
that the packages carry the data the engine needs, and that a player notices
the difference.
