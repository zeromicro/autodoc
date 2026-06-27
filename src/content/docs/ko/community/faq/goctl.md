---
title: goctl FAQ
description: goctl 코드 생성에 대해 자주 묻는 질문입니다.
sidebar:
  order: 6

---


## 다시 생성할 때 사용자 로직이 덮어써지지 않게 하려면?

goctl은 아직 존재하지 않는 **stub** 로직 파일만 생성합니다. `internal/logic/` 아래의 기존 파일은 절대 덮어쓰지 않습니다. 기존 프로젝트에서 `goctl api go`를 다시 실행해도 안전하며, 누락된 파일만 새로 만들어집니다.

## 파일 이름 스타일을 바꾸려면?

`--style` 플래그를 사용합니다.

```bash
goctl api go -api user.api -dir . --style go_zero
# 생성 예: user_handler.go, create_user_logic.go 등
```

옵션은 `gozero`(기본값), `go_zero`, `goZero`입니다.

## 요청 검증을 추가하려면?

go-zero에는 내장 validator가 없습니다. `go-playground/validator`를 사용하세요.

```go
import "github.com/go-playground/validator/v10"

var validate = validator.New()

func (l *CreateUserLogic) CreateUser(req *types.CreateUserReq) (*types.CreateUserResp, error) {
    if err := validate.Struct(req); err != nil {
        return nil, errorx.NewCodeError(400, err.Error())
    }
    // ...
}
```

## 사용자 정의 오류 코드를 반환하려면?

오류 패키지를 정의합니다.

```go
package errorx

type CodeError struct {
    Code int    `json:"code"`
    Msg  string `json:"msg"`
}

func (e *CodeError) Error() string { return e.Msg }
func NewCodeError(code int, msg string) *CodeError {
    return &CodeError{Code: code, Msg: msg}
}
```

그다음 `main.go`에서 사용자 정의 오류 핸들러를 등록합니다.

```go
httpx.SetErrorHandler(func(err error) (int, any) {
    var ce *errorx.CodeError
    if errors.As(err, &ce) {
        return http.StatusOK, ce
    }
    return http.StatusInternalServerError, nil
})
```

## 하나의 저장소에서 여러 서비스를 생성하려면?

각 서비스 디렉터리에서 해당 서비스의 `.api` 또는 `.proto` 파일을 사용해 goctl을 실행합니다.

```bash
cd services/user && goctl api go -api user.api -dir .
cd services/order && goctl api go -api order.api -dir .
```
