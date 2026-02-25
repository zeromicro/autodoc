---
title: 文档贡献
description: 如何为 go-zero 文档站点做贡献。
sidebar:
  order: 4

---

文档站点使用 [Astro Starlight](https://starlight.astro.build/) 构建，代码仓库为 `zeromicro/zerodoc`。

## 本地搭建

```bash
git clone https://github.com/zeromicro/zerodoc.git
cd zerodoc
npm install
npm run dev
# 打开 http://localhost:4321
```

## 文件结构

```text
src/content/docs/          # 英文内容（默认语言）
src/content/docs/zh-cn/    # 中文内容
```

每个页面是一个带有 YAML frontmatter 的 Markdown 或 MDX 文件：

```yaml
---
title: Page Title
description: Short description for SEO and the card grid.
sidebar:
  order: 3
---
```

## 写作指南

- 使用第二人称（"你"），主动语态。
- 代码块必须包含语言标记：```go、```bash、```yaml。
- 为代码块添加 `title` 提供上下文：```go title="main.go"`
- 保持句子简短；使用表格进行对比。
- 每个页面都应包含一个实际的代码示例。

## 新增页面

1. 在对应章节目录中创建文件。
2. 添加包含 `title`、`description` 和 `sidebar.order` 的 YAML frontmatter。
3. 在章节的 `index.md` 中添加链接。
4. 在 `zh-cn/` 下创建对应的中文翻译。

## 提交

向 `zeromicro/zerodoc` 的 `main` 分支提交 PR。部署预览会自动以 PR 评论形式发布。
