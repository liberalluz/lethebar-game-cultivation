<!-- translation-of: README.md -->
# 修仙

[English](README.md) · 简体中文

> 一个 Lethebar 世界：同一个故事，两种玩法。
> 故事是数据，规则是引擎的，这个世界住在这个仓里。

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Packs](https://img.shields.io/badge/packs-2-6f42c1.svg)](docs/specs/packs.md)
[![Spec](https://img.shields.io/badge/spec-2.0.0-007ec6.svg)](packs/cultivation/manifest.json)
[![Engine](https://img.shields.io/badge/engine-%3E%3D4.7.0%20%3C5.0.0-478cbf.svg)](https://github.com/liberalluz/lethebar)

## 状态

一个世界，两个包，都已发布。`cultivation` 是原来内建在引擎里的五节点线性故事；
`cultivation-rogue` 是派遣实验——一个很弱的师尊把比他强得多的徒弟派出去，而只有一个人
听得见别人心里在想什么。两个包同属 collection `修仙 / Cultivation`，所以在引擎的包列表
里是「一个世界、两种玩法」。

版本号在 [`docs/specs/packs.md`](docs/specs/packs.md) 和
[Releases 页](https://github.com/liberalluz/lethebar-game-cultivation/releases)；
这份文件说明这个仓是什么，不说明每个包现在是哪一版。

## 故事

`packs/cultivation/` 是那条五节点故事，`x1` 到 `x5`，走完约十五分钟。`x1` 到 `x4`
各有两个选项，今天两个选项都通向 `x2`。这是故意的：那个包要验证的是引擎能装载、前进、
存档、读档。分叉是内容改动，以后在 `packs/cultivation/data/nodes.json` 里做。

`packs/cultivation-rogue/` 是另一种玩法。第一幕七个节点、四个结局；两个可见信念
（`belief.sword`、`belief.body`）会变成 `qi` 或 `insight`，四场心声戏决定你拿到哪个
结局。只有师姐听得见心声，所以同一句说出口的话可以有两个意思。

显示名是中文的「修仙」「修仙·派遣」，英文的 `Cultivation`、`Cultivation: Dispatch`；
id 是 `cultivation` 与 `cultivation-rogue`，玩家看不到 id。

## 安装一个包

每个包可安装的形态是它的 Release 资产 `<id>.zip`。引擎从压缩包根读 `manifest.json`，
校验它，然后解释清单里声明的协议。包是数据——引擎不会执行包里的任何代码。

下载压缩包，用引擎的安装动作装上。网页上的链接装不了：浏览器的 CORS 规则会挡住引擎
读取那些字节。两个已发布的包都在
[Releases 页](https://github.com/liberalluz/lethebar-game-cultivation/releases)。

存档键是 `save:cultivation:<slot>` 与 `save:cultivation-rogue:<slot>`，由各自的清单 id
推出。旧内建包写下的 `save:xiuxian:<slot>` 读不回来；那个 id 改过一次，当时还没有任何
包发布。

## 构建与发布

```bash
python infra/tool/release/release.py --root . --check
python infra/tool/release/release.py --root . --write --stream <stream> --version v<version>

python infra/tool/release/pack.py build packs/<id> --out dist
python infra/checks/check_pack.py dist/<id>.zip
python infra/tool/release/preflight.py --pack packs/<id>
python infra/tool/release/pack.py hash dist/<id>.zip
python infra/tool/release/pack.py publish dist/<id>.zip \
  --repo liberalluz/lethebar-game-cultivation \
  --tag pack/<id>/v<version> --apply
```

`release.py` 把 `changelog.d/` 里的片段合进 `CHANGELOG.md`，只删它消费掉的片段；先跑
它，笔记和压缩包才描述同一次发布。`stream` 取 `cultivation`、`cultivation-rogue` 或
`repo`，决定条目落在哪个标题下。

`build` 用清单 id 命名压缩包，所以目录名和 id 不可能对不上。`check_pack` 读的是压缩包
而不是源目录：根上只能有 `manifest.json`，其余都在 `data/`、`assets/` 或 `i18n/` 下。
`preflight` 收的是包的**目录**，检查清单、版本契约、压缩包、描述文件，最后两项检查
Release 是否存在、资产是否取得到——所以它最后两项只有在发布之后才会通过。`hash` 写出
跟压缩包同行的描述文件。`dist/` 被 git 忽略，永远不提交。

tag 形状是 `pack/<id>/v<version>`；压缩包里的版本和 tag 里的版本必须一致。发布需要
`gh` 已登录且有本仓写权限。

CI 跑同样的步骤。`.github/workflows/gate.yml` 用 `infra/` 里的 `pack.py` 与
`check_pack.py` 构建并检查 `packs/` 下每个包，所以 gate 和仓一起走。打 `pack/*` 标签时
它还会发布；PR 上它先检查分支里的提交有没有写清为什么存在。

## 命令

| 命令 | 做什么 |
|---|---|
| `python infra/tool/release/release.py --root . --check` | 校验 `changelog.d/` 片段，不改任何东西 |
| `python infra/tool/release/release.py --root . --write --stream <stream> --version v<version>` | 把片段合进 `CHANGELOG.md` 并删掉消费掉的片段 |
| `python infra/tool/release/pack.py build packs/<id> --out dist` | 把包压成 `dist/<id>.zip` |
| `python infra/checks/check_pack.py dist/<id>.zip` | 按包信封规则检查压缩包 |
| `python infra/tool/release/preflight.py --pack packs/<id>` | 检查清单、契约、压缩包、描述文件、Release 与资产 |
| `python infra/tool/release/pack.py hash dist/<id>.zip` | 在压缩包旁写出 `id-version.json` 描述文件 |
| `python infra/tool/release/pack.py publish ...` | 建 Release，上传压缩包与描述文件 |
| `python infra/tool/release/pack.py self-test` | 检查发布工具本身 |
| `python infra/checks/check_pack.py --self-test` | 检查信封检查器本身 |
| `python infra/checks/check_author_gate.py --template .github/workflows/gate.yml` | 检查 CI 模板仍是「构建、检查、发布」 |
| `python infra/checks/check_commit_body.py` | 检查新提交是否带 `Why:` 与 `Batch:` |
| `python infra/tool/merge/pr_merge.py --self-test` | 检查合并正文工具本身 |

两个 `self-test` 自己造夹具、自己清理，只需要一个可写的仓，别的都不要。

## 项目结构

| 路径 | 放什么 |
|---|---|
| `packs/cultivation/` | 五节点故事：`manifest.json`、`data/nodes.json`、`data/mechanics.json`、`data/i18n/en.json` |
| `packs/cultivation-rogue/` | 派遣实验：`manifest.json`、`data/nodes.json`、`data/state.json`、`data/rules.json`、`data/i18n/en.json` |
| `infra/checks/` | 包信封检查、CI 模板检查、提交正文检查 |
| `infra/tool/release/` | `pack.py`：构建、hash、发布；`release.py`：合成 changelog；`preflight.py`：发布前检查 |
| `infra/tool/merge/` | `pr_merge.py`：生成并校验 squash 合并正文 |
| `infra/tool/batch/`、`infra/tool/repo/` | 从 Nebula 拷来的批次与仓库工具 |
| `docs/` | 规格、决策、意图、操作手册（[docs/README.md](docs/README.md)） |

仓根只放上表列出的东西，加上惯例的根文件（`README`、`CONTRIBUTING`、`CONTRIBUTING.ai`、
`SECURITY`、`LICENSE`、`CHANGELOG`、`AGENTS`、`.gitignore`、`.gitattributes`、
`.nebula-scaffold.json`）。

## 文档

| 想找什么 | 在哪 |
|---|---|
| 仓里有哪些包、各自什么版本、是什么 | [docs/specs/packs.md](docs/specs/packs.md) |
| 这个仓为什么存在 | [docs/intent/](docs/intent/) |
| 一个包承诺什么 | [docs/specs/](docs/specs/) |
| 决定过什么、否掉过什么 | [docs/decisions/](docs/decisions/) |
| 怎么发一版 | [docs/runbooks/](docs/runbooks/) |

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
