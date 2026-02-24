---
title: Docker Deployment
description: Build and deploy go-zero services with Docker, including multi-stage builds and CI/CD automation with GitHub Actions.
sidebar:
  order: 4

---

## Overview

This guide explains how to containerize and deploy a go-zero service using Docker after development is complete.

### Benefits of Containerizing with Docker

1. **Consistency** — Containers run identically across dev, test, staging, and production, eliminating "works on my machine" issues.
2. **Portability** — Run the same container on any cloud platform, OS, or infrastructure without code changes.
3. **Isolation** — Each container runs in its own isolated environment, preventing dependency conflicts.
4. **CI/CD integration** — Docker integrates with CI/CD tools to automate build, test, and deployment pipelines.
5. **Scalability** — Containers scale horizontally on demand to handle traffic spikes.

## Generating a Dockerfile with goctl

After finishing the API or RPC service, use goctl to generate the Dockerfile:

1. Enter the service directory (`api/`, `rpc/`, or `mq/`).
2. Run:

```bash
goctl docker -go <main-file>.go
```

Replace `<main-file>.go` with your service's `main.go`. For example:

```bash
goctl docker -go video.go
```

goctl generates a Dockerfile in the current directory:

```dockerfile
FROM golang:alpine AS builder

LABEL stage=gobuilder

ENV CGO_ENABLED 0
ENV GOPROXY https://goproxy.cn,direct
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk update --no-cache && apk add --no-cache tzdata

WORKDIR /build

ADD go.mod .
ADD go.sum .
RUN go mod download
COPY . .
COPY server/video/rpc/etc /app/etc
RUN go build -ldflags="-s -w" -o /app/video server/video/rpc/video.go


FROM scratch

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /usr/share/zoneinfo/Asia/Shanghai /usr/share/zoneinfo/Asia/Shanghai
ENV TZ Asia/Shanghai

WORKDIR /app
COPY --from=builder /app/video /app/video
COPY --from=builder /app/etc /app/etc

CMD ["./video", "-f", "etc/video.yaml"]
```

### Dockerfile Walkthrough

**Stage 1 — Build**

```dockerfile
FROM golang:alpine AS builder
ENV CGO_ENABLED 0
ENV GOPROXY https://goproxy.cn,direct
```

- Uses a lightweight Alpine-based Go image.
- Disables CGO for a fully static binary.
- Configures the Go module proxy for faster downloads.

```dockerfile
RUN apk update --no-cache && apk add --no-cache tzdata
```

Installs timezone data for correct time formatting in logs.

```dockerfile
ADD go.mod .
ADD go.sum .
RUN go mod download
COPY . .
RUN go build -ldflags="-s -w" -o /app/video server/video/rpc/video.go
```

Downloads dependencies first (leveraging Docker layer caching), then builds the binary. `-ldflags="-s -w"` strips debug symbols to reduce binary size.

**Stage 2 — Final image**

```dockerfile
FROM scratch
```

Uses the minimal `scratch` base image — no OS, no shell, just the binary.

```dockerfile
COPY --from=builder /etc/ssl/certs/ca-certificates.crt ...
COPY --from=builder /usr/share/zoneinfo/Asia/Shanghai ...
ENV TZ Asia/Shanghai
```

Copies only the TLS certificates and timezone data needed at runtime.

```dockerfile
CMD ["./video", "-f", "etc/video.yaml"]
```

Starts the service with its config file.

:::tip Notes
- If your service has additional config files, copy them in both the build and final stages.
- `scratch` has no shell. If you need bash for debugging, use `alpine` instead — the size increase is minimal.
- If your code uses **generics**, use `FROM golang:1.20.5-alpine AS builder` or any Go ≥ 1.18.
:::

## Building and Pushing the Image

### Option 1 — Local build

From the project root (where `go.mod` is):

```bash
docker build -t your-image-name:tag -f /path/to/Dockerfile .
```

### Option 2 — Docker Compose build + run

```yaml
version: '3'
services:
  myapp:
    build:
      context: ./path/to/your/app
      dockerfile: Dockerfile
    image: your-image-name:tag
```

This builds and starts the container in one step.

### Option 3 — GitHub Actions CI/CD

Automate builds and pushes to Docker Hub on every commit.

:::note
Recommended: read the [GitHub Actions docs](https://docs.github.com/en/actions) first.
:::

```yaml
name: Docker Build and Push
on:
  workflow_dispatch:
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout the repository
        uses: actions/checkout@v2

      - name: Login to Docker Hub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v1

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Build and push image
        uses: docker/build-push-action@v2
        with:
          context: .
          file: ./server/video/rpc/Dockerfile
          push: true
          tags: ${{ secrets.DOCKERHUB_IMAGE }}video-rpc:latest
          platforms: linux/amd64,linux/arm64

      - name: Deploy via SSH
        uses: appleboy/ssh-action@v0.1.10
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          password: ${{ secrets.PASSWORD }}
          port: ${{ secrets.PORT }}
          script: |
            cd /home/project/myapp
            docker-compose -f docker-compose.yaml stop video-rpc
            docker-compose -f docker-compose.yaml rm -f video-rpc
            docker image rm ${{ secrets.DOCKERHUB_IMAGE }}video-rpc:latest
            docker-compose -f docker-compose.yaml up -d video-rpc
```

#### Getting a Docker Hub access token

1. Log in to [Docker Hub](https://hub.docker.com/settings/security) and generate an access token.
2. Copy and save the token — it is only shown once.
3. Add it as a GitHub repository secret (`DOCKERHUB_TOKEN`).

![Docker Hub token](/resource/tutorials/ops/docker-deployment-2.png)

#### Adding GitHub Secrets

Go to **Settings → Secrets and variables → Actions** in your GitHub repository and add:

- `DOCKER_USERNAME` — your Docker Hub username
- `DOCKERHUB_TOKEN` — the token from the step above
- `HOST`, `USERNAME`, `PASSWORD`, `PORT` — your deployment server credentials

![GitHub Secrets](/resource/tutorials/ops/docker-deployment-3.png)
