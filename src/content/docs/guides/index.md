---
title: Guides
description: Step-by-step guides for building with go-zero, from HTTP APIs to full microservice systems.
sidebar:
  order: 1

---


Learn go-zero through practical, step-by-step guides organized by topic.

## HTTP Services

- [Basic HTTP Service](./http/basic/) — Create your first REST API
- [Middleware](./http/server/middleware/) — Request/response interceptors
- [JWT Authentication](./http/jwt-auth/) — Secure endpoints with tokens
- [File Upload](./http/file-upload/) — Handle multipart form data

## gRPC Services

- [gRPC Server](./grpc/server/) — Define and serve a protobuf service
- [gRPC Client](./grpc/client/) — Call gRPC services from Go
- [Interceptors](./grpc/interceptor/) — Middleware for gRPC

## Database

- [MySQL](./database/mysql/) — ORM-free data access with goctl models
- [Redis](./database/redis/) — Caching and distributed data
- [MongoDB](./database/mongodb/) — Document store integration

## Microservices

- [Service Discovery](./microservice/service-discovery/) — Register and resolve services
- [Load Balancing](./microservice/load-balancing) — Distribute RPC traffic
- [Distributed Tracing](./microservice/distributed-tracing/) — Trace requests across services

## Deployment

- [Docker](./deployment/docker/) — Containerize go-zero services
- [Kubernetes](./deployment/kubernetes/) — Deploy to a K8s cluster
