---
title: Config Center
description: Integrate go-zero with a remote configuration center.
sidebar:
  order: 13

---


Go-zero will soon support the configuration center function in the new version (v1.7.1). This article introduces the simple use of the configuration center in advance, and introduces the use precautions and characters. code https://github.com/zeromicro/go-zero/pull/3035.

## Demo

```go
package main

import (
        "github.com/zeromicro/go-zero/core/configcenter"
        "github.com/zeromicro/go-zero/core/configcenter/subscriber"
        "github.com/zeromicro/go-zero/core/discov"
)

// configuration structure definition
type TestSt struct {
        Name string `json:"name"`
}

func main() {
        // 创建 etcd subscriber
        ss := subscriber.MustNewEtcdSubscriber(subscriber.EtcdConf{
            Hosts: []string{"localhost:2379"}, // ETCD address
            Key:   "test1",    // Configuration key
        })
        
        // Create configurator
        cc := configurator.MustNewConfigCenter[TestSt](configurator.Config{
                Type: "json", // Configuration value type: json, yaml, toml
        }, ss)

        // Get configuration
        // Note: If the configuration changes, the result of the call will always get the latest configuration
        v, err := cc.GetConfig() 
        if err != nil {
                panic(err)
        }
        println(v.Name)
        
        // If you want to listen for configuration changes, you can add listeners
        cc.AddListener(func() {
                v, err := cc.GetConfig()
                if err != nil {
                        panic(err)
                }
                println(v.Name)
        })

        select {}
}
```

## Note

1. configurator Supported template types: struct, string。

2. If you want to use more configuration types([]struct,map,[]map...)，You can use the string type to get the data and parse it yourself.

    ```go
    func main() {
            // Create etcd subscriber
            ss := subscriber.MustNewEtcdSubscriber(subscriber.EtcdConf{
                Hosts: []string{"localhost:2379"}, // ETCD address
                Key:   "test1",    // Configuration key
            })
            
            // Create configurator
            cc := configurator.MustNewConfigCenter[string](configurator.Config{
                    Type: "json", // Configuration value type: json, yaml, toml
            }, ss)
    
            // Get configuration
            // Note: If the configuration changes, the result of the call will always get the latest configuration
            v, err := cc.GetConfig() 
            if err != nil {
                    panic(err)
            }
            
            // For cc. GetConfig () results, customize the parsing method
    }
    ```
3. If it is a struct template type, the parser of the configurator is the same as the static configuration method, and the config will be checked. For detailed rules, please refer to: <a href="docs/tutorials/api/parameter" target="_blank">参数规则</a>

```go
// configuration structure definition
type TestSt struct {
        Name string `json:",optional"`
        age  int    `json:",default=20"`
}
```

## Features

1. Configurator built-in snapshot data, can provide high performance capabilities.

2. Configurator supports custom subscribers, you can customize extensions according to your own technology stack, go-zero supports etcd by default.

```go
package main

import (
        "sync"

        "github.com/zeromicro/go-zero/core/configcenter"
)

type TestSt struct {
        Name string `json:"name"`
}

// Custom Subscriber
type MySubscriber struct {
        listeners []func()
        lock      sync.Mutex
}

// Implement Custom AddListeners
func (m *MySubscriber) AddListener(listener func()) error {
        m.lock.Lock()
        m.listeners = append(m.listeners, listener)
        m.lock.Unlock()
        return nil
}

// Implement Custom Values
func (m *MySubscriber) Value() (string, error) {
        return "", nil
}

func main() {
        mySubscriber := &MySubscriber{}

        cc := configurator.MustNewConfigCenter[TestSt](configurator.Config{
                Type: "json",
        }, mySubscriber) // Inject Custom Subscribers
        v, err := cc.GetConfig()
        if err != nil {
                panic(err)
        }
        println(len(v.Name))
}
```