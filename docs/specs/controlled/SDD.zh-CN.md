<!-- translation-of: SDD.md -->
# 软件设计说明 — 修仙包

简体中文 · [English](SDD.md)

状态：草稿。描述的是已发布的 `cultivation@1.0.1` 与 `cultivation-rogue@0.5.0`。
批次：B12
日期：2026-11-10

需求在 `SRS.md`。本文说明每条需求落在哪里：哪个文件、哪个 manifest 字段、
哪个数据键。它是一张地图，不是理由——理由在 `docs/decisions/` 与
`docs/specs/` 下的包规格里。

## 落点表

| REQ | 设计 |
|---|---|
| `REQ-001` | `packs/` 下每个 id 一个目录，目录里再写一遍 `manifest.id`。`infra/tool/release/pack.py` 以目录为构建单位，用 `manifest.id` 命名压缩包。 |
| `REQ-002` | `infra/checks/check_pack.py`——`MAX_ENTRIES = 512`、`MAX_FILE_BYTES = 8 * 1024 * 1024`、`MAX_TOTAL_BYTES = 32 * 1024 * 1024`；根目录白名单只有 `manifest.json` 一个名字。 |
| `REQ-003` | `manifest.names`（每种语言一个键）、`manifest.defaultLocale`、`manifest.locales`。引擎打印 `names[当前语言]`。 |
| `REQ-004` | `data/i18n/<locale>.json`——每个节点 id 一条，含 `text` 与 `choices`，另有 `strings` 覆盖引擎可能打印的每个标签（`resource.<id>.<value>`、`action.<id>`、`rank.<n>`、`failure.<n>`）。 |
| `REQ-005` | `manifest.protocol: "linear@1"`、`manifest.entry`，以及 `data/nodes.json` 里每个选项的 `next`。`choices: []` 的节点结束本局，除非存在 `data/phases.json`。 |
| `REQ-006` | 两个包的 `manifest.mechanics: ["progress"]`；`packs/cultivation/data/mechanics.json` 是 `{"rules": []}`，线性包因此声明了进度、没有规则。 |
| `REQ-007` | `data/state.json` 的 `belief.sword` 与 `belief.body`（0..3），`data/rules.json` 三条读它们的规则，以及 `data/nodes.json` 里四个结局节点。 |
| `REQ-008` | 走的是一张新节点图，不是新文本字段：听者选项通向 `a1-voice-sword-believe`、`a1-voice-sword-turn`、`a1-voice-body-believe`、`a1-voice-body-turn`，每场只由那位听者引出。 |
| `REQ-009` | `data/actions.json`——六个 `send-*` 加一个 `rest`；每个 `send-*` 写 `stone`，再写 `injury.<d>` 与 `trust.<d>`/`greed.<d>` 之一；每次派遣都带 `requires`：`gate >= 1` 与 `injury.<d> <= 1`。 |
| `REQ-010` | `data/phases.json`——`turns: 36`、第 1/13/25 天的年号、三条 `injury.<d> >= 3` 的 `fail`，一条 `ruin`、三条 `breach`；`packs/cultivation-rogue/data/nodes.json` 的 `a2-hub` 用 `choices: []`，靠声明的阶段机续命。 |
| `REQ-015` | `manifest.clock: {"per": "turn"}`，`capabilities` 里有 `clock@1`；`data/rules.json`——三条 `tick >= 12/24/36` 写 `year`，三条 `field >= 1/3/6` 各加一石，三条 `year >= 1/2/3` 各扣一石，三条 `[year >= N, wall < 3/6/9]` 写 `breach`，一条 `[year >= 1, stone <= 0]` 写 `ruin`；`data/actions.json` 的 `dig-wall`（4 石）与 `tend-field`（3 石）是抬高 `wall` 与 `field` 的唯一办法。 |
| `REQ-011` | 两个包的 `manifest.saveSchema: 1`；槽位键由引擎按 `manifest.id` 拼，所以 `cultivation` 与 `cultivation-rogue` 永远读不到对方的档。 |
| `REQ-012` | 两个 manifest 的 `manifest.collection` 写同一个 `id`（`cultivation`）和同一组 `names`；引擎按 `collection.id` 分组。 |
| `REQ-013` | `.github/workflows/gate.yml` 在 `pack/<id>/v*` 标签上发布；`pack.py build` 写压缩包，`pack.py hash` 写 `<id>-<version>.json` 记 sha256。 |
| `REQ-016` | `manifest.capabilities` 加 `persist@1`，`manifest.persist` 声明一个整数键（`emperors`，0..9）；`data/rules.json` 在 `turn eq 1` 的规则里读 `persist.emperors`，加一块田、十二石或两级墙，并把数量抄进 `lineage` 资源，九条标签承载文本。 |
| `REQ-017` | `manifest.rolls` 声明 `clan` 为 `{"from": 0, "to": 2}`；`data/ledger.json` 加 `wave`（0..2）；`data/rules.json` 在跨年时把 `wave` 归零、用 `add_roll` 花掉抽签，并按 `wave` 取值扣一到两石贡。 |
| `REQ-014` | `.github/workflows/gate.yml` 遍历 `packs/*/` 跑 `pack.py build` 与 `check_pack.py`，第一个被拒就让任务失败。 |

## 仓的形状

三类内容三个家：`packs/<id>/` 是产品，`infra/` 是门禁跑的工具，`docs/` 是对它们的描述。
一个批次只动其中一类；批次卡里的允许路径让这件事可以被检查，而不只是被希望。

## 包的信封

`check_pack.py` 是压缩包里能有什么的唯一权威，它不解包直接读 zip。由此有两个后果：
包里不能有第二个根文件（所以包内放不了 `README.md`），单文件上限 8 MiB
（所以两个包今天都在 8 KiB 以下）。

## 语言覆盖

`data/i18n/en.json` 是 `nodes.json` 里中文的译本。引擎在装载时合并两者，把缺节点或
缺标签当作致命错误，而不是界面瑕疵。标签来自状态资源、动作、位阶与失败，
这正是 `strings` 在 `0.4.0` 才出现的原因：`0.3.0` 声明了资源（也就是标签），
却从没译过它们。

## 线性玩法

`linear@1` 读 `nodes.json`、画 `text`、给 `choices`、跟 `next`。线性包五个节点是一条链；
多数节点上的两个选项指向同一个下一步，这是有意的——写它们的那一批验证的是管线，
不是分叉。分叉住在派遣包里。

## 信念与心声

信念是两个有界数（`0..3`），由选项效果改动、由三条规则读取。心声是第二张图：
四场只有听者在场才解锁的戏。这是有意的设计落点——引擎没有并行文本这种原语，
所以「他听见了你没说出口的话」被建模成额外节点，而不是额外几行字。

## 派遣循环

一次派遣是一个动作：代价是伤，回报是石、信、贪。三个弟子让选择变得可读：
同一个地方，谁去，回报不同。拒绝路径是数据不是代码：`injury.<d> <= 1` 的 `requires`
让引擎把按钮按下去、把理由印出来。

另外两个动作花石却不派任何人：`dig-wall` 与 `tend-field`。两者都用 `requires`
把价钱门住，而不是只靠 `costs`——引擎不会拒绝一个花费超过存量的动作，
它照扣，再把结果夹到零。

## 日程机

三十六个回合、三个年份、五种收场。山门节点是那道铰链：它没有选项，
在纯线性读法下本该结束本局。声明 `phases.json` 改变了这一点——结束归机器管，
只要还有天，中枢就继续活着。年号落在第 1、13、25 天，因为那是年份翻动的地方；
引擎只把年号当标题印出来，从不拿它当闸门。

让年份真的存在的是时钟。`clock.per` 是 `turn`，所以每个动作都推一格 `tick`；
一条规则把 `tick >= 12` 写成 `year 1`。经济挂在 `year` 上，且在结束当天的那个
动作里按文件顺序跑：翻年、付田产、扣存粮、查墙、查米缸。顺序决定了两件事：
墙要在跨年那天之前立好；一局可以先把最后一石付给田，再被年份收走。

## 存档与合集

两个包都是 `saveSchema: 1`。这个 schema 承诺的是字段含义，不是布局：进了存档的节点 id
是永久的，改名要 `saveSchema` + 1。合集块只是元数据，改变分组，不改变玩法。

## 发布与 CI

一次发布是一个标签加两个资产。门禁在每次推送时构建每个包，坏包因此不会悄无声息地上
`main`；打标签的任务复用同两条命令，所以本地构建与已发布压缩包的哈希一致。
