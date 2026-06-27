---
title: HTTP 서버 설정
description: go-zero HTTP 서버 설정 전체 참조입니다.
sidebar:
  order: 2

---

## 개요

HTTP 서버 설정은 주로 서버가 바인딩할 호스트, 포트, 인증서 같은 항목을 제어하는 데 사용합니다.

## 설정 설명

Go 구조체 정의는 다음과 같습니다.

```go
RestConf struct {
        service.ServiceConf
        Host     string `json:",default=0.0.0.0"`
        Port     int
        CertFile string `json:",optional"`
        KeyFile  string `json:",optional"`
        Verbose  bool   `json:",optional"`
        MaxConns int    `json:",default=10000"`
        MaxBytes int64  `json:",default=1048576"`
        // milliseconds
        Timeout      int64         `json:",default=3000"`
        CpuThreshold int64         `json:",default=900,range=[0:1000]"`
        Signature    SignatureConf `json:",optional"`
        Middlewares MiddlewaresConf
    }
```

HTTP 서버의 주요 설정 항목은 아래 표와 같습니다.

| 이름 | 데이터 타입 | 의미 | 기본값 | 필수 여부 |
|:---:|:---:|:---:|:---:|:---:|
| Host | string | 리스닝 주소 | 0.0.0.0 | 예 |
| Port | int | 리스닝 포트 | 없음 | 예 |
| CertFile | string | HTTPS 인증서 파일 | 없음 | 아니요 |
| KeyFile | string | HTTPS 개인 키 파일 | 없음 | 아니요 |
| Verbose | bool | 상세 로그 출력 여부 | 없음 | 아니요 |
| MaxConns | int | 동시 요청 수 | 10000 | 예 |
| MaxBytes | int64 | 최대 본문 크기 | 1048576 | 예 |
| Timeout | int64 | 제한 시간(ms) | 3000 | 예 |
| CpuThreshold | int64 | CPU 사용률 임계값. 기본값은 900(90%)이며 허용 범위는 0~1000입니다. | 900 | 예 |
| Signature | SignatureConf | 서명 설정 | 없음 | 아니요 |
| Middlewares | MiddlewaresConf | 미들웨어 활성화 설정 | 없음 | 아니요 |

`ServiceConfig` 공통 설정은 [기본 서비스 설정](../../../reference/configuration/service-config.md)을 참고하세요.
`MiddlewaresConf` 설정은 [미들웨어](./middleware.md)를 참고하세요.
