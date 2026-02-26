---
title: IDE Plugins
description: Recommended IDE extensions for Go, Proto, and productivity.
sidebar:
  order: 5
---


The right IDE setup gives you auto-completion for `.api` files, inline errors, and one-click code generation.

## VS Code

Install the following extensions (search in the Extensions panel or click the links):

| Extension | Purpose |
|---|---|
| [Go](https://marketplace.visualstudio.com/items?itemName=golang.Go) | Language server, debugging, test runner |
| [goctl](https://marketplace.visualstudio.com/items?itemName=zeromicro.goctl-vscode) | Syntax highlight + snippets for `.api` files |
| [vscode-proto3](https://marketplace.visualstudio.com/items?itemName=zxh404.vscode-proto3) | Syntax highlight for `.proto` files |
| [Error Lens](https://marketplace.visualstudio.com/items?itemName=usernamehw.errorlens) | Inline error messages |

After installing the Go extension, open any `.go` file and VS Code will prompt you to install `gopls`, `dlv`, and other tools — accept all prompts.

### Validate gopls is running

Open a `.go` file. Hover over a function name — you should see a documentation popup. If not, run:

```
Ctrl+Shift+P → Go: Install/Update Tools → select all → OK
```

## GoLand / IntelliJ IDEA

| Plugin | Purpose |
|---|---|
| Go (built-in in GoLand) | Full Go support |
| [Protocol Buffers](https://plugins.jetbrains.com/plugin/14004-protocol-buffers) | `.proto` syntax + navigation |
| [goctl plugin](https://plugins.jetbrains.com/plugin/15414-goctl) | `.api` file syntax highlight |

In GoLand: **Settings → Go → GOROOT** — ensure it points to your Go installation.

## Neovim

Use [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig) with `gopls`:

```lua
require('lspconfig').gopls.setup{}
```

Install `gopls`:

```bash
go install golang.org/x/tools/gopls@latest
```

## Next Step

[Understand API DSL syntax →](../../../reference/dsl/api-syntax)
