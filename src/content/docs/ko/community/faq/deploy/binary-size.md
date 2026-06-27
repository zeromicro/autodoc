---
title: 바이너리 크기 줄이기
description: 프로덕션 배포용 Go 바이너리 크기를 줄이는 방법입니다.
sidebar:
  order: 2
---


## 컴파일된 go-zero 바이너리 크기를 줄이는 방법은?

서비스 디스커버리에 `Kubernetes`를 사용하지 않는다면, 컴파일할 때 `-tags no_k8s` 플래그를 사용해 `k8s` 관련 의존성 패키지를 제외할 수 있습니다.

구체적인 방법은 다음과 같습니다.

```bash
GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -tags no_k8s demo.go
```

이렇게 빌드하면 아래 이미지처럼 바이너리 크기를 20MB 이상 줄일 수 있습니다.



> go-zero 버전: >= v1.7.1
