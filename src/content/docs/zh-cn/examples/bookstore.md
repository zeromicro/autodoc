---
title: 书店示例
description: 完整示例：API 网关调用 RPC 服务，后端使用 MySQL 存储。
sidebar:
  order: 4

---

# 书店示例

go-zero 官方示例：HTTP API 网关委托给后端 gRPC 服务，使用 MySQL 持久化数据。

## 架构

```text
客户端
  │
  ▼ HTTP :8888
bookstore-api  （go-zero REST 服务）
  │
  ▼ gRPC :8080
bookstore-rpc  （zrpc 服务）
  │
  ▼
 MySQL
```

## 获取代码

```bash
git clone https://github.com/zeromicro/go-zero.git
cd go-zero/example/bookstore
```

目录结构：

```
bookstore/
├── api/                    # HTTP 网关
│   ├── bookstore.go
│   ├── etc/bookstore-api.yaml
│   └── internal/
│       ├── handler/        # HTTP 处理函数
│       ├── logic/          # 业务逻辑
│       ├── svc/            # ServiceContext
│       └── types/
├── rpc/                    # gRPC 后端
│   ├── bookstore.go
│   ├── etc/bookstore.yaml
│   ├── internal/
│   │   ├── logic/          # gRPC 处理函数
│   │   ├── model/          # MySQL model
│   │   └── svc/
│   └── pb/                 # Protobuf 定义
└── shared/
```

## 分步操作

### 1. 创建数据库

```sql
CREATE DATABASE bookstore;
USE bookstore;

CREATE TABLE `book` (
  `book`  varchar(255) NOT NULL COMMENT '书名',
  `price` int          NOT NULL DEFAULT 0 COMMENT '价格'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 2. 生成 MySQL Model

```bash
cd rpc
goctl model mysql ddl -src ./internal/model/book.sql \
  -dir ./internal/model -cache
```

### 3. 配置文件

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

### 4. ServiceContext — RPC 客户端注入

```go title="api/internal/svc/servicecontext.go"
type ServiceContext struct {
    Config    config.Config
    Bookstore bookstore.Bookstore  // 生成的 gRPC 客户端打钉
}

func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:    c,
        Bookstore: bookstore.NewBookstore(zrpc.MustNewClient(c.Bookstore)),
    }
}
```

### 5. 启动服务

```bash
# 终端 1 — 启动 RPC
cd rpc && go run bookstore.go -f etc/bookstore.yaml

# 终端 2 — 启动 API
cd api && go run bookstore.go -f etc/bookstore-api.yaml
```

### 6. 测试

```bash
# 添加书籍
curl -X POST http://localhost:8888/add \
  -H "Content-Type: application/json" \
  -d '{"book":"The Go Programming Language","price":42}'
# {"ok":true}

# 查询库存
curl "http://localhost:8888/check?book=The+Go+Programming+Language"
# {"found":true,"price":42}
```

## 核心知识点

| 知识点 | 位置 | 说明 |
|--------|------|------|
| API 定义 | `api/bookstore.api` | REST 路由 DSL |
| Proto 定义 | `rpc/pb/bookstore.proto` | gRPC 服务合同 |
| goctl model | `rpc/internal/model/` | 带缓存的类型安全 MySQL 访问 |
| ServiceContext | `api/internal/svc/` | 依赖注入容器 |
| RPC 客户端调用 | `api/internal/logic/` | 在 logic 层调用 gRPC 后端 |
| etcd 服务发现 | `api/etc/bookstore-api.yaml` | 通过 etcd 解析 RPC 地址 |

## 常用 goctl 命令

```bash
# 重新生成 API 网关代码
cd api && goctl api go -api bookstore.api -dir .

# 重新生成 gRPC 存格/客户端打钉
cd rpc && goctl rpc protoc pb/bookstore.proto \
  --go_out=./pb --go-grpc_out=./pb --zrpc_out=.

# 重新生成 model
goctl model mysql ddl -src ./internal/model/book.sql \
  -dir ./internal/model -cache
```
