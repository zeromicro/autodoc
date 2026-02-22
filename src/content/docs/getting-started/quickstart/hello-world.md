---
title: Hello World
description: Build and run your first go-zero API service.
sidebar:
  order: 8
---

# Hello World

## Prerequisites

- [x] Go installed
- [x] goctl installed

## Step 1: Create Project

```bash
goctl api new greet
cd greet
go mod tidy
```

## Step 2: Run Service

```bash
go run greet.go
```

## Step 3: Verify

```bash
curl http://localhost:8888/from/you
```

Expected response:

```json
{"message":"Hello you"}
```
