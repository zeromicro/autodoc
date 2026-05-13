---
title: 응답 본문
description: go-zero HTTP handler에서 응답 본문을 작성하는 방법입니다.
sidebar:
  order: 6

---

## 개요

go-zero에서 응답 본문은 `http.ResponseWriter`의 `Write` 메서드로 작성하고, 응답 header는 `Header` 메서드로 설정합니다. XML 같은 추가 응답 형식이 필요하다면 [zeromicro/x](https://github.com/zeromicro/x) 확장 패키지의 `https://github.com/zeromicro/x/blob/main/http/responses.go`를 참고하세요.

## 예제

### JSON 응답 매개변수

```go
type Response struct {
    Name   string `json:"name"`
    Age    int    `json:"age"`
}

resp := &Response{Name: "jack", Age: 18}
httpx.OkJson(w, resp)
```
