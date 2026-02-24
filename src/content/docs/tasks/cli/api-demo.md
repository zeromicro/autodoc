---
title: API Demo Code Generation
description: Generate a complete HTTP service from an .api file using goctl.
sidebar:
  order: 2

---

## Overview

After completing the <a href="/docs/tasks/installation/goctl" target="_blank">goctl installation</a>, we can create a minimal HTTP service to get an overview of goctl's go-zero api service.

## Task Targets

1. Learn how to create a minimized HTTP service using goctl
1. Preliminary understanding of the project structure of go-zero

## Preparing

1. <a href="/docs/tasks" target="_blank">Complete golang installation</a>
1. <a href="/docs/tasks/installation/goctl" target="_blank">Complete goctl installation</a>

## Code Generation

```shell
# Create a workspace directory and navigate into it
$ mkdir -p ~/workspace/api && cd ~/workspace/api
# Generate a demo service
$ goctl api new demo
Done.
```

After executing the instruction, a demo directory will be generated under the current directory that contains a minimized HTTP service and we will check the directory structure of the service.

```shell
$ cd ~/workspace/api/demo
$ ls
demo.api demo.go  etc      go.mod   internal
$ tree
.
├── demo.api
├── demo.go
├── etc
│   └── demo-api.yaml
├── go.mod
└── internal
    ├── config
    │   └── config.go
    ├── handler
    │   ├── demohandler.go
    │   └── routes.go
    ├── logic
    │   └── demologic.go
    ├── svc
    │   └── servicecontext.go
    └── types
        └── types.go
```

:::note
API, RPC, Job Directory structure is similar to what the go-zero project structure can look at <a href="/docs/concepts/layout">Project Structure</a>
:::

## Write simple logic code

After completing the above code generation, we can find `~/workspace/api/demo/internal/logic/demologic.go` files, add codes between line `27` and `28`  :

```go
resp = new(types.Response)
resp.Message = req.Name
```

## Start service

After writing the above code, we can start the service with the following instructions：

```shell
# Enter service directory
$ cd ~/workspace/api/demo
# Tidy dependencies
$ go mod tidy
# Run the service
$ go run demo.go
```

When you see the output `Starting server at 0.0.0.0:8888...`, the service has started successfully. You can now send requests to the HTTP service.

**Access in terminal**
```bash
$ curl --request GET 'http://127.0.0.1:8888/from/me'
``````

When you see `{"message":"me"}` in the terminal, your service is running correctly.

**Access in Postman**
![postman](/resource/tasks/cli/task-api-demo-postman.png)

<center> Access in Postman </center>

The service has started successfully when you see the following response in Postman.

```json
{
    "message": "me"
}
```

Congratulations — you have created and started a minimal go-zero API service. For goctl CLI reference, see <a href="/docs/tutorials/cli/overview" target="_blank">CLI Tools</a>. For a complete HTTP service guide, see <a href="/docs/tutorials/http/server/configuration/service" target="_blank">HTTP Server</a>.
