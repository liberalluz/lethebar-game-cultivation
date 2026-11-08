<!-- translation-of: README.md -->
# 修仙

[English](README.md) · 简体中文

> 一个 Lethebar 包：五重境界，一步一选。
> 故事是数据，规则归引擎，而这个仓就是故事唯一的家。

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Pack](https://img.shields.io/badge/pack-cultivation-c0392b.svg)](packs/cultivation/manifest.json)
[![Version](https://img.shields.io/badge/version-1.0.0-97ca00.svg)](https://github.com/liberalluz/lethebar-game-cultivation/releases/tag/pack/cultivation/v1.0.0)
[![Spec](https://img.shields.io/badge/spec-2.0.0-007ec6.svg)](packs/cultivation/manifest.json)
[![Engine](https://img.shields.io/badge/engine-%3E%3D4.7.0%20%3C5.0.0-478cbf.svg)](https://github.com/liberalluz/lethebar)

协议：`linear@1`——一个节点、一个选择，走向下一个节点；没有选项的节点就是终点。

## 状态

**v1.0.0，尚未发布。** 包里是中英双语的完整五节点故事，可直接构建成引擎安装的压缩包。它原本是引擎里的内建故事；从引擎 `v0.6.0` 起内建故事不再随引擎发布，这样的包就是承载它的唯一方式。

- `mechanics`：`progress`——步数由已访问节点算出；包本身不声明任何规则（`data/mechanics.json` 是空的）。
- `locales`：`zh-CN`（默认）与 `en`，每个节点都有英文。
- 没有素材。没有图、没有音、没有字体——文字由引擎用它自己的字体绘制，所以包里不带。

## 故事

五个节点，`x1` 到 `x5`，从头走到尾约十五分钟。`x1` 到 `x4` 各有两个选项，目前两个都指向 `x2`。这是**有意**的：这一批只验证包能装、能走、能存读。分叉是内容改动，以后在 `packs/cultivation/data/nodes.json` 里做。

显示名中文是「修仙」，英文是 `Cultivation`；id 是 `cultivation`，玩家看不到。

## 使用这个包

可安装的形态是 Release 资产 `cultivation.zip`。引擎从压缩包根上读 `manifest.json`，校验它，然后解释 manifest 声明的协议。包就是数据——引擎不会执行包里的代码。

存档键是 `save:cultivation:<slot>`，由 manifest 的 id 推出。旧内建包写下的档（`save:xiuxian:<slot>`）读不回来；id 只改过这一次，改在任何包发布之前。

## 构建与发布

```bash
python infra/tool/release/release.py --root . --check
python infra/tool/release/release.py --root . --write --stream cultivation --version v1.0.0
python infra/tool/release/pack.py build packs/cultivation --out dist
python infra/checks/check_pack.py dist/cultivation.zip
python infra/tool/release/pack.py hash dist/cultivation.zip
python infra/tool/release/pack.py publish dist/cultivation.zip \
  --repo liberalluz/lethebar-game-cultivation \
  --tag pack/cultivation/v1.0.0 --apply
```

`release.py` 把 `changelog.d/` 里的片段并进 `CHANGELOG.md`，只删掉它消费过的那几个；先跑它，发布说明和压缩包才描述同一次发布。`build` 用 manifest 的 id 命名压缩包，所以目录名和 id 不可能对不上。`check_pack` 读的是压缩包本身而不是源码树：根上只许有 `manifest.json`，其余都必须落在 `data/`、`assets/` 或 `i18n/` 下。`hash` 写出随包一起上传的描述文件。`dist/` 不进 git，永远不提交。

标签形状是 `pack/<id>/v<version>`；包里的版本和标签里的版本必须一致。发布需要 `gh` 已认证且对本仓有写权限。

CI 跑的是同样三步：`.github/workflows/gate.yml` 用 `infra/` 里的 `pack.py` 与 `check_pack.py` 构建和检查，工具跟着这个仓一起走。打 `pack/*` 标签时它还会发布；PR 上它先查一遍这条分支的提交有没有写清缘由。

## 命令

| 命令 | 作用 |
|---|---|
| `python infra/tool/release/release.py --root . --check` | 校验 `changelog.d/` 的片段，不改任何东西 |
| `python infra/tool/release/release.py --root . --write --stream cultivation --version v1.0.0` | 把片段并进 `CHANGELOG.md` 并删掉已消费的片段 |
| `python infra/tool/release/pack.py build packs/cultivation --out dist` | 把包打成 `dist/cultivation.zip` |
| `python infra/checks/check_pack.py dist/cultivation.zip` | 按包信封检查压缩包 |
| `python infra/tool/release/pack.py hash dist/cultivation.zip` | 在压缩包旁写 `<id>-<version>.json` 描述文件 |
| `python infra/tool/release/pack.py publish ...` | 建 Release 并上传压缩包与描述文件 |
| `python infra/tool/release/pack.py self-test` | 自检发布工具 |
| `python infra/checks/check_pack.py --self-test` | 自检信封检查器 |
| `python infra/checks/check_author_gate.py --template .github/workflows/gate.yml` | 检查 CI 模板仍是「构建、检查、发布」三步 |
| `python infra/checks/check_commit_body.py` | 检查新提交带 `Why:` 与 `Batch:` |
| `python infra/tool/merge/pr_merge.py --self-test` | 自检合并信息工具 |

两个 `self-test` 自己造夹具、自己清理，只需要一个可写的仓，别的都不要。

## 项目结构

| 路径 | 内容 |
|---|---|
| `packs/cultivation/` | 包本身：`manifest.json`、`data/nodes.json`、`data/mechanics.json`、`data/i18n/en.json` |
| `infra/checks/` | 包信封检查、CI 模板检查、提交信息检查 |
| `infra/tool/release/` | `pack.py`：build、hash、publish；`release.py`：合并 changelog |
| `infra/tool/merge/` | `pr_merge.py`：生成并校验 squash 合并信息 |
| `infra/tool/batch/`、`infra/tool/repo/` | 随仓携带的 Nebula 批次与仓库工具 |
| `docs/` | 规格、决策、意图、操作手册（见 [docs/README.md](docs/README.md)） |

仓库根上只放上表列出的东西，加上常规根文件（`README`、`CONTRIBUTING`、`CONTRIBUTING.ai`、`SECURITY`、`LICENSE`、`CHANGELOG`、`AGENTS`、`.gitignore`、`.gitattributes`、`.nebula-scaffold.json`）。

## 文档

| 想找什么 | 在哪 |
|---|---|
| 这个仓为什么存在 | [docs/intent/](docs/intent/) |
| 这个包承诺了什么 | [docs/specs/](docs/specs/) |
| 决定过什么、否掉过什么 | [docs/decisions/](docs/decisions/) |
| 怎么发一个版本 | [docs/runbooks/](docs/runbooks/) |

## 参与贡献

- 开 PR 之前先读 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 用 AI 改文字或代码？也读 [CONTRIBUTING.ai.md](CONTRIBUTING.ai.md)：AI 改动需要人评审并附证据，作者不能自审。
- 不要为了让测试通过而改故事；两个选项都指向 `x2` 是有意的。

## 安全

见 [SECURITY.md](SECURITY.md)。引擎把包当不可信输入；本仓把引擎的信封规则当作「包能装什么」的权威。

## 许可

本包以 [Apache License 2.0](LICENSE) 授权：允许使用、修改与再分发，条件是保留版权声明与许可正文。播放它的引擎另行授权，见引擎自己的仓。

本仓不携带任何第三方材料——没有字体、图片或声音——因此没有 `NOTICE` 文件。将来若包里带了别处的素材，它的声明与许可条款要在同一个 PR 里一起加。
