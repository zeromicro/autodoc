---
title: goctl 常见问题
description: goctl 代码生成的常见问题与解答。
sidebar:
  order: 6

---

## 如何添加自定义逻辑而不被重新生成覆盖？

goctl 只在 logic 文件**不存在**时才生成桩代码，永远不会覆盖 `internal/logic/` 中的已有文件。对已有项目重新运行 `goctl api go` 是安全的——只会创建缺失的文件。

## 如何更改文件命名风格？

使用 `--style` 参数：

```bash
goctl api go -api user.api -dir . --style go_zero
# 生成：user_handler.go, create_user_logic.go 等
```

可选值：`gozero`（默认）、`go_zero`、`goZero`。

## 如何添加请求校验？

go-zero 不包含内建校验器。可以使用 `go-playground/validator`：

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

## 如何返回自定义错误码？

定义一个错误包：

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

然后在 `main.go` 中注册自定义错误处理器：

```go
httpx.SetErrorHandler(func(err error) (int, any) {
    var ce *errorx.CodeError
    if errors.As(err, &ce) {
        return http.StatusOK, ce
    }
    return http.StatusInternalServerError, nil
})
```

## 如何从一个仓库生成多个服务？

在每个服务目录中分别运行 goctl，各自使用独立的 `.api` 或 `.proto` 文件：

```bash
cd services/user && goctl api go -api user.api -dir .
cd services/order && goctl api go -api order.api -dir .
```
