---
title: 지속적 프로파일링
description: go-zero의 Pyroscope 통합을 사용해 프로덕션에서 CPU와 메모리를 실시간으로 프로파일링합니다.
sidebar:
  order: 4
---

import { Aside } from '@astrojs/starlight/components';


마이크로서비스 아키텍처가 복잡해지고 트래픽이 증가할수록 성능 문제를 진단하기가 더 어려워집니다. 전통적인 `pprof` 프로파일링은 수동 트리거, 파일 다운로드, 수동 분석이 필요하므로 프로덕션 환경에서는 다루기 어렵습니다.

go-zero는 [Pyroscope](https://grafana.com/docs/pyroscope/)를 통한 네이티브 **지속적 프로파일링**을 지원합니다. 비즈니스 코드를 건드리지 않고도 성능 데이터를 실시간으로 수집할 수 있습니다.

**얻을 수 있는 것:**
- CPU 병목 위치 파악
- 비정상적인 CPU/메모리/goroutine 동작 추적
- 프로덕션의 hot function 분석
- 온콜 운영 비용 감소

<Aside type="tip">
**go-zero ≥ v1.8.4**가 필요합니다.
</Aside>

## 왜 지속적 프로파일링인가요?

| 전통적인 `pprof` | 지속적 프로파일링 |
|---------------------|---------------------|
| 수동 트리거 | 자동, 상시 수집 |
| 다운로드 후 오프라인 분석 | 브라우저에서 실시간 flame graph 확인 |
| 침투적 방식(코드 변경 필요) | 비즈니스 코드에 투명함 |
| 특정 시점의 스냅샷 | 시간 흐름에 따른 추세 분석 |

**사용 사례:**
- CPU가 갑자기 급증하지만 로컬에서 재현하기 어려운 경우
- 메모리 누수가 발생했지만 코드 경로를 찾기 어려운 경우
- 높은 QPS에서 병목이 어디인지 알고 싶은 경우
- 운영팀과 개발팀이 함께 성능 문제를 분석해야 하는 경우

## 1. 로컬에서 Pyroscope 시작

```bash
docker pull grafana/pyroscope
docker run -it -p 4040:4040 grafana/pyroscope
```

`http://localhost:4040`을 열어 flame graph와 시각화 데이터를 확인합니다.

프로덕션 배포 옵션은 [Pyroscope 시작하기 가이드](https://grafana.com/docs/pyroscope/latest/get-started/)를 참고하세요.

## 2. 샘플 서비스 생성

```bash
goctl quickstart -t mono
cd greet/api
```

## 3. 설정에서 프로파일링 활성화

`etc/greet.yaml`에 `Profiling` 섹션을 추가합니다.

```yaml
Name: ping
Host: localhost
Port: 8888
Log:
  Level: error
Profiling:
  ServerAddr: http://localhost:4040   # 필수: Pyroscope 서버 주소
  CpuThreshold: 0                     # 0 = 지속 수집(데모에 적합)
```

### 설정 매개변수

| 매개변수 | 기본값 | 설명 |
|-----------|---------|-------------|
| `CpuThreshold` | `700` | 트리거 임계값입니다(700 = CPU 70%). 지속적으로 수집하려면 `0`으로 설정합니다. |
| `UploadDuration` | `15s` | 프로파일을 전송하는 주기입니다. |
| `ProfilingDuration` | `2m` | 각 수집 윈도우의 지속 시간입니다. |
| `ProfileType` | 아래 참고 | 수집할 프로파일 종류입니다. |

```go
ProfileType struct {
    CPU        bool `json:",default=true"`
    Memory     bool `json:",default=true"`
    Goroutines bool `json:",default=true"`
    Mutex      bool `json:",default=false"` // 기본적으로 비활성화되어 있으며 성능에 영향을 줍니다
    Block      bool `json:",default=false"` // 기본적으로 비활성화되어 있으며 성능에 영향을 줍니다
}
```

## 4. CPU 부하 시뮬레이션(선택)

프로파일링 동작을 확인하려면 `internal/logic/pinglogic.go`에 CPU를 많이 사용하는 작업을 추가합니다.

```go
func (l *PingLogic) Ping() (resp *types.Resp, err error) {
    simulateCPULoad()
    return &types.Resp{Msg: "pong"}, nil
}

func simulateCPULoad() {
    for i := 0; i < 1000000; i++ {
        _ = i * i * i
    }
}
```

## 5. 실행하고 부하 생성

```bash
# 서비스 시작
go run greet.go -f etc/greet.yaml

# 다른 터미널에서 부하 생성
hey -c 100 -z 60m "http://localhost:8888/ping"
```

`CpuThreshold: 0`이면 서비스가 시작되자마자 Pyroscope로 프로파일을 업로드합니다. `http://localhost:4040`을 열면 flame graph가 실시간으로 갱신되는 것을 볼 수 있습니다.

flame graph에는 `simulateCPULoad`가 대부분의 CPU 시간을 소비하는 것으로 명확히 나타나므로 정확한 hot function을 찾을 수 있습니다.

## 6. 수정 확인

인위적으로 넣은 부하를 제거하고 서비스를 재시작한 뒤 부하 테스트를 다시 실행합니다. flame graph를 통해 CPU 사용량이 내려가고 병목이 사라졌는지 확인할 수 있습니다.

## 프로덕션 권장 사항

- 프로덕션에서는 지속 업로드 오버헤드를 피하기 위해 `CpuThreshold: 700`(70%)을 사용합니다.
- `Mutex`와 `Block` 프로파일링은 특정 동시성 문제를 진단할 때만 활성화합니다.
- 과거 비교가 가능하도록 영구 스토리지를 사용하는 Pyroscope 배포를 권장합니다.
- Grafana 대시보드와 통합해 메트릭과 프로파일을 함께 확인합니다.

## 관련 문서

- [메트릭](../metrics/)
- [추적](../tracing/)
- [로깅](../../log/)
