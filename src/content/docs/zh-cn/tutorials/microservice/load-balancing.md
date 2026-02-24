---
title: 负载均衡
description: 在 go-zero 微服务中配置负载均衡。
sidebar:
  order: 3

---

# 负载均衡

go-zero 的 `zrpc` 客户端默认使用 **P2C（Pick of Two Choices，二选一）** 负载均衡，相较于传统轮询更能感知实例延迟。

## P2C 算法原理

<pre class="mermaid">
flowchart LR
    Client -->|随机选两个实例| A[实例 A<br/>延迟 12 ms]
    Client --> B[实例 B<br/>延迟 45 ms]
    A -->|✓ 延迟更低，被选中| Req[发送请求]
    B -->|✗ 跳过| Skip[未选中]
</pre>

每次发起请求时，P2C 会从候选实例中**随机选取两个**，然后将请求路由至负载（延迟 × 在途请求数）更低的那个。这个 O(1) 的算法解决了轮询面对"慢实例"时的热点问题。

## 默认行为

当使用 etcd 服务发现时，P2C 负载均衡**自动生效**，无需任何配置：

```yaml title="etc/app.yaml"
UserRpc:
  Etcd:
    Hosts: [127.0.0.1:2379]
    Key: user.rpc
```

etcd 中每个注册的实例都会自动纳入 P2C 的候选池。

## 静态端点（轮询）

使用静态地址列表时，go-zero 使用轮询策略：

```yaml
UserRpc:
  Endpoints:
    - 10.0.0.1:8080
    - 10.0.0.2:8080
    - 10.0.0.3:8080
```

## 直连（无负载均衡）

测试或调试时，可以直接指定单个实例：

```yaml
UserRpc:
  Endpoints:
    - 127.0.0.1:8080
```

## Kubernetes 集成

在 Kubernetes 中，通常将 go-zero 服务作为 Headless Service 部署，结合 Pod DNS 地址实现均衡：

```yaml title="k8s/service.yaml"
apiVersion: v1
kind: Service
metadata:
  name: user-rpc
spec:
  clusterIP: None   # Headless Service
  selector:
    app: user-rpc
  ports:
    - port: 8080
```

然后在 go-zero 配置中直接使用 DNS 地址：

```yaml
UserRpc:
  Target: dns:///user-rpc.default.svc.cluster.local:8080
```

## 可观测性

可通过 Prometheus 监控负载均衡效果：

| 指标名 | 说明 |
|---|---|
| `rpc_client_requests_total` | 各实例请求总数 |
| `rpc_client_duration_ms_bucket` | 各实例延迟直方图 |

在 Grafana 中用分位数折线图对比各 Pod 的 P99 延迟，可直观看到 P2C 是否有效均摊流量。

## 超时与 Keepalive

```yaml
UserRpc:
  Timeout: 2000           # 单次请求超时（毫秒）
  KeepaliveTime: 20000    # TCP keepalive ping 间隔（毫秒）
```

超时期间只要约束对应 ctx 即可；go-zero 不会自动重试（防止副作用），如需重试请在业务层实现幂等逻辑后自行封装。

## 延伸阅读

- [gRPC 客户端](../grpc/client) — 客户端完整配置参考
- [分布式链路追踪](./distributed-tracing) — 追踪请求在各实例间的路径
