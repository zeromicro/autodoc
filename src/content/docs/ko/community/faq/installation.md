---
title: 설치 FAQ
description: go-zero 설치와 초기 설정에서 자주 발생하는 문제입니다.
sidebar:
  order: 2

---


## 설치 후 `goctl: command not found`가 표시됩니다

`$GOPATH/bin`이 `PATH`에 포함되어 있는지 확인하세요.

```bash
export PATH=$PATH:$(go env GOPATH)/bin
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.zshrc
```

## `go mod tidy` 중 `go: module ... not found`가 발생합니다

Go 1.18 이상을 사용하고 유효한 `go.mod`가 있는지 확인하세요.

```bash
go version          # 1.18 이상이어야 합니다
go env GOPROXY      # https://goproxy.cn 또는 https://proxy.golang.org가 포함되어야 합니다
```

회사 방화벽 뒤에 있다면 프록시를 설정하세요.

```bash
go env -w GOPROXY=https://goproxy.cn,direct
```

## goctl rpc 실행 시 `protoc-gen-go: program not found`가 발생합니다

필요한 protoc 플러그인을 설치하세요.

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

또는 goctl 내장 설치기를 사용합니다.

```bash
goctl env check --install
```

## 생성된 코드에 import 오류가 있습니다

생성된 디렉터리 안에서 `go mod tidy`를 실행하세요. 또한 `.proto`의 `go_package`가 실제 생성 디렉터리 경로와 일치하는지 확인하세요.

## IDE에서 생성된 파일에 오류가 표시됩니다

IDE의 Go module root가 올바르게 설정되어 있는지 확인하세요. VS Code에서는 `go.mod`가 있는 프로젝트 루트를 workspace로 여세요.
