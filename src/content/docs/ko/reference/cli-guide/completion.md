---
title: Shell Completion
description: go-zero의 Shell Completion에 대해 설명합니다.
sidebar:
  order: 16

---

## 개요


## goctl completion directive

```bash
$ goctl completion --help
Generate the autocompletion script for goctl for the specified shell.
참고: each sub-command's help for details on how to use the generated script.

Usage:
  goctl completion [command]

Available 명령s:
  bash        Generate the autocompletion script for bash
  fish        Generate the autocompletion script for fish
  powershell  Generate the autocompletion script for powershell
  zsh         Generate the autocompletion script for zsh

Flags:
  -h, --help   help for completion

Use "goctl completion [command] --help" for more information about a command.
```


:::note 위한 current shell
:::

### goctl completion bash directive

```bash
$ goctl completion bash --help
Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package.
If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:

    source <(goctl completion bash)

To load completions for every new session, execute once:

#### Linux:

    goctl completion bash > /etc/bash_completion.d/goctl

#### macOS:

    goctl completion bash > $(brew --prefix)/etc/bash_completion.d/goctl

You will need to start a new shell for this setup to take effect.

Usage:
  goctl completion bash

Flags:
  -h, --help              help for bash
      --no-descriptions   disable completion descriptions
```


1 Temporary entry 으로 force


```bash
$ source <(goctl completion bash)
```

2 Permanent entry 으로 force


**Linux**
```bash
$ goctl completion bash > /etc/bash_completion.d/goctl
```

**MacOS**
```bash
$ goctl completion bash > $(brew --prefix)/etc/bash_completion.d/goctl
```

### goctl completion fish directive

```bash
$ goctl completion fish --help
Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

    goctl completion fish | source

To load completions for every new session, execute once:

    goctl completion fish > ~/.config/fish/completions/goctl.fish

You will need to start a new shell for this setup to take effect.

Usage:
  goctl completion fish [flags]

Flags:
  -h, --help              help for fish
      --no-descriptions   disable completion descriptions
```

1 Temporary entry 으로 force


```bash
$ goctl completion fish | source
```

2 Permanent entry 으로 force

```bash
$ goctl completion fish > ~/.config/fish/completions/goctl.fish
```

### goctl completion powershell directive

```bash
$ goctl completion powershell --help
Generate the autocompletion script for powershell.

To load completions in your current shell session:

    goctl completion powershell | Out-String | Invoke-Expression

To load completions for every new session, add the output of the above command
to your powershell profile.

Usage:
  goctl completion powershell [flags]

Flags:
  -h, --help              help for powershell
      --no-descriptions   disable completion descriptions
```

1 Temporary entry 으로 force


```bash
$ goctl completion powershell | Out-String | Invoke-Expression
```

2 Permanent entry 으로 force

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

```bash
$ goctl completion powershell | Out-String | Invoke-Expression
```

### goctl completion zsh directive

```bash
$ goctl completion zsh --help
Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need
to enable it.  You can execute the 다음 once:

    echo "autoload -U compinit; compinit" >> ~/.zshrc

To load completions in your current shell session:

    source <(goctl completion zsh); compdef _goctl goctl

To load completions for every new session, execute once:

#### Linux:

    goctl completion zsh > "${fpath[1]}/_goctl"

#### macOS:

    goctl completion zsh > $(brew --prefix)/share/zsh/site-functions/_goctl

You will need to start a new shell for this setup to take effect.

Usage:
  goctl completion zsh [flags]

Flags:
  -h, --help              help for zsh
      --no-descriptions   disable completion descriptions
```

:::tip
이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

```bash
echo "autoload -U compinit; compinit" >> ~/.zshrc
```

:::

1 Temporary entry 으로 force


```bash
$ source <(goctl completion zsh); compdef _goctl goctl
```

2 Permanent entry 으로 force


**Linux**
```bash
$ goctl completion zsh > "${fpath[1]}/_goctl"
```

**MacOS**
```bash
$ goctl completion zsh > $(brew --prefix)/share/zsh/site-functions/_goctl
```
