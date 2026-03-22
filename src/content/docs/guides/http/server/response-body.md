---
title: Response Body
description: Write response bodies in go-zero HTTP handlers.
sidebar:
  order: 6

---


## Overview

In go-zero, `http.ResponseWriter`'s `Write` method returns the response body and the `Header` method sets response headers. For additional response formats (e.g. XML), see the [zeromicro/x](https://github.com/zeromicro/x) extension package — `https://github.com/zeromicro/x/blob/main/http/responses.go`.

## Sample

### Json Response Parameters

```go
type Response struct {
    Name   string `json:"name"`
    Age    int    `json:"age"`
}

resp := &Response{Name: "jack", Age: 18}
httpx.OkJson(w, resp)
```
