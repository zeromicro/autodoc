---
title: Basic HTTP Service
description: Create and run a REST API service with go-zero.
sidebar:
  order: 2

---


This guide walks you through creating a minimal HTTP service using go-zero's API framework.

## Define the API

Create `hello.api`:

```text
syntax = "v1"

type HelloReq {
    Name string `path:"name,options=you|me"`
}

type HelloReply {
    Message string `json:"message"`
}

service hello-api {
    @handler HelloHandler
    get /hello/:name (HelloReq) returns (HelloReply)
}
```

## Generate Code

```bash
goctl api go -api hello.api -dir ./hello
```

Generated layout:

```text
hello/
├── etc/hello-api.yaml
├── internal/
│   ├── config/config.go
│   ├── handler/hellohandler.go
│   ├── logic/hellologic.go
│   ├── svc/servicecontext.go
│   └── types/types.go
└── hello.go
```

## Implement Logic

```go title="internal/logic/hellologic.go"
func (l *HelloLogic) Hello(req *types.HelloReq) (resp *types.HelloReply, err error) {
    return &types.HelloReply{
        Message: "Hello " + req.Name,
    }, nil
}
```

## Configuration

```yaml title="etc/hello-api.yaml"
Name: hello-api
Host: 0.0.0.0
Port: 8888
```

## Start the Server

```bash
cd hello && go mod tidy && go run hello.go
```

## Test

```bash
curl http://localhost:8888/hello/world
# {"message":"Hello world"}
```

## Error Handling

```go
import "github.com/zeromicro/go-zero/rest/httpx"

httpx.Error(w, errorx.NewCodeError(400, "invalid name"))
```
