---
title: Project Creation Methods
description: Common ways to bootstrap go-zero projects.
sidebar:
  order: 11
---

# Project Creation Methods

## From Scratch

- `goctl api new <name>`
- `goctl rpc new <name>`

## From Existing DSL

- `goctl api go -api <file>.api -dir .`
- `goctl rpc protoc <file>.proto --go_out=. --go-grpc_out=. --zrpc_out=.`

## From Team Templates

Use custom templates to enforce organization-level conventions and project standards.
