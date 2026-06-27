---
title: 코드 스타일
description: go-zero 기여자를 위한 코딩 관례와 스타일 가이드입니다.
sidebar:
  order: 2

---


go-zero는 표준 Go 관례를 따르며, 몇 가지 추가 가이드라인을 적용합니다.

## 포맷팅

모든 코드는 `gofmt` / `goimports`로 포맷해야 합니다.

```bash
goimports -w ./...
```

포맷 문제가 있으면 CI에서 PR이 거부됩니다.

## 명명

| 요소 | 관례 | 예시 |
|---------|-----------|---------|
| 패키지 | 짧고 소문자로 작성하며 밑줄을 쓰지 않음 | `logx`, `httpx` |
| 인터페이스 | 설명적인 명사 또는 `-er` 접미사 | `UserModel`, `Breaker` |
| 생성자 | `NewXxx` 또는 `MustNewXxx` | `NewCache`, `MustNewServer` |
| 오류 변수 | `ErrXxx` | `ErrNotFound`, `ErrTimeout` |
| 설정 구조체 | 표준 기반 설정을 임베드 | `RestConf`, `RpcServerConf` |

## 오류 처리

- 오류를 조용히 무시하지 마세요.
- `fmt.Errorf("createUser: %w", err)`처럼 컨텍스트를 포함해 오류를 감싸세요.
- 타입 단언이 필요한 경우 패키지 수준에 정의된 sentinel error를 사용하세요.

## 테스트

- 단위 테스트는 소스와 같은 패키지에 `foo_test.go` 형태로 둡니다.
- table-driven test를 권장합니다.
- mock은 `mockgen`으로 생성하거나 필요한 최소 스텁을 직접 작성합니다.
- 새 패키지는 **80%** 이상의 커버리지를 목표로 합니다.

```bash
go test -race -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## 주석

- export되는 모든 심볼에는 문서 주석이 있어야 합니다.
- 주석은 완전한 문장으로 쓰고 심볼 이름으로 시작합니다.
- 의도가 분명하지 않은 로직에는 “왜” 그런지 설명하는 인라인 주석을 추가합니다.
