---
title: goctl Swagger
description: goctl로 Swagger/OpenAPI 문서를 생성하는 방법을 설명합니다.
sidebar:
  order: 13

---

API 파일에서 Swagger 문서를 생성합니다. 출력 형식은 JSON과 YAML을 모두 지원합니다.

:::note 참고
이 기능은 goctl 1.8.2보다 높은 버전이 필요합니다.
:::

## 명령

```bash
goctl api swagger -h
Generate swagger file from api

Usage:
  goctl api swagger [flags]

Flags:
      --api string   API file
      --dir string   Output directory
  -h, --help         Help for swagger
      --yaml         Generate YAML format
```

## 기능

### 기본 정보 설정

`info` 섹션에서 `title`, `description`, `version` 등을 사용해 Swagger의 기본 정보를 설명할 수 있습니다.

```go
info (
    title: "Demo API"                        // Swagger의 title에 대응합니다
    description: "Demo API generates Swagger..."  // Swagger의 description에 대응합니다
    version: "v1"                            // Swagger의 version에 대응합니다
)
```

![swagger info](/resource/tutorials/cli/info_basic.png)

### 이용 약관과 연락처 정보

`info` 섹션에서 `termsOfService`, `contactName`, `contactURL`, `contactEmail` 등을 사용해 이용 약관과 연락처 정보를 설명할 수 있습니다.

```go
info (
    termsOfService: "https://github.com/zeromicro/go-zero"  // API 이용 약관 URL
    contactName: "keson.an"                                // 기술 지원 담당자 이름
    contactURL: "https://github.com/zeromicro/go-zero"     // 연락처 관련 링크
    contactEmail: "example@gmail.com"                      // 연락처 이메일
)
```

### 라이선스 정보

`info` 섹션에서 `licenseName`, `licenseURL` 등을 사용해 라이선스 정보를 설명할 수 있습니다.

```go
info (
    licenseName: "MIT"  // 라이선스 유형(예: MIT/Apache 2.0/GPL 등)
    licenseURL: "https://github.com/zeromicro/go-zero/blob/master/LICENSE"  // 라이선스 상세 URL
)
```

![swagger info](/resource/tutorials/cli/info_contact.png)

### 프로토콜과 호스트 설정

`info` 섹션에서 `schemes`, `host`, `basePath` 등을 사용해 프로토콜과 호스트를 설정할 수 있습니다.

```go
info (
    consumes: "application/json"  // 기본 요청 콘텐츠 타입, 여러 값은 쉼표로 구분할 수 있습니다
    produces: "application/json"  // 기본 응답 콘텐츠 타입, 여러 값은 쉼표로 구분할 수 있습니다
    schemes: "https"              // 지원 프로토콜(http/https/ws/wss), 여러 값을 설정할 수 있습니다
    host: "example.com"           // API 서비스 호스트 주소(프로토콜 제외)
    basePath: "/v1"               // API 기본 경로, 모든 엔드포인트에 이 접두사가 붙습니다
)
```

### 비즈니스 오류 코드 정의

전역과 인터페이스 수준의 비즈니스 오류 코드 정의를 지원합니다. 전제 조건은 `wrapCodeMsg`가 활성화되어 있어야 한다는 것입니다. 비즈니스 오류 코드 설명은 code-msg의 `code` 필드를 기준으로 생성됩니다.

```go
// 전역 오류 코드 설명 정의
info (
    wrapCodeMsg: "true"
    bizCodeEnumDescription: "1001-Not logged in<br>1002-No permission to operate"
)

// 인터페이스 수준 오류 코드 설명 정의
service Swagger {
 @doc (
  bizCodeEnumDescription: "1003-User does not exist<br>1004-Illegal operation" // 인터페이스 수준 비즈니스 오류 코드 열거 설명입니다. 전역 비즈니스 오류 코드를 덮어씁니다. JSON 형식이며 key는 비즈니스 오류 코드, value는 오류 코드 설명입니다. wrapCodeMsg가 true일 때만 적용됩니다.
 )
 @handler login
 post /user/login (UserLoginReq) returns (UserLoginResp)
}

// 인터페이스 수준 오류 코드 설명 정의
service Swagger {
 @doc (
  bizCodeEnumDescription: "1003-User does not exist<br>1004-Illegal operation" // 인터페이스 수준 비즈니스 오류 코드 열거 설명입니다. 전역 비즈니스 오류 코드를 덮어씁니다. JSON 형식이며 key는 비즈니스 오류 코드, value는 오류 코드 설명입니다. wrapCodeMsg가 true일 때만 적용됩니다.
 )
 @handler login
 post /user/login (UserLoginReq) returns (UserLoginResp)
}
```

![swagger info](/resource/tutorials/cli/biz_code.png)

### Code-Message 형식 생성

`info` 섹션에 `wrapCodeMsg: "true"`를 설정하면 모든 응답 본문이 code-message 형식으로 감싸집니다. 이 형식은 Swagger 생성에만 적용되며 필드 이름은 고정되어 변경할 수 없습니다. go-zero의 실제 응답 본문과는 관련이 없습니다.

```go
// Swagger 생성을 위한 code-message 형식 래핑 활성화
info (
    wrapCodeMsg: "true"
)
```

생성되는 code-message 형식 예시는 다음과 같습니다.

```json
{
  "code": 0,
  "msg": "OK",
  "data": {original response body}
}
```

![swagger info](/resource/tutorials/cli/code_msg.png)

### 사용자 정의 인증 타입

`securityDefinitionsFromJson`으로 여러 인증 방식을 정의하고, `@server`의 `authType` 필드로 그룹 아래의 모든 라우트에 사용할 인증 타입을 선언할 수 있습니다. API 인증 JSON 형식은 OpenAPI Specification 표준을 참고하세요: https://swagger.io/specification/v2/#security-definitions-object

```go
info (
    securityDefinitionsFromJson: `{"apiKey":{"type":"apiKey","name":"x-api-key","in":"header"},"petstore_auth":{"type":"oauth2","authorizationUrl":"http://swagger.io/api/oauth/dialog","flow":"implicit","scopes":{"write:pets":"modify pets in your account","read:pets":"read your pets"}}}`
)

@server (
    authType: apiKey // /user/info가 apiKey 인증 타입을 사용하여다고 선언합니다
)
service Swagger {
 @handler userInfo
 post /user/info (UserInfoReq) returns (UserInfoResp)
}
```

![swagger info](/resource/tutorials/cli/auth_type_definition.png)

![swagger info](/resource/tutorials/cli/auth_type_check.png)

### 태그 그룹화

`@server`의 `tags` 속성을 사용해 Swagger에서 라우트를 그룹화할 수 있습니다.

```go
@server (
    tags: "User Operations"
)
service Swagger {
 @handler login
 post /user/login (UserLoginReq) returns (UserLoginResp)
}

@server (
    tags: "User Operations"
)
service Swagger {
 @handler userInfo
 post /user/info (UserInfoReq) returns (UserInfoResp)
}
```

위 라우트 `/user/login`과 `/user/info`는 Swagger에서 `User Operations` 태그 아래에 그룹화됩니다.

![swagger info](/resource/tutorials/cli/tags.png)

### 응답 본문 예제 표시

구조체의 `example` 태그를 사용해 응답 본문 필드의 예제 값을 추가할 수 있습니다. `example` 태그는 JSON 요청 본문에도 사용할 수 있습니다.

```go
type UserInfoResp {
    Id int `json:"id,example=10"`
    Name string `json:"name,example=keson.an"`
}
```

![swagger info](/resource/tutorials/cli/example.png)

### 매개변수 제어

구조체는 go-zero 매개변수 태그를 지원합니다.

- range: 숫자 범위 제한입니다. 예: range=[1:10000]
- options: 열거 값 제한입니다. 예: options=golang|java|python
- default: 기본값입니다. 예: default=male
- optional: 선택 매개변수입니다.

```go
type DemoReq {
    Id int `json:"id,range=[1:10000],example=10"` // 유효 범위
    Language string `json:"language,options=golang|java|python|typescript|rust"` // 열거 값
    Gender string `json:"gender,default=male,options=male|female,example=male"` // 기본값
    Name string `json:"name,optional"` // 선택 항목
}
```

![swagger info](/resource/tutorials/cli/parameter.png)

### 복합 구조체 타입

다음과 같은 복잡한 중첩 구조체를 지원합니다.

- 기본 타입과 해당 배열, map
- 객체와 객체 포인터
- 여러 단계로 중첩된 구조체
- 배열의 배열, map의 map 같은 복합 조합

```go
type ComplexJsonLevel2 {}
type ComplexJsonLevel1 {
    Integer int `json:"integer,example=1"`
    Object ComplexJsonLevel2 `json:"object"`
    PointerObject *ComplexJsonLevel2 `json:"pointerObject"`
}

type ComplexJsonReq {
    ArrayArrayInteger [][]int `json:"arrayArrayInteger"`
    MapMapObject map[string]map[string]ComplexJsonLevel1 `json:"mapMapObject"`
    ArrayPointerObject []*ComplexJsonLevel1 `json:"arrayPointerObject"`
}
```

![swagger info](/resource/tutorials/cli/complex.png)

### 경로 매개변수

경로 매개변수는 URL 경로에 직접 포함되는 변수입니다. API 정의에서는 `path:"parameterName"` 태그로 선언합니다. Swagger를 생성할 때 경로 매개변수는 자동으로 `{$path}` 형식으로 변환됩니다.

```go
type UserInfoReq {
    Id int `path:"id"`  // 경로 매개변수 id 정의
}

type UserInfoResp {
    Id int `json:"id,example=10"`
    Name string `json:"name,example=keson.an"`
}

@server(
    prefix: /api
)
service Swagger {
    @handler userInfo
    get /user/info/:id (UserInfoReq) returns (UserInfoResp)  // URL에서 :id 사용
}
```

![swagger info](/resource/tutorials/cli/path_parameter.png)
