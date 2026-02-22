---
title: Install protoc
description: Install Protocol Buffers compiler for RPC code generation.
sidebar:
  order: 4
---

# Install protoc

RPC services in go-zero use protobuf. You need three components:

1. `protoc` — the protobuf compiler
2. `protoc-gen-go` — generates Go types from `.proto` files
3. `protoc-gen-go-grpc` — generates gRPC service stubs

goctl can install the last two for you automatically.

## Install protoc

### macOS

```bash
brew install protobuf
```

### Linux

```bash
# Find the latest release at https://github.com/protocolbuffers/protobuf/releases
PB_VERSION=27.2
wget https://github.com/protocolbuffers/protobuf/releases/download/v${PB_VERSION}/protoc-${PB_VERSION}-linux-x86_64.zip
unzip protoc-${PB_VERSION}-linux-x86_64.zip -d $HOME/.local
export PATH=$PATH:$HOME/.local/bin
```

### Windows

Download `protoc-*.zip` from the [releases page](https://github.com/protocolbuffers/protobuf/releases) and add the `bin/` folder to `PATH`.

## Install Go plugins via goctl

goctl automates installing `protoc-gen-go` and `protoc-gen-go-grpc`:

```bash
goctl env check --install --verbose
```

Expected output:

```
[goctl-env]: preparing ...
[goctl-env]: go out ...
[goctl-env]: grpc out ...
[goctl-env]: Done.
```

## Verify Everything

```bash
protoc --version
# libprotoc 27.2

protoc-gen-go --version
# protoc-gen-go v1.34.2

protoc-gen-go-grpc --version
# protoc-gen-go-grpc 1.4.0
```

## Next Step

[Configure your IDE →](./ide-plugins)
