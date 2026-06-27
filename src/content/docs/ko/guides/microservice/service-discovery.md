---
title: 서비스 디스커버리
description: go-zero의 서비스 디스커버리에 대해 설명합니다.
sidebar:
  order: 2

---


## etcd (권장 위한 프로덕션)

### 서버 Registration

추가 `Etcd` block 로 RPC 서버 설정 — 없음 code changes needed:

```yaml title="etc/order-rpc.yaml"
Name: order.rpc
ListenOn: 0.0.0.0:8080
Etcd:
  Hosts:
    - 127.0.0.1:2379
  Key: order.rpc         # 예시입니다
```


### 클라이언트 디스커버리

Point 클라이언트 설정 at same etcd cluster과 key:

```yaml title="etc/user-api.yaml"
OrderRpc:
  Etcd:
    Hosts:
      - 127.0.0.1:2379
    Key: order.rpc
  Timeout: 2000
```

```go title="internal/svc/servicecontext.go"
orderConn := zrpc.MustNewClient(c.OrderRpc)
svc.OrderRpc = order.NewOrderClient(orderConn.Conn())
```

### etcd Cluster

위한 높은 availability 사용 three 또는 five nodes:

```yaml
Etcd:
  Hosts:
    - etcd1.infra:2379
    - etcd2.infra:2379
    - etcd3.infra:2379
  Key: order.rpc
```

## Kubernetes DNS


```yaml
OrderRpc:
  Target: dns:///order-rpc-svc.default.svc.cluster.local:8080
```

또는 사용 list 의 pod 엔드포인트 directly (useful 사용하여 StatefulSets):

```yaml
OrderRpc:
  Endpoints:
    - order-rpc-0.order-rpc-svc.default:8080
    - order-rpc-1.order-rpc-svc.default:8080
```

## Static 엔드포인트 (Dev / CI)

위한 로컬 개발 또는 integration 테스트, skip etcd entirely:

```yaml
OrderRpc:
  Endpoints:
    - 127.0.0.1:8080
```

## Service Key Conventions

| Convention | 예제 | Notes |
|---|---|---|
| `<name>.rpc` | `order.rpc` | 표준; matches `Name` 필드 |
| `<env>/<name>.rpc` | `prod/order.rpc` | Multi-environment 공유 etcd |
| `<ns>.<name>.rpc` | `payment.order.rpc` | Domain namespacing |

사용 same string 에서 서버's `Etcd.Key`과 클라이언트's `Etcd.Key`.

## 헬스 체크


```yaml title="k8s/order-rpc.yaml"
livenessProbe:
  exec:
    command: ["/bin/grpc_health_probe", "-addr=:8080"]
  initialDelaySeconds: 5
  periodSeconds: 10
readinessProbe:
  exec:
    command: ["/bin/grpc_health_probe", "-addr=:8080"]
  initialDelaySeconds: 3
  periodSeconds: 5
```

## 부하 분산


## Graceful Scaling
