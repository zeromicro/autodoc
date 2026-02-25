---
title: 服务发现
description: 在 go-zero 微服务中注册和发现服务。
sidebar:
  order: 2

---

# 服务发现

go-zero 支持可插拔的服务发现后端。每个 RPC 服务端在启动时自动注册；每个 RPC 客户端持续监听注册表，并通过 P2C 负载均衡选择健康实例。

## etcd（推荐用于生产）

### 服务注册（服务端）

在 RPC 服务端配置中添加 `Etcd` 块——无需修改任何代码：

```yaml title="etc/order-rpc.yaml"
Name: order.rpc
ListenOn: 0.0.0.0:8080
Etcd:
  Hosts:
    - 127.0.0.1:2379
  Key: order.rpc         # 服务发现 key，客户端使用完全相同的字符串
```

go-zero 在启动时调用 `etcd.Put(key, address)` 完成注册，优雅退出时调用 `etcd.Delete`；同时持有租约，进程崩溃后过期条目自动清理。

### 客户端发现

客户端配置指向相同的 etcd 集群和 key：

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

### etcd 集群

生产环境建议部署 3 或 5 个节点：

```yaml
Etcd:
  Hosts:
    - etcd1.infra:2379
    - etcd2.infra:2379
    - etcd3.infra:2379
  Key: order.rpc
```

## Kubernetes DNS

在 Kubernetes 内部运行时，可以用 Headless Service 的 DNS 名替代 etcd：

```yaml
OrderRpc:
  Target: dns:///order-rpc-svc.default.svc.cluster.local:8080
```

或直接列出 Pod 的 endpoint（适用于 StatefulSet）：

```yaml
OrderRpc:
  Endpoints:
    - order-rpc-0.order-rpc-svc.default:8080
    - order-rpc-1.order-rpc-svc.default:8080
```

## 静态 Endpoint（开发/CI）

本地开发或集成测试时，跳过 etcd 直连：

```yaml
OrderRpc:
  Endpoints:
    - 127.0.0.1:8080
```

## 服务 Key 命名约定

| 约定 | 示例 | 说明 |
|------|------|------|
| `<名称>.rpc` | `order.rpc` | 标准格式，与 `Name` 字段一致 |
| `<环境>/<名称>.rpc` | `prod/order.rpc` | 多环境共用 etcd 时区分环境 |
| `<域>.<名称>.rpc` | `payment.order.rpc` | 业务域命名空间 |

服务端的 `Etcd.Key` 和客户端的 `Etcd.Key` 必须使用完全相同的字符串。

## 健康检查

go-zero RPC 服务端自动实现 [gRPC 健康检查协议](https://github.com/grpc/grpc/blob/master/doc/health-checking.md)，可直接用于 Kubernetes 探针：

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

## 负载均衡

客户端默认使用 **P2C（二选一）** 结合 EWMA 延迟算法。每次调用从注册表中随机选两个实例，转发给负载更低的那个——无需任何配置。

## 平滑扩缩容

新实例启动并注册到 etcd 后，客户端在租约 TTL（默认 10 秒）内感知到新实例。实例优雅退出时（收到 SIGTERM）会先注销自身再停止接受新连接，确保滚动发布期间零请求丢失。
