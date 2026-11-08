# 0001 — One source for the Cultivation story

## The problem

The engine carried the story as built-in content: a five-node linear pack
compiled into the engine's own tree and shipped with every engine release. That
couples content to engine releases — a typo in a node needs a new engine build —
and it makes the engine bigger than its job, which is to run packs.

## What this repository is for

`lethebar-game-cultivation` is the only home of the story after the split. It
owns the text, the manifest and the release; the engine owns the protocol, the
save format and the renderer.

It is a pack repository and nothing else: `packs/cultivation/` plus the tools
needed to build, check and publish it. There is no engine code here.

## What success looks like

- A player installs `cultivation.zip` from the `pack/cultivation/v1.0.0`
  release and finishes the five nodes in both `zh-CN` and `en`.
- The engine repository contains no copy of the story after `v0.6.0`.
- `main` is green: the gate builds the pack, checks the envelope and uploads
  the archive.
- The tag publishes both assets: the archive and its descriptor.

## Out of scope

Art, music, extra nodes and mechanics rules. This repository starts as a move
and a rename; content comes later, in its own changes.
