---
title: 配置中心
description: 使用 go-zero 内置配置中心，基于 etcd 管理动态配置。
sidebar:
  order: 5
---

go-zero 提供了内置的配置中心（`core/configcenter`），支持基于 etcd 或自定义 subscriber 的动态配置管理。配置变更后自动生效，无需重启服务。

## 基本用法

```go
package main

import (
	"github.com/zeromicro/go-zero/core/configcenter"
	"github.com/zeromicro/go-zero/core/configcenter/subscriber"
)

type AppConfig struct {
	Name string `json:"name"`
}

func main() {
	// 创建 etcd subscriber
	ss := subscriber.MustNewEtcdSubscriber(subscriber.EtcdConf{
		Hosts: []string{"localhost:2379"},
		Key:   "app-config",
	})

	// 创建配置中心，使用泛型指定配置类型
	cc := configcenter.MustNewConfigCenter[AppConfig](configcenter.Config{
		Type: "json", // 支持: json, yaml, toml
	}, ss)

	// GetConfig 始终返回最新的配置快照
	v, err := cc.GetConfig()
	if err != nil {
		panic(err)
	}
	println(v.Name)

	// 监听配置变化
	cc.AddListener(func() {
		v, err := cc.GetConfig()
		if err != nil {
			panic(err)
		}
		println("config changed:", v.Name)
	})

	select {} // 阻塞主协程
}
```

## 使用 string 类型

配置中心支持两种模板类型：`struct` 和 `string`。当需要复杂类型如 `[]struct`、`map`、`[]map` 时，使用 `string` 类型后自行解析：

```go
func main() {
	ss := subscriber.MustNewEtcdSubscriber(subscriber.EtcdConf{
		Hosts: []string{"localhost:2379"},
		Key:   "app-config",
	})

	// 使用 string 类型，自行解析
	cc := configcenter.MustNewConfigCenter[string](configcenter.Config{
		Type: "json",
	}, ss)

	v, err := cc.GetConfig()
	if err != nil {
		panic(err)
	}

	// 对 v 进行自定义解析
	_ = v
}
```

## 结构体校验

使用 `struct` 作为模板类型时，配置中心会使用与静态配置相同的校验规则。可以使用标准的 go-zero 配置标签：

```go
type AppConfig struct {
	Name string `json:",optional"`
	Age  int    `json:",default=20"`
}
```

详细规则请参考[参数规则](../../reference/api-dsl/parameter.md)。

## 自定义 Subscriber

go-zero 默认提供 etcd subscriber。你可以实现 `Subscriber` 接口来对接自己的配置后端（如 Consul、Nacos、Apollo）：

```go
package main

import (
	"sync"

	"github.com/zeromicro/go-zero/core/configcenter"
)

type AppConfig struct {
	Name string `json:"name"`
}

// CustomSubscriber 实现 configcenter.Subscriber 接口
type CustomSubscriber struct {
	listeners []func()
	lock      sync.Mutex
}

func (s *CustomSubscriber) AddListener(listener func()) error {
	s.lock.Lock()
	s.listeners = append(s.listeners, listener)
	s.lock.Unlock()
	return nil
}

func (s *CustomSubscriber) Value() (string, error) {
	// 从你的配置后端返回当前配置值
	return `{"name": "my-app"}`, nil
}

func main() {
	sub := &CustomSubscriber{}

	cc := configcenter.MustNewConfigCenter[AppConfig](configcenter.Config{
		Type: "json",
	}, sub)

	v, err := cc.GetConfig()
	if err != nil {
		panic(err)
	}
	println(v.Name)
}
```

## 核心特性

| 特性 | 说明 |
|---|---|
| 内置快照 | 从内存快照高性能读取，`GetConfig()` 不会每次远程调用 |
| 可插拔 subscriber | 默认支持 etcd；实现 `Subscriber` 接口即可对接自定义后端 |
| 自动校验 | struct 类型配置使用与静态配置相同的校验规则 |
| 变更通知 | 注册 listener 实时响应配置变化 |
| 类型安全泛型 | 使用 Go 泛型（`ConfigCenter[T]`）提供编译期类型安全 |
