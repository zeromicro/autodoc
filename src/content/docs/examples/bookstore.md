---
title: Bookstore
description: A complete example with API service calling an RPC service, backed by MySQL.
sidebar:
  order: 4
---

# Bookstore

The go-zero official example: an API gateway that delegates to a backend RPC service, using MySQL for storage.

## Architecture

```text
Client → bookstore-api (HTTP) → bookstore-rpc (gRPC) → MySQL
```

## Repository

```bash
git clone https://github.com/zeromicro/go-zero.git
cd go-zero/example/bookstore
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| `api/` | 8888 | HTTP gateway |
| `rpc/` | 8080 | gRPC book service |

## Start RPC

```bash
cd rpc
go run bookstore.go -f etc/bookstore.yaml
```

## Start API

```bash
cd api
go run bookstore.go -f etc/bookstore-api.yaml
```

## Test

```bash
# Add a book
curl -X POST http://localhost:8888/add \
  -H "Content-Type: application/json" \
  -d '{"book":"The Go Programming Language","price":42}'

# Check stock
curl "http://localhost:8888/check?book=The+Go+Programming+Language"
```

## Key Concepts Demonstrated

- API gateway routing to RPC backend
- goctl model generation from MySQL DDL
- ServiceContext wiring of RPC client
