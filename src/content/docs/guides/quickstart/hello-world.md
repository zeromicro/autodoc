---
title: Hello World
description: Build and run your first go-zero API service in under 5 minutes.
sidebar:
  order: 8
---


This page walks you through creating, running, and testing your first go-zero HTTP service from scratch. The whole thing takes about 5 minutes.

## Prerequisites

- Go 1.21+ installed (`go version`)
- goctl installed (`goctl --version`)

Not installed? See [Install Go](../../../getting-started/installation/golang) and [Install goctl](../../../getting-started/installation/goctl).

## Step 1 — Scaffold the Project

```bash
goctl api new greet
cd greet
go mod tidy
```

This creates a complete project layout:

```
greet/
├── etc/
│   └── greet-api.yaml        # config: port, logging, etc.
├── internal/
│   ├── config/
│   │   └── config.go          # config struct
│   ├── handler/
│   │   ├── greethandler.go    # HTTP handler (auto-generated)
│   │   └── routes.go          # route registration
│   ├── logic/
│   │   └── greetlogic.go      # ← edit this: your business logic
│   └── svc/
│       └── servicecontext.go  # shared dependencies (DB, cache, etc.)
└── greet.go                   # main entrypoint
```

## Step 2 — Look at the Generated DSL

Open `greet.api`:

```go
type Request {
    Name string `path:"name,options=you|me"`
}

type Response {
    Message string `json:"message"`
}

service greet-api {
    @handler Greet
    get /from/:name (Request) returns (Response)
}
```

This single file is the source of truth. `goctl` generated all the Go code from it.

## Step 3 — Run the Service

```bash
go run greet.go
```

Expected output:

```
Starting server at 0.0.0.0:8888...
```

## Step 4 — Test It

Open a new terminal:

```bash
curl http://localhost:8888/from/you
```

Expected response:

```json
{"message":"Hello you"}
```

## Step 5 — Add Custom Logic

Open `internal/logic/greetlogic.go`. You'll see:

```go
func (l *GreetLogic) Greet(req *types.Request) (resp *types.Response, err error) {
    // todo: add your logic here and delete this line
    return
}
```

Replace it with:

```go
func (l *GreetLogic) Greet(req *types.Request) (resp *types.Response, err error) {
    return &types.Response{
        Message: fmt.Sprintf("Hello %s, welcome to go-zero!", req.Name),
    }, nil
}
```

Add the `fmt` import at the top of the file if needed. Save and re-run:

```bash
go run greet.go
```

```bash
curl http://localhost:8888/from/alice
# {"message":"Hello alice, welcome to go-zero!"}
```

## How the Request Flows

```
curl /from/alice
  → routes.go         (route matching)
  → greethandler.go   (parse + validate request)
  → greetlogic.go     (your business logic)
  → greethandler.go   (serialize response)
  → {"message":"..."}
```

You only write the logic. go-zero handles routing, parsing, validation, serialization, and error wrapping.

## Next Steps

- [Create a full API service with custom types →](./api-service)
- [Create an RPC service →](./rpc-service)
