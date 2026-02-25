---
title: 安装 IDE 插件
description: 为 VS Code、GoLand 和 Neovim 安装 go-zero 相关插件。
sidebar:
  order: 5
---

# 安装 IDE 插件

## VS Code

安装以下插件以获得完整的 Go 开发体验：

| 插件 | 功能 |
|---|---|
| [Go](https://marketplace.visualstudio.com/items?itemName=golang.Go) | Go 语言支持（必装） |
| [goctl](https://marketplace.visualstudio.com/items?itemName=zeromicro.goctl-vscode) | .api 文件语法高亮和补全 |
| [Proto Lint](https://marketplace.visualstudio.com/items?itemName=Plex.vscode-protolint) | .proto 文件代码检查 |
| [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) | 在编辑器内发送 HTTP 请求 |

安装后，将以下内容添加到 `settings.json`：

```json
{
  "go.toolsManagement.autoUpdate": true,
  "go.useLanguageServer": true,
  "gopls": {
    "ui.semanticTokens": true
  }
}
```

## GoLand / IntelliJ IDEA

在 **Plugins** 搜索并安装：

| 插件 | 功能 |
|---|---|
| **Go** | 内置支持（GoLand 自带） |
| **goctl** | .api 语法支持和 goctl 命令集成 |
| **Protocol Buffer** | .proto 支持 |

## Neovim

使用 `nvim-lspconfig` 配置 `gopls`：

```lua
require('lspconfig').gopls.setup({
  settings = {
    gopls = {
      analyses  = { unusedparams = true },
      staticcheck = true,
    },
  },
})
```

## 下一步

[Hello World 快速开始 →](../../guides/quickstart/hello-world)
