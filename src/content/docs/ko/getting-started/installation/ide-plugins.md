---
title: IDE 플러그인
description: Go, Proto, 생산성을 위한 권장 IDE 확장입니다.
sidebar:
  order: 5
---


올바른 IDE 설정은 `.api` 파일 자동 완성, 인라인 오류 표시, 한 번의 클릭으로 실행하는 코드 생성을 제공합니다.

## VS Code

다음 확장을 설치합니다. Extensions 패널에서 검색하거나 링크를 클릭하세요.

| 확장 | 목적 |
|---|---|
| [Go](https://marketplace.visualstudio.com/items?itemName=golang.Go) | 언어 서버, 디버깅, 테스트 러너 |
| [goctl](https://marketplace.visualstudio.com/items?itemName=zeromicro.goctl-vscode) | `.api` 파일 구문 강조와 스니펫 |
| [vscode-proto3](https://marketplace.visualstudio.com/items?itemName=zxh404.vscode-proto3) | `.proto` 파일 구문 강조 |
| [Error Lens](https://marketplace.visualstudio.com/items?itemName=usernamehw.errorlens) | 인라인 오류 메시지 |

Go 확장을 설치한 뒤 아무 `.go` 파일이나 열면 VS Code가 `gopls`, `dlv`와 기타 도구 설치를 안내합니다. 모든 프롬프트를 승인하세요.

### gopls 실행 확인

`.go` 파일을 열고 함수 이름 위에 마우스를 올립니다. 문서 팝업이 보이면 정상입니다. 보이지 않으면 다음 명령을 실행합니다.

```
Ctrl+Shift+P → Go: Install/Update Tools → select all → OK
```

## GoLand / IntelliJ IDEA

| 플러그인 | 목적 |
|---|---|
| Go (GoLand 내장) | 완전한 Go 지원 |
| [Protocol Buffers](https://plugins.jetbrains.com/plugin/14004-protocol-buffers) | `.proto` 구문과 탐색 |
| [goctl plugin](https://plugins.jetbrains.com/plugin/15414-goctl) | `.api` 파일 구문 강조 |

GoLand에서는 **Settings → Go → GOROOT**가 Go 설치 경로를 가리키는지 확인하세요.

## Neovim

`gopls`와 함께 [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig)를 사용합니다.

```lua
require('lspconfig').gopls.setup{}
```

`gopls`를 설치합니다.

```bash
go install golang.org/x/tools/gopls@latest
```

## 다음 단계

[API DSL 문법 이해하기 →](../../../reference/api-dsl)
