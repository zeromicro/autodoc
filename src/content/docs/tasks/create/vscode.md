---
title: Create Project (VS Code)
description: Scaffold a new go-zero project from Visual Studio Code.
sidebar:
  order: 4

---

## Overview

Once Golang is installed, we can formally enter golang for development. The two current mainstream editors are Goland VSCode, which will describe how to create a golang project using VSCode.

VScode download reference [VSCode official net](https://code.visualstudio.com/)

:::Note taps
Current document demo version is `Version: 1.74.1 (Universal)`, this may be different if your VScode version is not consistent.
:::

## Install Go Extension

Open VScode,click on the left extension button, search `Go`and install it.

![install go extension](/resource/tasks/create/vscode-go-extension.png)

## Create Go Project

Open VScode and click `Open...`in the workspace, select the specified directory or create a new folder as a project directory. Here I choose to create a new folder `hellowd`, return to the project.

![create from vscode](/resource/tasks/create/create-from-vscode.png)

## Create go module

In the top right corner of VScode, select `Toggle Panel` or use shortcuts `Command + J`, Strike `Terminal`, enter `go into the terminal and init helloowold`, go back and create a go module.

![open terminal](/resource/tasks/create/open-vscode-terminal.png) ![open terminal](/resource/tasks/create/create-go-module-from-vscode.png)

## New main.go

Create a new `main.go` file in the project directory `HELLOWORLD`, and enter the following code:

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello World!")
}
```

![create main.go](/resource/tasks/create/create-new-file.png)

## Run program

In the upper right corner of VScode, select `Toggle Panel` or use shortcut `Command + J`, click `Terminal`, enter `go run main.go`, go back, run the program.

```bash
$ go run main.go
Hello World!
```

![run program](/resource/tasks/create/run-in-vscode.png)
