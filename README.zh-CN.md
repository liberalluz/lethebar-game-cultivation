<!-- translation-of: README.md -->
# 修仙

[English](README.md) · 简体中文

> 一个 Lethebar 世界：同一个故事，两种玩法。
> 故事是数据，规则是引擎的，这个世界住在这个仓里。

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE) <!-- pack-badges:begin -->
![packs](https://img.shields.io/badge/packs-2-6f42c1)
![spec](https://img.shields.io/badge/spec-2.0.0-007ec6)
![engine](https://img.shields.io/badge/engine-%3E%3D4.7.0%20%3C5.0.0-478cbf)

| Kind | Pack | Version | Spec | Engine |
| --- | --- | --- | --- | --- |
| `bundle` | `cultivation` | `1.0.1` | `2.0.0` | `>=4.7.0 <5.0.0` |
| `bundle` | `cultivation-rogue` | `0.6.3` | `2.0.0` | `>=4.7.0 <5.0.0` |
<!-- pack-badges:end -->

## 状态

一个世界，两个包，都已发布。`cultivation` 是原来内建在引擎里的五节点线性故事；
`cultivation-rogue` 是派遣玩法——一个很弱的师尊把比他强得多的徒弟派出去，一局九代，
而只有一个人听得见别人心里在想什么。两个包同属 collection `修仙 / Cultivation`，所以在
引擎的包列表里是「一个世界、两种玩法」。

上表由两个 manifest 经 `python infra/tool/release/pack.py badge . --write README.md`
生成；gate 用同样的命令加 `--check` 跑，任一行漂了就红。这是这份文件唯一写版本号的地方，
日期在 [Releases 页](https://github.com/liberalluz/lethebar-game-cultivation/releases)。

## 故事

`packs/cultivation/` 是那条五节点故事，`x1` 到 `x5`，走完约十五分钟。`x1` 到 `x4`
各有两个选项，今天两个选项都通向 `x2`。这是故意的：那个包要验证的是引擎能装载、前进、
存档、读档。分叉是内容改动，以后在 `packs/cultivation/data/nodes.json` 里做。

`packs/cultivation-rogue/` 是另一种玩法。第一幕十二个节点、四个结局；两个可见信念
（`belief_sword`、`belief_body`）会变成 `qi` 或 `insight`，四场心声戏决定你拿到哪个
结局。只有师姐听得见心声，所以同一句说出口的话可以有两个意思。走到结局会为你打开第二幕
的门：三个徒弟、一块田、一堵墙，以及每年一次、连来九代的雪线——一局三百二十四天。

显示名是中文的「修仙」「修仙·派遣」，英文的 `Cultivation`、`Cultivation: Dispatch`；
id 是 `cultivation` 与 `cultivation-rogue`，玩家看不到 id。

## 安装一个包

从 Releases 页拿压缩包，用引擎自己的安装动作装上；为什么网页链接装不了、装包怎么做，
见引擎的[发布指南](https://github.com/liberalluz/lethebar/blob/main/docs/guide/publishing.md)。

存档键是 `save:cultivation:<slot>` 与 `save:cultivation-rogue:<slot>`，由各自的清单 id
推出。旧内建包写下的 `save:xiuxian:<slot>` 读不回来；那个 id 改过一次，当时还没有任何
包发布。

## 构建与发布

命令、tag 形状、发布前检查与发布证据都在
[docs/runbooks/release.md](docs/runbooks/release.md)；什么算合格的归档、什么算合格的
发布，以引擎的[发布指南](https://github.com/liberalluz/lethebar/blob/main/docs/guide/publishing.md)
为准。本仓的 gate 在每个 PR 上构建并检查所有包，只在 `pack/*` 标签上发布。

## 项目结构

| 路径 | 放什么 |
|---|---|
| `packs/cultivation/` | 五节点故事：`manifest.json`、`data/nodes.json`、`data/mechanics.json`、`data/i18n/en.json` |
| `packs/cultivation-rogue/` | 派遣玩法：`manifest.json`、`data/nodes.json`、`data/ledger.json`、`data/actions.json`、`data/rules.json`、`data/phases.json`、`data/i18n/en.json` |
| `infra/checks/` | 信封检查、数据检查、CI 模板检查、提交正文检查 |
| `infra/tool/release/` | `pack.py`：构建、hash、徽章、发布；`release.py`：合成 changelog；`preflight.py`：发布前检查 |
| `infra/tool/merge/` | `pr_merge.py`：生成并校验 squash 合并正文 |
| `infra/tool/batch/`、`infra/tool/repo/` | 从 Nebula 拷来的批次与仓库工具 |
| `product/release-notes/` | 每个包每个版本一份说明，Release 页显示的就是它 |
| `docs/` | 规格、决策、意图、操作手册（[docs/README.md](docs/README.md)） |

仓根只放上表列出的东西，加上惯例的根文件（`README`、`CONTRIBUTING`、`CONTRIBUTING.ai`、
`SECURITY`、`LICENSE`、`CHANGELOG`、`AGENTS`、`.gitignore`、`.gitattributes`、
`.nebula-scaffold.json`）。

## 文档

| 想找什么 | 在哪 |
|---|---|
| 一个包承诺什么 | [docs/specs/](docs/specs/) |
| 这个仓为什么存在 | [docs/intent/](docs/intent/) |
| 决定过什么、否掉过什么 | [docs/decisions/](docs/decisions/) |
| 怎么发一版 | [docs/runbooks/](docs/runbooks/) |
| 两个包从哪份设计长出来 | [design/](design/README.md) |

## 参与贡献

- 开 PR 之前先读 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 用 AI 改文字或代码？也读 [CONTRIBUTING.ai.md](CONTRIBUTING.ai.md)：AI 改动需要人
  评审并附证据，作者不能自审。
- 不要为了让测试通过而改故事；两个选项都通向 `x2` 是有意的。

## 安全

见 [SECURITY.md](SECURITY.md)。引擎把包当不可信输入；本仓把引擎的信封规则当作
「包能装什么」的权威。

## 许可

本仓里的包按 [Apache License 2.0](LICENSE) 授权。允许使用、修改与再分发，但要保留
版权声明与许可文本。播放它们的引擎在自己的仓里单独授权。

没有打包任何第三方素材——没有字体、图片或声音——所以没有 `NOTICE` 文件。将来某个包
若带了别处来的素材，它的声明与许可条款随同一个 PR 到场。
