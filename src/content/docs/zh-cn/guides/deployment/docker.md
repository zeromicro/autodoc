---
title: Docker 部署
description: 将 go-zero 服务打包并运行在 Docker 中。
sidebar:
  order: 15
---

# Docker 部署

```bash
docker build -t greet:latest .
docker run -p 8888:8888 greet:latest
```
