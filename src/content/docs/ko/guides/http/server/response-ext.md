---
title: 응답 확장
description: go-zero HTTP 서비스에서 확장 응답 helper를 사용하는 방법입니다.
sidebar:
  order: 7

---

## 개요

go-zero는 강력한 HTTP 기능을 제공하지만, 모든 응답 형식을 프레임워크 본체에서 직접 제공하지는 않습니다. go-zero용 확장 패키지인 `github.com/zeromicro/x`는 다음과 같은 HTTP 응답 확장 기능을 제공합니다.

1. `code-data` 응답 형식 지원
2. XML 응답 지원
3. `code-msg` 오류 타입 지원

자세한 내용은 https://github.com/zeromicro/x 를 참고하세요.

### `code-data` 통합 응답 형식 사용

프런트엔드와 응답 형식을 통일하기 위해, 많은 프로젝트에서는 업무 코드, 메시지, 업무 데이터를 다음과 같은 공통 형식으로 한 번 감쌉니다.

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    ...
  }
}
```

이런 응답 형식이 필요하다면 보통 두 가지 방법을 사용할 수 있습니다.

1. 응답 형식을 직접 구현합니다.
2. go-zero 확장 패키지를 사용합니다.

아래에서는 go-zero 확장 패키지를 사용하는 방법을 보여 줍니다.

1. demo 프로젝트를 초기화합니다.

```shell
$ mkdir demo && cd demo
$ go mod init demo
```

2. demo 디렉터리에 `user.api` API 파일을 만들고 다음 내용을 추가합니다.

```go
syntax = "v1"

type LoginRequest {
    Username string `json:"username"`
    Password string `json:"password"`
}

type LoginResponse {
    UID int64 `json:"uid"`
    Name string `json:"name"`
}

service user {
    @handler login
    post /user/login (LoginRequest) returns (LoginResponse)
}
```

3. goctl로 코드를 생성합니다.

```shell
$ goctl api go --api user.api --dir .
Done.
```

4. 로그인 mock 로직을 추가합니다. `demo/internal/logic/loginlogic.go` 파일을 다음처럼 수정합니다.

```go
package logic

import (
    "context"

    "demo/internal/svc"
    "demo/internal/types"

    "github.com/zeromicro/go-zero/core/logx"
    "github.com/zeromicro/x/errors"
)

type LoginLogic struct {
    logx.Logger
    ctx    context.Context
    svcCtx *svc.ServiceContext
}

func NewLoginLogic(ctx context.Context, svcCtx *svc.ServiceContext) *LoginLogic {
    return &LoginLogic{
        Logger: logx.WithContext(ctx),
        ctx:    ctx,
        svcCtx: svcCtx,
    }
}

func (l *LoginLogic) Login(req *types.LoginRequest) (resp *types.LoginResponse, err error) {
    // mock login
    if req.Username != "go-zero" || req.Password != "123456" {
        return nil, errors.New(1001, "invalid username or password")
    }

    resp = new(types.LoginResponse)
    resp.Name = "go-zero"
    resp.UID = 1
    return resp, nil
}
```

먼저 `demo/internal/handler/loginhandler.go`를 수정하기 전의 응답 형식을 확인해 보겠습니다.

```shell
$ cd demo
$ go mod tidy
$ go run user.go
# 성공 응답
curl --location '127.0.0.1:8888/user/login' \
--header 'Content-Type: application/json' \
--data '{
    "username":"go-zero",
    "password":"123456"
}'
{"uid":1,"name":"go-zero"}

# 오류 응답
curl --location '127.0.0.1:8888/user/login' \
--header 'Content-Type: application/json' \
--data '{
    "username":"go-zero",
    "password":"111111"
}'
code: 1001, msg: invalid username or password
```

5. 이제 `demo/internal/handler/loginhandler.go` 파일을 수정해 `loginHandler`의 응답 처리 방식을 확장 패키지의 메서드로 교체합니다.

:::tip
이 단계는 template을 수정해 자동화할 수 있습니다. 그러면 코드를 다시 생성할 때마다 같은 수정을 반복하지 않아도 됩니다. 자세한 내용은 [템플릿 커스터마이징](../../../reference/customization/template.md)을 참고하세요.
:::

```go
package handler

import (
    "net/http"

    "demo/internal/logic"
    "demo/internal/svc"
    "demo/internal/types"
    "github.com/zeromicro/go-zero/rest/httpx"
    xhttp "github.com/zeromicro/x/http"
)

func loginHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        var req types.LoginRequest
        if err := httpx.Parse(r, &req); err != nil {
            httpx.ErrorCtx(r.Context(), w, err)
            return
        }

        l := logic.NewLoginLogic(r.Context(), svcCtx)
        resp, err := l.Login(&req)
        if err != nil {
            // code-data response
            xhttp.JsonBaseResponseCtx(r.Context(), w, err)
        } else {
            // code-data response
            xhttp.JsonBaseResponseCtx(r.Context(), w, resp)
        }
    }
}
```

user 서비스를 다시 시작하고 응답 형식을 확인합니다.

```shell
$ go run user.go
# 오류가 없는 경우
curl --location '127.0.0.1:8888/user/login' \
--header 'Content-Type: application/json' \
--data '{
    "username":"go-zero",
    "password":"123456"
}'
{"code":0,"msg":"ok","data":{"uid":1,"name":"go-zero"}}

# 오류가 있는 경우
curl --location '127.0.0.1:8888/user/login' \
--header 'Content-Type: application/json' \
--data '{
    "username":"go-zero",
    "password":"111111"
}'
{"code":1001,"msg":"invalid username or password"}
```

### XML 응답 지원

위 예제에서 이어서 `demo/internal/handler/loginhandler.go`의 응답 메서드를 XML 응답 helper로 바꿀 수 있습니다. 일반 XML 응답이 필요하면 `xhttp.OkXml` 또는 `xhttp.OkXmlCtx`를 사용할 수 있고, 같은 `code-data` 형식의 XML 응답이 필요하면 `xhttp.XmlBaseResponse` 또는 `xhttp.XmlBaseResponseCtx`를 사용합니다. 아래 예제에서는 `xhttp.XmlBaseResponseCtx`를 사용합니다.

```go
package handler

import (
    "net/http"

    "demo/internal/logic"
    "demo/internal/svc"
    "demo/internal/types"
    "github.com/zeromicro/go-zero/rest/httpx"
    xhttp "github.com/zeromicro/x/http"
)

func loginHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        var req types.LoginRequest
        if err := httpx.Parse(r, &req); err != nil {
            httpx.ErrorCtx(r.Context(), w, err)
            return
        }

        l := logic.NewLoginLogic(r.Context(), svcCtx)
        resp, err := l.Login(&req)
        if err != nil {
            //xhttp.XmlBaseResponse(w,err)
            xhttp.XmlBaseResponseCtx(r.Context(),w,err)
        } else {
            //xhttp.XmlBaseResponse(w,resp)
            xhttp.XmlBaseResponseCtx(r.Context(),w,resp)
        }
    }
}

```

user 프로그램을 다시 실행해 XML 응답 형식을 확인합니다.

```shell
$ go run user.go
# 오류가 없는 경우
curl --location '127.0.0.1:8888/user/login' \
--header 'Content-Type: application/json' \
--data '{
    "username":"go-zero",
    "password":"123456"
}'
<xml version="1.0" encoding="UTF-8"><code>0</code><msg>ok</msg><data><UID>1</UID><Name>go-zero</Name></data></xml>

# 오류가 있는 경우
curl --location '127.0.0.1:8888/user/login' \
--header 'Content-Type: application/json' \
--data '{
    "username":"go-zero",
    "password":"111111"
}'
<xml version="1.0" encoding="UTF-8"><code>1001</code><msg>invalid username or password</msg></xml>
```

## 참고 자료

- [goctl 코드 생성 도구](../../../reference/cli-guide/index.md)
- https://github.com/zeromicro/x
- [템플릿 커스터마이징](../../../reference/customization/template.md)
