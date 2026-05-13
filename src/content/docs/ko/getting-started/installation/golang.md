---
title: Go 설치
description: go-zero 개발에 필요한 Go 런타임을 설치하고 확인합니다.
sidebar:
  order: 2
---


go-zero는 **Go 1.21 이상**이 필요합니다. 이 문서는 macOS, Linux, Windows에서 Go를 설치하고 환경을 확인하는 방법을 설명합니다.

## 기존 설치 확인

```bash
go version
# go version go1.23.4 linux/amd64
```

버전이 1.21 이상이면 [환경 확인](#환경-확인)으로 이동하세요. 그렇지 않으면 아래 절차로 설치하거나 업그레이드합니다.

## 설치

### macOS

```bash
# Homebrew 사용(권장)
brew install go

# 또는 다음 페이지에서 .pkg 설치 파일 다운로드
# https://go.dev/dl/
```

### Linux

```bash
# 다운로드 후 압축 해제(1.23.4는 최신 버전으로 바꾸세요)
wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz
```

셸 프로필(`~/.bashrc`, `~/.zshrc` 등)에 Go 경로를 추가합니다.

```bash
export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go
export GOBIN=$GOPATH/bin
export PATH=$PATH:$GOBIN
```

셸 설정을 다시 로드합니다.

```bash
source ~/.zshrc   # 또는 ~/.bashrc
```

### Windows

[go.dev/dl](https://go.dev/dl/)에서 `.msi` 설치 파일을 내려받아 실행합니다. 설치 프로그램이 `PATH`를 자동으로 업데이트합니다.

## 환경 확인

```bash
go version
# go version go1.23.4 ...

go env GOPATH GOBIN GOMODCACHE
# /home/user/go
# /home/user/go/bin
# /home/user/go/pkg/mod
```

`GOBIN`이 `PATH`에 포함되어 있는지 확인하세요. `goctl`과 Go로 설치한 다른 바이너리가 이 위치에 놓입니다.

## 문제 해결

| 문제 | 해결 방법 |
|---|---|
| `go: command not found` | `/usr/local/go/bin`을 `PATH`에 추가하고 셸을 다시 로드합니다. |
| 설치 후 `goctl: command not found` | `$GOBIN`을 `PATH`에 추가합니다. |
| 모듈 다운로드 오류 | `go env -w GOPROXY=https://goproxy.cn,direct` 실행(중국 환경) |

## 다음 단계

[goctl 설치 →](../goctl)
