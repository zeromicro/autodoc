---
title: 项目结构
description: 标准 go-zero 项目目录及职责说明。
sidebar:
  order: 5
---

# 项目结构

```text
greet/
├── etc/                 # 配置文件
├── internal/
│   ├── config/          # 配置结构定义
│   ├── handler/         # 请求路由与参数绑定
│   ├── logic/           # 业务逻辑
│   ├── svc/             # 依赖注入与上下文
│   └── types/           # 请求响应类型
└── greet.go             # 服务入口
```

## 推荐实践

- 将共享依赖统一收敛在 `svc.ServiceContext`
- 把业务逻辑放入 `logic`，避免在 handler 堆积业务代码
- 保持配置与环境变量映射清晰，便于部署
