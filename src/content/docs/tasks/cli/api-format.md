---
title: API File Formatting
description: Format go-zero .api files with goctl.
sidebar:
  order: 3

---


## Overview

After an `.api` file is written, the content may be poorly formatted, for example:

```go
syntax= "v1"

info(
key1:value1
key2:value2
longkey:longvalue
)

type Foo {
  Bar string
    Baz int
}
```

This `.api` file is unformatted. Use `goctl api format` to reformat it.

## Task Targets

1. familiar with the use of goctl api format
1. Learn about the function of the goctl api format command

## Preparing

1. <a href="/docs/tasks/installation/goctl" target="_blank">Complete goctl installation</a>

## Format api file

1. Create an api file and copy the following content to the `demo.api` file

    ```go
    syntax = "v1"

    type User {
        Id int64 `json:"id"`
        Name string `json:"name"`
        Age int `json:"age"`
        Description string `json:"description"`
    }

    type Student {
        Id int64 `json:"id"`
        No int64 `json:"no"`
        Name string `json:"name"`
        Age int `json:"age"`
        Description string `json:"description"`
    }

    service User {
        @handler ping
        get /ping
    }
    ```

1. Create workspace and directory

    ```bash
    $ mkdir -p ~/workspace/api/format
    ```

1. Copy `demo.api` to `~/workspace/api/format/`

1. Format api file

    ```bash
    $ cd ~/workspace/api/format
    $ goctl api format --dir demo.api
    ```

1. View formatted api files

    ```bash
    syntax = "v1"

    type User {
        Id          int64  `json:"id"`
        Name        string `json:"name"`
        Age         int    `json:"age"`
        Description string `json:"description"`
    }

    type Student {
        Id          int64  `json:"id"`
        No          int64  `json:"no"`
        Name        string `json:"name"`
        Age         int    `json:"age"`
        Description string `json:"description"`
    }

    service User {
        @handler ping
        get /ping
    }
    ```
