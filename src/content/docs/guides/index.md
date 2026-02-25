---
title: Guides
description: Step-by-step guides for building with go-zero, from HTTP APIs to full microservice systems.
sidebar:
  order: 1

---

# Guides

Learn go-zero through practical, step-by-step guides organized by topic.

## HTTP Services

- [Basic HTTP Service](./http/basic.md) — Create your first REST API
- [Middleware](./http/server/middleware.md) — Request/response interceptors
- [JWT Authentication](./http/jwt-auth.md) — Secure endpoints with tokens
- [File Upload](./http/file-upload.md) — Handle multipart form data

## gRPC Services

- [gRPC Server](./grpc/server/) — Define and serve a protobuf service
- [gRPC Client](./grpc/client/) — Call gRPC services from Go
- [Interceptors](./grpc/interceptor.md) — Middleware for gRPC

## Database

- [MySQL](./database/mysql.md) — ORM-free data access with goctl models
- [Redis](./database/redis.md) — Caching and distributed data
- [MongoDB](./database/mongodb.md) — Document store integration

## Microservices

- [Service Discovery](./microservice/service-discovery.md) — Register and resolve services
- [Load Balancing](./microservice/load-balancing) — Distribute RPC traffic
- [Distributed Tracing](./microservice/distributed-tracing.md) — Trace requests across services

## Deployment

- [Docker](./deployment/docker.md) — Containerize go-zero services
- [Kubernetes](./deployment/kubernetes.md) — Deploy to a K8s cluster
