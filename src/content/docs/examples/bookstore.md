---
title: Bookstore
description: A complete example with API service calling an RPC service, backed by MySQL.
sidebar:
  order: 4
---

# Bookstore

The go-zero official bookstore example is the canonical starting point for multi-service development. It demonstrates how an HTTP API gateway delegates to a backend gRPC service, which reads and writes MySQL through a goctl-generated model.

## Architecture

```text
Client
  │
  ▼  HTTP :8888
bookstore-api   (go-zero REST server)
  │
  ▼  gRPC :8080
bookstore-rpc   (zrpc server)
  │
  ▼
 MySQL
```

## Get the Code

```bash
git clone https://github.com/zeromicro/go-zero.git
cd go-zero/example/bookstore
```

Directory layout:

```
bookstore/
├── api/                    # HTTP gateway
│   ├── bookstore.go        # entry point
│   ├── etc/
│   │   └── bookstore-api.yaml
│   └── internal/
│       ├── config/
│       ├── handler/        # HTTP handlers (generated)
│       ├── logic/          # business logic
│       ├── svc/            # ServiceContext
│       └── types/          # request/response structs
├── rpc/                    # gRPC backend
│   ├── bookstore.go
│   ├── etc/
│   │   └── bookstore.yaml
│   ├── internal/
│   │   ├── config/
│   │   ├── logic/          # gRPC handlers
│   │   ├── model/          # MySQL model (generated)
│   │   └── svc/
│   └── pb/                 # protobuf definitions
└── shared/                # shared proto types
```

## Step-by-Step Walkthrough

### 1. Create the Database

```sql
CREATE DATABASE bookstore;
USE bookstore;

CREATE TABLE `book` (
  `book`  varchar(255) NOT NULL COMMENT 'book name',
  `price` int          NOT NULL DEFAULT 0 COMMENT 'book price'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 2. Generate the MySQL Model

```bash
cd rpc
goctl model mysql ddl -src ./internal/model/book.sql -dir ./internal/model -cache
```

### 3. Configure Services

```yaml title="rpc/etc/bookstore.yaml"
Name: bookstore.rpc
ListenOn: 0.0.0.0:8080

DataSource: root:password@tcp(127.0.0.1:3306)/bookstore?parseTime=true
Cache:
  - Host: 127.0.0.1:6379
```

```yaml title="api/etc/bookstore-api.yaml"
Name: bookstore-api
Host: 0.0.0.0
Port: 8888

Bookstore:
  Etcd:
    Hosts:
      - 127.0.0.1:2379
    Key: bookstore.rpc
```

### 4. ServiceContext — RPC Client Wiring

```go title="api/internal/svc/servicecontext.go"
type ServiceContext struct {
    Config     config.Config
    Bookstore  bookstore.Bookstore   // generated gRPC client stub
}

func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:    c,
        Bookstore: bookstore.NewBookstore(zrpc.MustNewClient(c.Bookstore)),
    }
}
```

### 5. Start Services

```bash
# Terminal 1 — RPC backend
cd rpc && go run bookstore.go -f etc/bookstore.yaml

# Terminal 2 — API gateway
cd api && go run bookstore.go -f etc/bookstore-api.yaml
```

### 6. Test

```bash
# Add a book
curl -X POST http://localhost:8888/add \
  -H "Content-Type: application/json" \
  -d '{"book":"The Go Programming Language","price":42}'
# {"ok":true}

# Check stock
curl "http://localhost:8888/check?book=The+Go+Programming+Language"
# {"found":true,"price":42}
```

## Key Concepts Demonstrated

| Concept | Location | Description |
|---------|----------|-------------|
| API definition | `api/bookstore.api` | REST routes using `.api` DSL |
| Proto definition | `rpc/pb/bookstore.proto` | gRPC service contracts |
| goctl model | `rpc/internal/model/` | Type-safe MySQL access with cache |
| ServiceContext | `api/internal/svc/` | Dependency injection container |
| RPC client | `api/internal/logic/` | Calling gRPC backend from logic layer |
| etcd discovery | `api/etc/bookstore-api.yaml` | RPC target resolved via etcd |

## Common goctl Commands Used

```bash
# Regenerate API gateway code
cd api && goctl api go -api bookstore.api -dir .

# Regenerate gRPC server/client stubs
cd rpc && goctl rpc protoc pb/bookstore.proto \
  --go_out=./pb --go-grpc_out=./pb --zrpc_out=.

# Regenerate model from DDL
goctl model mysql ddl -src ./internal/model/book.sql \
  -dir ./internal/model -cache
```
