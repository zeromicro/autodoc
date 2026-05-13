---
title: HTTP 클라이언트
description: go-zero 서비스에서 HTTP 호출을 수행하는 방법입니다.
sidebar:
  order: 4

---


## 개요

HTTP Client는 HTTP 요청을 보내기 위한 라이브러리이며 다음 기능을 지원합니다.

1. `Content-Type` 자동 인식(`application/json`, `application/x-www-form-urlencoded` 지원)
2. URL path argument 자동 채우기
3. 구조체 field를 HTTP request header로 채우기

## 요청 예제

### GET, POST form 요청

GET form 요청과 POST form 요청은 같은 방식으로 사용합니다. 구조체 field에 `form` tag만 지정하면 됩니다.

```go
type Request struct {
    Node   string `path:"node"`
    ID     int    `form:"id"`
    Header string `header:"X-Header"`
}

var domain = flag.String("domain", "http://localhost:3333", "the domain to request")

func main() {
    flag.Parse()

    req := types.Request{
        Node:   "foo",
        ID:     1024,
        Header: "foo-header",
    }
    resp, err := httpc.Do(context.Background(), http.MethodGet, *domain+"/nodes/:node", req)
    // resp, err := httpc.Do(context.Background(), http.MethodPost, *domain+"/nodes/:node", req)
    if err != nil {
        fmt.Println(err)
        return
    }

    io.Copy(os.Stdout, resp.Body)
}
```

위 코드는 다음 curl과 같습니다.

```bash
# get
curl --location 'http://localhost:3333/nodes/foo?id=1024' \
--header 'X-Header: foo-header'

# post
curl --location 'http://localhost:3333/nodes/foo' \
--header 'X-Header: foo-header' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'id=1024'
```

### POST JSON 요청

POST JSON 요청도 같은 방식으로 사용합니다. 구조체 field에 `json` tag를 지정하면 됩니다.

```go
type Request struct {
    Node   string `path:"node"`
    Foo    string `json:"foo"`
    Bar    string `json:"bar"`
    Header string `header:"X-Header"`
}

var domain = flag.String("domain", "http://localhost:3333", "the domain to request")

func main() {
    flag.Parse()

    req := types.Request{
        Node:   "foo",
        Header: "foo-header",
        Foo:    "foo",
        Bar:    "bar",
    }
    resp, err := httpc.Do(context.Background(), http.MethodPost, *domain+"/nodes/:node", req)
    if err != nil {
        fmt.Println(err)
        return
    }

    io.Copy(os.Stdout, resp.Body)
}
```

위 요청은 다음 curl과 같습니다.

```bash
curl --location 'http://localhost:3333/nodes/foo' \
--header 'X-Header: foo-header' \
--header 'Content-Type: application/json' \
--data '{
    "foo":"foo",
    "bar":"bar"
}'
```

:::tip hint
`httpc`는 `http.DefaultClient`를 사용하며, 이 client는 별도로 지정할 수 없습니다.
:::
