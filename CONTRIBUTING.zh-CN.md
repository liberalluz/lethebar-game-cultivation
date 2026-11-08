<!-- translation-of: CONTRIBUTING.md -->
# 贡献指南

[English](CONTRIBUTING.md) · 简体中文

## 开始之前

- 读 `AGENTS.md`。
- 读 `docs/specs/git-conventions.md` §2–§4。
- AI 参与的改动读 `CONTRIBUTING.ai.md`。
- 一个改动 = 一个批次 = 一个 PR。

## 流程

```text
批次卡 -> 分支 -> 提交 -> PR -> 一个批准 -> squash 合并
```

- 先开批次卡，PR 链到它。
- `main` 受保护：一个 code owner 批准、线性历史。
- 不要直接推 `main`。
- 分支保持短生命周期。
- 填写 PR 模板，不留占位符；空白正文或还留着模板注释的，直接退回。
- 合并前必需检查必须通过。

## 评审

- 作者不能自审；作者是 AI 时，由人签字。
- 评审 diff、测试和证据。
- 豁免要记录，不能只口头同意。

## 合并

- 用 `gh pr merge --squash` 合并，不要直接推 `main`。
- 多笔提交的 squash 合并要传 `--subject` 与 `--body-file`；正文由
  `python infra/tool/merge/pr_merge.py` 生成，不要手打。规则和已经留在历史里的
  两种错法见 `docs/specs/git-conventions.md` §4。
- 合并之后跑 `python infra/tool/merge/pr_merge.py --verify-only`；它读什么、
  为什么别的检查覆盖不到，也见 §4。
