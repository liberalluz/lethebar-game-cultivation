# Software Test Description — Cultivation packages

Status: draft.
Batch: B10
Date: 2026-11-09

One section per test in `STP.md`. Each says how to set it up, what to do, and
what to see. All commands run from the repository root; the web build of the
engine is reachable from the published site and installs packages from a local
`.zip` through 所有包 → 安装插件包.

## TC-ID-001 — one directory, one id

1. Run `python infra/tool/release/pack.py build packs/cultivation --out dist`
   and the same for `packs/cultivation-rogue`.
2. Read `dist/cultivation.zip` and `dist/cultivation-rogue.zip` with
   `python -c "import zipfile,json;print(json.loads(zipfile.ZipFile('dist/cultivation.zip').read('manifest.json'))['id'])"`.
3. Compare each printed id with its directory name.

Expected: two archives, each root manifest naming `cultivation` and
`cultivation-rogue`, matching their directories, and the two ids differ.

## TC-ENV-001 — the archive stays inside its envelope

1. Run `python infra/checks/check_pack.py dist/cultivation.zip` and the same
   for the dispatch archive.
2. Copy one archive, add a second file at its root with
   `python -c "import zipfile,shutil;shutil.copy('dist/cultivation.zip','dist/bad.zip');z=zipfile.ZipFile('dist/bad.zip','a');z.writestr('README.md','x');z.close()"`.
3. Run `check_pack.py dist/bad.zip`.
4. Repeat step 2 with a symlinked entry (`ZipInfo` with `external_attr`
   `0xA1FF0000`) and a 9 MiB entry.

Expected: step 1 prints `the envelope holds` twice; steps 3 and 4 fail with a
message naming the second root entry, the symlink and the 8 MiB cap.

## TC-IDN-001 — the player sees a name, not an id

1. Start a new game and open 所有包.
2. Note the two entries under the world heading.
3. Switch the interface language to English and open 所有包 again.

Expected: the entries read 修仙·派遣 and Cultivation: Dispatch; neither screen
shows `cultivation` or `cultivation-rogue`.

## TC-LOC-001 — every node and label has a line

1. Run the label mirror over both packs: for each node id in `nodes.json`,
   check that `data/i18n/en.json` has an entry with `text` and a `choices`
   array of the same length.
2. For every state resource, action, rank and failure in the dispatch pack,
   check that `strings` holds the key the engine prints.
3. Remove one key from `en.json`, rebuild, and install the archive.

Expected: steps 1 and 2 find no gap; step 3 is refused at install with a
missing-translation error, and putting the key back makes it installable again.

## TC-LIN-001 — five nodes, one end

1. Install `dist/cultivation.zip` and start a new game.
2. Take the first choice on each of the five screens.

Expected: the fifth screen has no choices and an end screen appears; step count
reads 5/5 at the end.

## TC-PRG-001 — the readout is the engine's

1. Start the linear pack and note the small caption under the text on the
   first screen, then the second and third.
2. Open `packs/cultivation/data/mechanics.json`.

Expected: the caption reads 第 1/5 步, then 第 2/5 步, then 第 3/5 步;
the file holds `{"rules": []}`.

## TC-BLF-001 — two runs, two endings

1. Install `dist/cultivation-rogue.zip`, start a new game, and answer the
   sword questions with belief.
2. Save to slot 1, finish the act, and note the ending and the belief numbers
   the ending names.
3. Start again, answer every question against belief, finish, compare.

Expected: the two endings differ; the belief numbers at the end differ; the
navigation differs at the second and third scene, not only at the last.

## TC-VOI-001 — four scenes only a listener opens

1. Walk the first act once, choosing the listener line at the sword scene.
2. Walk it again, choosing the line that keeps the thought private.
3. Compare the scene graphs: `python -c "import json;n=json.load(open('packs/cultivation-rogue/data/nodes.json'));print([x['id'] for x in n['nodes'] if 'voice' in x['id']])"`.

Expected: the first walk passes through one of the four `a1-voice-*` scenes
and the second never does; the four scenes exist and each is reachable only
through its listener choice.

## TC-DSP-001 — a dispatch writes a disciple

1. Open the pack, walk the prologue to the hub, and send 阿磐 to the ruins.
2. Read the ledger before and after — the hub shows stone, and the disciple's
   line shows injury, trust or greed.
3. Send 阿磐 to the ruins a second time, then try a third.

Expected: each send changes `stone` and at least one of
`injury.apan`/`trust.apan`/`greed.apan`; after the second send the injury is 2,
the third button is disabled, and the reason names `injury.apan`.

## TC-DSP-002 — rest makes a disciple sendable again

1. With 阿磐 at injury 2, take 歇息 once.
2. Try the ruins dispatch again.

Expected: injury drops to 1, the button enables, and the dispatch succeeds.

## TC-PHS-001 — twelve days, three failures

1. Rest twelve times, counting the day counter.
2. On a fresh run, send one disciple to the ruins until injury reaches 3.

Expected: the thirteenth action is refused and the run reports the days are
spent (a rank title appears at days 1, 5 and 9); at injury 3 the run ends with
that disciple's own failure line, not a generic one.

## TC-PHS-002 — the hub stays alive

1. Open the dispatch pack and walk the prologue to the gate.
2. Read the hub screen: it must hold no choices and still offer the action
   list.

Expected: actions are offered, the day counter reads 12, and the first rank
title is shown.

## TC-SAV-001 — a save belongs to its pack

1. In the dispatch pack, save to slot 1 at the hub, then quit to the package
   list.
2. Open the linear pack and its save page.
3. Return to the dispatch pack, load slot 1.

Expected: the linear pack lists no save; the dispatch pack lists slot 1 with
the hub's text, and loading returns to the hub with the same stone and injury
numbers.

## TC-COL-001 — one world, two packs

1. Open 所有包 with both installed.
2. Copy the dispatch archive, delete its `collection` block from the manifest,
   rebuild and install it under a test name.

Expected: step 1 shows one world heading with both packs; step 2 shows the
edited pack outside that heading.

## TC-REL-001 — the descriptor matches the archive

1. Pick the newest `pack/cultivation-rogue/v*` release on GitHub.
2. Download both assets.
3. Run `python infra/tool/release/pack.py hash cultivation-rogue.zip` on the
   downloaded archive and compare with the descriptor's `sha256`.

Expected: the two values are identical, and the descriptor's version matches
the tag.

## TC-CI-001 — a broken pack cannot land quietly

1. On a scratch branch, delete a node from `packs/cultivation/data/nodes.json`
   without touching `en.json`.
2. Push and open the workflow run.

Expected: the `check_pack` step fails, and the run is red with the missing
translation named; `main`'s latest run is green for both packs.
