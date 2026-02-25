---
title: PR 流程
description: 如何向 go-zero 提交并合入 Pull Request。
sidebar:
  order: 3

---

## 提交 PR 之前

1. 搜索已有的 Issue 和 PR 以避免重复。
2. 对于重大改动，先创建 Issue 讨论方案。
3. 确保所有测试通过：`go test ./...`
4. 运行 `golangci-lint run` 并修复所有问题。
5. 运行 `goimports -w ./...` 格式化代码。

## PR 标题

遵循 Conventional Commits 规范：

```text
fix: prevent goroutine leak in http server shutdown
feat: add Redis cluster support to cache package
docs: update quickstart guide for v1.7
refactor: simplify breaker state machine
```

## PR 描述

使用以下模板：

```markdown
## 概述
简要描述本次改动。

## 变更内容
- 列出修改的文件/包及原因

## 测试
描述如何测试本次改动。

## 是否有破坏性变更？
是 / 否。如果是，描述影响范围和迁移方式。
```

## 审查流程

1. 至少需要**一位维护者审查**通过。
2. CI 必须全部通过（测试 + lint + 构建）。
3. 审查通过后，维护者使用 **squash merge** 合入。

## 合入之后

- PR 作者会在发版说明中被致谢。
- 在 PR 描述中使用 `Fixes #<issue>` 关闭相关 Issue。
