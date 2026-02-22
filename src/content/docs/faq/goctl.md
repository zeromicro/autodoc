---
title: goctl FAQ
description: Common questions about goctl code generation.
sidebar:
  order: 3
---

# goctl FAQ

## How do I add custom logic without it being overwritten on re-generation?

goctl only generates **stub** logic files if they don't already exist. It never overwrites files in `internal/logic/`. Re-running `goctl api go` on an existing project is safe — only missing files are created.

## How do I change the file naming style?

Use the `--style` flag:

```bash
goctl api go -api user.api -dir . --style go_zero
# produces: user_handler.go, create_user_logic.go, etc.
```

Options: `gozero` (default), `go_zero`, `goZero`.

## How to add request validation?

go-zero does not include a built-in validator. Use `go-playground/validator`:

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

## How to return custom error codes?

Define an error package:

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

Then register a custom error handler in `main.go`:

```go
httpx.SetErrorHandler(func(err error) (int, any) {
    var ce *errorx.CodeError
    if errors.As(err, &ce) {
        return http.StatusOK, ce
    }
    return http.StatusInternalServerError, nil
})
```

## How to generate multiple services from one repo?

Run goctl from each service directory, each with its own `.api` or `.proto` file:

```bash
cd services/user && goctl api go -api user.api -dir .
cd services/order && goctl api go -api order.api -dir .
```
