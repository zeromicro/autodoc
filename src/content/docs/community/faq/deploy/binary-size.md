---
title: Reducing Binary Size
description: Tips to reduce the Go binary size for production deployments.
---


## How to reduce the size of go-zero compiled binary files?

If you are not using `Kubernetes` for service discovery, you can exclude the `k8s` related dependency packages during compilation by using the `-tags no_k8s` flag.

The specific method is as follows:

```bash
GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -tags no_k8s demo.go
```

This can reduce the size by more than 20MB, as shown in the image below:



> go-zero version: >= v1.7.1