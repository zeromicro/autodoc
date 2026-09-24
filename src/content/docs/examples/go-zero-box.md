---
title: go-zero-box Project Template
description: A go-zero project template with APIs, asynchronous queues, scheduled tasks, and a CLI.
sidebar:
  order: 6
---

go-zero-box is a community-maintained project template for learning business layering, dependency injection, and service organization beyond a basic API example. Based on go-zero v1.9.4, it can run the API, queue consumers, and scheduler together or deploy them separately.

Repository：[go-zero-box](https://github.com/prf16/go-zero-box)

## Capability

| Capability | Implementation |
| --- | --- |
| API service | Modular API DSL with login, registration, and JWT authentication examples |
| Queues and scheduled tasks | asynq for queue processing and task scheduling |
| Command-line tools | Cobra for registering and running custom commands |
| Dependency management | Wire generates dependency injection code; ServiceContext groups dependencies |
| Development tools | Makefile targets for builds, API generation, and dependency injection generation |

## Get the Code

```bash
git clone https://github.com/prf16/go-zero-box.git
cd go-zero-box
go mod download
```

## Prerequisites

Go 1.23.5 or later, MySQL 5.7 or later, and Redis.

Update `Database`, `Redis`, and `Asynqx` in `app/etc/app.yaml` for your environment. Set your own `JwtAuth.AccessSecret` before using authentication examples. See `deploy/sql/v1.sql` for the database schema and the project README for initialization details.

## Start the Service

Run the API service from the project root:

```bash
go run . server:api
```

With the default configuration, access the Hello endpoint and Swagger documentation:

```bash
curl http://localhost:8001/api/hello
```

[Swagger](http://localhost:8001/api/doc)

### Other Run Modes

| Command | Purpose |
| --- | --- |
| `go run . server:queue` | Start queue consumers |
| `go run . server:scheduler` | Start the scheduler |
| `go run . server:all` | Run the API, queue consumers, and scheduler together |
| `go run . hello:world` | Run the sample command |

## RPC Extension

The companion [go-zero-box-rpc](https://github.com/prf16/go-zero-box-rpc) project provides the RPC service. Configure `UserRpc` and check client initialization in `pkg/rpc/client.go` before integrating it. The current example leaves that initialization disabled; complete the connection setup before calling RPC endpoints.

## Key Takeaways

- Organize API definitions, handlers, logic, and services by business module.
- Manage dependencies with Wire and ServiceContext.
- Reuse business services across HTTP requests, queue tasks, and CLI commands.
