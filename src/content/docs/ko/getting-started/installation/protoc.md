---
title: protoc 설치
description: RPC 코드 생성에 필요한 Protocol Buffers 컴파일러를 설치합니다.
sidebar:
  order: 4
---


go-zero의 RPC 서비스는 protobuf를 사용합니다. 다음 세 가지 컴포넌트가 필요합니다.

1. `protoc` — protobuf 컴파일러
2. `protoc-gen-go` — `.proto` 파일에서 Go 타입 생성
3. `protoc-gen-go-grpc` — gRPC 서비스 스텁 생성

goctl은 마지막 두 항목을 자동으로 설치할 수 있습니다.

## protoc 설치

### macOS

```bash
brew install protobuf
```

### Linux

```bash
# 최신 릴리스는 https://github.com/protocolbuffers/protobuf/releases 에서 확인하세요
PB_VERSION=27.2
wget https://github.com/protocolbuffers/protobuf/releases/download/v${PB_VERSION}/protoc-${PB_VERSION}-linux-x86_64.zip
unzip protoc-${PB_VERSION}-linux-x86_64.zip -d $HOME/.local
export PATH=$PATH:$HOME/.local/bin
```

### Windows

[releases page](https://github.com/protocolbuffers/protobuf/releases)에서 `protoc-*.zip`을 내려받고 `bin/` 폴더를 `PATH`에 추가합니다.

## goctl로 Go 플러그인 설치

goctl은 `protoc-gen-go`와 `protoc-gen-go-grpc` 설치를 자동화합니다.

```bash
goctl env check --install --verbose
```

예상 출력:

```
[goctl-env]: preparing ...
[goctl-env]: go out ...
[goctl-env]: grpc out ...
[goctl-env]: Done.
```

## 전체 확인

```bash
protoc --version
# libprotoc 27.2

protoc-gen-go --version
# protoc-gen-go v1.34.2

protoc-gen-go-grpc --version
# protoc-gen-go-grpc 1.4.0
```

## 다음 단계

[IDE 설정 →](../ide-plugins)
