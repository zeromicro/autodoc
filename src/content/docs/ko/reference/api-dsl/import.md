---
title: API Import
description: go-zero의 API Import에 대해 설명합니다.
sidebar:
  order: 10

---

## 개요


## api 파일 import


```json
{
"code": 0,
"msg": "success",
"data": {}
}
```


**base.api**
```go
syntax =  "v1"

type Base {
    Code int    `json:"code"`
    Msg  string `json:"msg"`
}
```

**user.api**
```go {4}
syntax = "v1"

// 가져오기
import "base.api"

type UserInfoReq {
    Id int64 `path:"id"`
}

type UserInfo {
    Id   int64  `path:"id"`
    Name string `json:"name"`
    Age  int    `json:"age"`
}

type UserInfoResp {
    Base // Base API 포함
    Data UserInfo `json:"data"`
}

type UserInfoUpdateReq {
    Id int64 `json:"id"`
    UserInfo
}

type UserInfoUpdateResp {
    Base
}

service user {
    @handler userInfo
    get /user/info/:id (UserInfoReq) returns (UserInfoResp)

    @handler userInfoUpdate
    post /user/info/update (UserInfoUpdateReq) returns (UserInfoUpdateResp)
}

```

:::note 튜토리얼


이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.
