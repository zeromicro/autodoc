---
title: Create Project (GoLand)
description: Scaffold a new go-zero project from JetBrains GoLand.
sidebar:
  order: 3

---

## Overview

Having completed the Golang installation, we can formally enter golang for development, and the two currently mainstream editors are Goland VSCode, which will describe how to create a golang project using Golan.

Goland download please refer to [Goland Web Site](https://www.jetbrains.com/go/).

:::Note a reminder
The Goland version of the current document presentation is `GoLand 2022.1.4`, this may be different if your Goland version does not match.
:::

## Create project

Open Goland, click `New Project`, select `Go`, fill in the project name, click `Create`.

![create from goland](/resource/tasks/create/create-from-goland.png)

![create from goland](/resource/tasks/create/create-from-goland-main.png)

## New main.go

Right-click on `helloworld` to select `New`, choose `Go File`, enter file name `main`to enter.

![create from goland](/resource/tasks/create/create-main-from-goland.png)

![create from goland](/resource/tasks/create/create-main-from-goland2.png)

Enter the following code in `main.go`:

```go
package main

import "fmt"

func main() {
    fmt.Println("hello world!")
}

```

![create from goland](/resource/tasks/create/create-main-from-goland3.png)

## Run program

In Golin, there are several ways to start the program：

1. Right click on `main.go` file, select `Run go build main.go`.

![create from goland](/resource/tasks/create/run-in-goland1.png) ![create from goland](/resource/tasks/create/run-result-in-goland1.png)

1. In the `main.go` file content panel, the fifth line code was found `func main()` on the left triangle, click running.

![create from goland](/resource/tasks/create/run-in-goland2.png) ![create from goland](/resource/tasks/create/run-result-in-goland2.png)

1. Right-click on `main.go` file, select `Open In`, then select `Terminal`to open the terminal, and then enter the following instructions to run.

    ```bash
    $ go run main.go
    ```

    ![create from goland](/resource/tasks/create/run-in-goland3.png) ![create from goland](/resource/tasks/create/run-result-in-goland3.png)
