---
title: Docker 部署
description: 将 go-zero 服务打包并运行在 Docker 中。
sidebar:
  order: 15
---

go-zero 服务编译为单一静态二进制文件，可构建出非常小的 Docker 镜像。

## Dockerfile

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o service .

FROM alpine:3.20
RUN apk --no-cache add ca-certificates tzdata
WORKDIR /app
COPY --from=builder /app/service .
COPY etc/ ./etc/
EXPOSE 8888
CMD ["./service", "-f", "etc/app.yaml"]
```

## 构建与运行

```bash
docker build -t myapp:latest .
docker run -p 8888:8888 myapp:latest
```

## Docker Compose

```yaml title="docker-compose.yaml"
services:
  api:
    build: ./api
    ports: ["8888:8888"]
    depends_on: [mysql, redis, etcd]

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: myapp
    volumes: [mysql_data:/var/lib/mysql]

  redis:
    image: redis:7-alpine

  etcd:
    image: bitnami/etcd:latest
    environment:
      ALLOW_NONE_AUTHENTICATION: "yes"

volumes:
  mysql_data:
```

```bash
docker compose up -d
```

## 健康检查

```dockerfile
HEALTHCHECK --interval=10s --timeout=3s \
  CMD wget -qO- http://localhost:8888/healthz || exit 1
```
