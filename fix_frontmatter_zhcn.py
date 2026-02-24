#!/usr/bin/env python3
"""Fix frontmatter titles and add descriptions to zh-cn docs."""
import os
import re

FIXES = {
    # tasks/installation
    "zh-cn/tasks/installation/go-zero.md":         ("安装 go-zero", "将 go-zero 框架作为依赖安装到您的 Go 模块中。"),
    "zh-cn/tasks/installation/golang.md":          ("安装 Go", "在 Linux、macOS 或 Windows 上下载并安装 Go 编程语言。"),
    "zh-cn/tasks/installation/goctl.md":           ("安装 goctl", "安装 go-zero 代码生成工具 goctl。"),
    "zh-cn/tasks/installation/goctl-intellij.md":  ("GoLand 插件", "安装并使用 JetBrains GoLand 的 goctl 插件。"),
    "zh-cn/tasks/installation/goctl-vscode.md":    ("VS Code 插件", "安装并使用 Visual Studio Code 的 goctl 扩展。"),
    "zh-cn/tasks/installation/protoc.md":          ("安装 protoc", "安装 Protocol Buffers 编译器及 Go gRPC 插件。"),
    # tasks/create
    "zh-cn/tasks/create/command.md":               ("创建项目（CLI）", "通过命令行脚手架创建新的 go-zero 项目。"),
    "zh-cn/tasks/create/goland.md":                ("创建项目（GoLand）", "通过 JetBrains GoLand 脚手架创建新的 go-zero 项目。"),
    "zh-cn/tasks/create/vscode.md":                ("创建项目（VS Code）", "通过 Visual Studio Code 脚手架创建新的 go-zero 项目。"),
    # tasks/dsl
    "zh-cn/tasks/dsl/api.md":                      ("API 语法", "编写和验证 go-zero .api DSL 文件。"),
    "zh-cn/tasks/dsl/proto.md":                    ("Proto 语法", "为 go-zero gRPC 服务编写 Protocol Buffer .proto 文件。"),
    # tasks/cli
    "zh-cn/tasks/cli/api-demo.md":                 ("API Demo 代码生成", "使用 goctl 从 .api 文件生成完整的 HTTP 服务。"),
    "zh-cn/tasks/cli/api-format.md":               ("API 文件格式化", "使用 goctl 格式化 go-zero .api 文件。"),
    "zh-cn/tasks/cli/grpc-demo.md":                ("gRPC Demo 代码生成", "使用 goctl 从 .proto 文件生成 gRPC 服务。"),
    "zh-cn/tasks/cli/mongo.md":                    ("MongoDB Model 生成", "使用 goctl 生成 MongoDB Model 代码。"),
    "zh-cn/tasks/cli/mysql.md":                    ("MySQL Model 生成", "使用 goctl 生成 MySQL Model 代码。"),
    # tasks
    "zh-cn/tasks/memory-cache.md":                 ("内存缓存", "在 go-zero 服务中使用进程内内存缓存。"),
    "zh-cn/tasks/configcenter.md":                 ("配置中心", "将 go-zero 与远程配置中心集成。"),
    "zh-cn/tasks/static-configuration/configuration.md": ("静态配置", "在 go-zero 中加载和管理静态 YAML/JSON 配置文件。"),
    # tasks/mongo
    "zh-cn/tasks/mongo/conn.md":                   ("MongoDB 连接", "在 go-zero 中创建 MongoDB 连接。"),
    "zh-cn/tasks/mongo/curd.md":                   ("MongoDB CRUD", "使用 MongoDB 进行增删改查操作。"),
    # tasks/mysql
    "zh-cn/tasks/mysql/mysql.md":                  ("MySQL 快速上手", "在 go-zero 中连接 MySQL 并执行查询。"),
    # tasks/redis
    "zh-cn/tasks/redis/redis.md":                  ("Redis 快速上手", "在 go-zero 中连接 Redis 并执行命令。"),
    # tasks/queue
    "zh-cn/tasks/queue/delay-queue.md":            ("延迟队列", "在 go-zero 中使用 beanstalkd 延迟队列。"),
    "zh-cn/tasks/queue/message-queue.md":          ("消息队列", "在 go-zero 中使用 Kafka 消息队列。"),
    # tutorials/cli
    "zh-cn/tutorials/cli/overview.md":             ("goctl 概览", "goctl 代码生成工具概览。"),
    "zh-cn/tutorials/cli/quickstart.md":           ("goctl 快速上手", "快速开始使用 goctl 进行代码生成。"),
    "zh-cn/tutorials/cli/api.md":                  ("goctl API", "从 .api 文件生成 HTTP 服务代码。"),
    "zh-cn/tutorials/cli/rpc.md":                  ("goctl RPC", "从 .proto 文件生成 gRPC 服务代码。"),
    "zh-cn/tutorials/cli/model.md":                ("goctl Model", "使用 goctl 生成数据库 Model 代码。"),
    "zh-cn/tutorials/cli/docker.md":               ("goctl Docker", "使用 goctl 生成 Dockerfile。"),
    "zh-cn/tutorials/cli/kube.md":                 ("goctl Kubernetes", "使用 goctl 生成 Kubernetes 部署清单。"),
    "zh-cn/tutorials/cli/env.md":                  ("goctl 环境", "检查和配置 goctl 构建环境。"),
    "zh-cn/tutorials/cli/config.md":               ("goctl 配置", "管理 goctl 配置。"),
    "zh-cn/tutorials/cli/bug.md":                  ("goctl Bug 上报", "使用 goctl bug 上报问题。"),
    "zh-cn/tutorials/cli/completion.md":           ("Shell 自动补全", "为 goctl 设置 Shell 自动补全。"),
    "zh-cn/tutorials/cli/migrate.md":              ("goctl Migrate", "将 goctl 模板迁移到最新版本。"),
    "zh-cn/tutorials/cli/style.md":                ("goctl 命名风格", "配置生成代码的命名风格。"),
    "zh-cn/tutorials/cli/swagger.md":              ("goctl Swagger", "使用 goctl 生成 Swagger/OpenAPI 文档。"),
    "zh-cn/tutorials/cli/template.md":             ("goctl 模板", "自定义 goctl 代码生成模板。"),
    "zh-cn/tutorials/cli/upgrade.md":              ("goctl 升级", "升级 goctl 至最新版本。"),
    # tutorials/api
    "zh-cn/tutorials/api/faq.md":                  ("API FAQ", "go-zero .api DSL 常见问题解答。"),
    "zh-cn/tutorials/api/import.md":               ("API Import", "使用 import 语句组织 .api 文件。"),
    "zh-cn/tutorials/api/jwt.md":                  ("API JWT 鉴权", "在 .api 文件中声明 JWT 鉴权。"),
    "zh-cn/tutorials/api/middleware.md":           ("API 中间件声明", "在 .api 文件中声明中间件。"),
    "zh-cn/tutorials/api/parameter.md":            ("API 参数", "在 .api 文件中定义请求和响应参数。"),
    "zh-cn/tutorials/api/route-group.md":          ("API 路由分组", "在 .api 文件中对路由进行分组。"),
    "zh-cn/tutorials/api/route-prefix.md":         ("API 路由前缀", "为路由组添加 URL 前缀。"),
    "zh-cn/tutorials/api/route-rule.md":           ("API 路由规则", "在 .api 文件中定义路由规则。"),
    "zh-cn/tutorials/api/route-sse.md":            ("SSE 路由", "在 .api 文件中定义 Server-Sent Events 路由。"),
    "zh-cn/tutorials/api/signature.md":            ("请求签名", "为 API 路由添加 HMAC 签名验证。"),
    "zh-cn/tutorials/api/type.md":                 ("API 类型", "在 .api 文件中定义请求和响应类型。"),
    # tutorials/configuration
    "zh-cn/tutorials/configuration/overview.md":    ("配置概览", "go-zero 服务配置概览。"),
    "zh-cn/tutorials/configuration/log.md":         ("日志配置", "在 go-zero 中配置结构化日志。"),
    "zh-cn/tutorials/configuration/service.md":     ("服务配置", "go-zero HTTP 服务配置完整参考。"),
    "zh-cn/tutorials/configuration/prometheus.md":  ("Prometheus 配置", "在 go-zero 中配置 Prometheus 指标。"),
    # tutorials/gateway
    "zh-cn/tutorials/gateway/grpc.md":             ("gRPC 网关", "使用 go-zero 网关将 gRPC 服务暴露为 HTTP 接口。"),
    "zh-cn/tutorials/gateway/http.md":             ("HTTP 网关", "通过 go-zero 网关代理 HTTP 请求。"),
    # tutorials/grpc
    "zh-cn/tutorials/grpc/interceptor.md":         ("gRPC 拦截器", "为 gRPC 服务添加服务端和客户端拦截器。"),
    "zh-cn/tutorials/grpc/server/configuration.md":("gRPC 服务端配置", "go-zero gRPC 服务端配置完整参考。"),
    "zh-cn/tutorials/grpc/server/example.md":      ("gRPC 服务端示例", "go-zero gRPC 服务端完整示例。"),
    "zh-cn/tutorials/grpc/client/configuration.md":("gRPC 客户端配置", "go-zero gRPC 客户端配置完整参考。"),
    "zh-cn/tutorials/grpc/client/conn.md":         ("gRPC 客户端连接", "在 go-zero 中创建 gRPC 客户端连接。"),
    # tutorials/http/server
    "zh-cn/tutorials/http/server/configuration.md":("HTTP 服务端配置", "go-zero HTTP 服务端配置完整参考。"),
    "zh-cn/tutorials/http/server/error.md":        ("错误处理", "在 go-zero HTTP 服务中处理和格式化错误。"),
    "zh-cn/tutorials/http/server/request-body.md": ("请求体", "在 go-zero HTTP 处理器中解析请求体。"),
    "zh-cn/tutorials/http/server/response-body.md":("响应体", "在 go-zero HTTP 处理器中写入响应体。"),
    "zh-cn/tutorials/http/server/response-ext.md": ("响应扩展", "go-zero HTTP 服务中的扩展响应助手。"),
    "zh-cn/tutorials/http/server/sse.md":          ("Server-Sent Events", "在 go-zero 中使用 SSE 向客户端推送数据。"),
    # tutorials/http
    "zh-cn/tutorials/http/client/index.md":        ("HTTP 客户端", "在 go-zero 服务中发起 HTTP 调用。"),
    # tutorials/log
    "zh-cn/tutorials/log/log.md":                  ("日志", "配置并使用 go-zero 的结构化日志（logx）。"),
    # tutorials/mcp
    "zh-cn/tutorials/mcp/servers.md":              ("MCP 服务器", "使用 go-zero 构建 Model Context Protocol 服务器。"),
    # tutorials/mongo
    "zh-cn/tutorials/mongo/connection.md":         ("MongoDB 连接", "在 go-zero 服务中连接 MongoDB。"),
    "zh-cn/tutorials/mongo/curd.md":               ("MongoDB CRUD", "在 go-zero 中执行 MongoDB 增删改查操作。"),
    "zh-cn/tutorials/mongo/cache.md":              ("MongoDB 缓存", "为 go-zero 中的 MongoDB 查询添加缓存。"),
    # tutorials/mysql
    "zh-cn/tutorials/mysql/connection.md":         ("MySQL 连接", "在 go-zero 服务中连接 MySQL。"),
    "zh-cn/tutorials/mysql/curd.md":               ("MySQL CRUD", "在 go-zero 中执行 MySQL 增删改查操作。"),
    "zh-cn/tutorials/mysql/cache.md":              ("MySQL 缓存", "使用 go-zero sqlc 为 MySQL 查询添加缓存。"),
    "zh-cn/tutorials/mysql/bulk-insert.md":        ("MySQL 批量插入", "在 go-zero 中高效执行批量插入。"),
    "zh-cn/tutorials/mysql/local-transaction.md":  ("本地事务", "在 go-zero sqlx 中使用本地事务。"),
    "zh-cn/tutorials/mysql/distribute-transaction.md":("分布式事务", "在 go-zero 中使用分布式事务。"),
    # tutorials/ops
    "zh-cn/tutorials/ops/prepare.md":              ("环境准备", "准备 CI/CD 环境（GitLab、Jenkins、Harbor、Kubernetes）。"),
    "zh-cn/tutorials/ops/docker-compose.md":       ("Docker Compose 部署", "使用 Docker Compose 部署 go-zero 服务。"),
    "zh-cn/tutorials/ops/machine.md":              ("物理机部署", "将 go-zero 服务部署到物理机或虚拟机。"),
    "zh-cn/tutorials/ops/k8s.md":                  ("Kubernetes CI/CD 流水线", "通过 Jenkins CI/CD 流水线将 go-zero 服务部署到 Kubernetes。"),
    # tutorials/proto
    "zh-cn/tutorials/proto/spec.md":               ("Proto 规范", "go-zero Protocol Buffer 规范和约定。"),
    "zh-cn/tutorials/proto/services-group.md":     ("服务分组", "在单个 .proto 文件中组织多个服务。"),
    "zh-cn/tutorials/proto/faq.md":                ("Proto FAQ", "go-zero Proto 使用常见问题解答。"),
    # tutorials/queue
    "zh-cn/tutorials/queue/kafka.md":              ("Kafka 队列", "在 go-zero 中使用 Kafka 消息队列。"),
    "zh-cn/tutorials/queue/beanstalkd.md":         ("Beanstalkd 队列", "在 go-zero 中使用 Beanstalkd 延迟队列。"),
    # tutorials/redis
    "zh-cn/tutorials/redis/db-selection.md":       ("Redis DB 选择", "在 go-zero 中配置 Redis 数据库选择。"),
    "zh-cn/tutorials/redis/metric.md":             ("Redis 指标", "在 go-zero 中监控 Redis 连接指标。"),
    "zh-cn/tutorials/redis/redis-lock.md":         ("Redis 分布式锁", "在 go-zero 中使用 Redis 实现分布式锁。"),
    # tutorials/service-governance
    "zh-cn/tutorials/service-governance/breaker.md":    ("熔断器", "在 go-zero 服务中配置熔断。"),
    "zh-cn/tutorials/service-governance/limiter.md":    ("限流器", "在 go-zero 服务中配置限流。"),
    "zh-cn/tutorials/service-governance/loadbalance.md":("负载均衡", "在 go-zero RPC 客户端中配置负载均衡。"),
    # tutorials/cron-job
    "zh-cn/tutorials/cron-job/k8s.md":             ("Kubernetes 定时任务", "在 Kubernetes 上使用 go-zero 调度定时任务。"),
    # tutorials/customization
    "zh-cn/tutorials/customization/template.md":   ("模板自定义", "自定义 goctl 代码生成模板。"),
    # concepts
    "zh-cn/concepts/architecture-evolution.md":    ("架构演进", "go-zero 架构从单体到微服务的演进过程。"),
    "zh-cn/concepts/components.md":               ("组件架构", "go-zero 核心组件及其关系概览。"),
    "zh-cn/concepts/keywords.md":                 ("关键词", "go-zero 生态系统中的关键术语和概念。"),
    "zh-cn/concepts/layout.md":                   ("项目结构", "go-zero 项目的标准目录结构。"),
    # components
    "zh-cn/components/fx.md":                      ("FX Pipeline", "使用 go-zero FX 流式工具构建数据管道。"),
    "zh-cn/components/mr.md":                      ("MapReduce", "使用 go-zero mr 进行并发 map-reduce。"),
    "zh-cn/components/limiter/peroid.md":          ("Period Limiter", "使用 go-zero 按时间段限制请求速率。"),
    "zh-cn/components/limiter/token.md":           ("Token Bucket Limiter", "使用 go-zero 令牌桶限制请求速率。"),
    "zh-cn/components/log/logc.md":                ("logc", "使用 go-zero logc 进行上下文感知的结构化日志记录。"),
    "zh-cn/components/log/logx.md":                ("logx", "使用 go-zero logx 进行结构化日志记录。"),
    # faq
    "zh-cn/faq/deploy/binary-size.md":             ("减小二进制体积", "减小生产环境 Go 二进制体积的技巧。"),
    "zh-cn/faq/http/cors.md":                      ("CORS 配置", "在 go-zero HTTP 服务中配置跨域资源共享。"),
    "zh-cn/faq/http/fileserver.md":                ("文件服务器", "通过 go-zero HTTP 服务提供静态文件。"),
    "zh-cn/faq/log/fileconsole.md":                ("同时输出到文件和控制台", "在 go-zero 中同时将日志输出到文件和控制台。"),
    # reference
    "zh-cn/reference/goctl-plugins.md":           ("goctl 插件", "使用社区插件扩展 goctl。"),
    # contributing
    "zh-cn/contributing/contributors.md":          ("贡献者", "构建 go-zero 的开发者们。"),
    # tutorials/microservice
    "zh-cn/tutorials/microservice/service-discovery.md": ("服务发现", "在 go-zero 微服务中注册和发现服务。"),
    "zh-cn/tutorials/microservice/load-balancing.md":    ("负载均衡", "在 go-zero 微服务中配置负载均衡。"),
    "zh-cn/tutorials/microservice/distributed-tracing.md":("链路追踪", "为 go-zero 微服务添加分布式链路追踪。"),
    # monitor
    "zh-cn/tutorials/monitor/index.md":            ("监控与可观测性", "使用指标、追踪和日志监控 go-zero 服务。"),
    # configuration
    "zh-cn/tutorials/configuration/auto-validation.md": ("配置自动校验", "在 go-zero 启动时自动校验配置。"),
}

docs_root = "src/content/docs"
updated = 0
skipped = 0

for rel_path, (new_title, new_desc) in FIXES.items():
    full_path = os.path.join(docs_root, rel_path)
    if not os.path.exists(full_path):
        skipped += 1
        continue

    with open(full_path, encoding='utf-8') as f:
        original = f.read()

    if not original.startswith("---\n"):
        skipped += 1
        continue

    close_idx = original.find("\n---\n", 4)
    if close_idx == -1:
        skipped += 1
        continue

    fm_raw = original[4:close_idx]
    body = original[close_idx + 5:]

    # Update title
    if re.search(r'^title:', fm_raw, re.MULTILINE):
        fm_raw = re.sub(r'^title:.*$', f'title: {new_title}', fm_raw, flags=re.MULTILINE, count=1)
    else:
        fm_raw = f'title: {new_title}\n' + fm_raw

    # Update or add description
    if new_desc:
        if re.search(r'^description:', fm_raw, re.MULTILINE):
            fm_raw = re.sub(r'^description:.*$', f'description: {new_desc}', fm_raw, flags=re.MULTILINE, count=1)
        else:
            fm_raw = re.sub(
                r'^(title:.*)$',
                r'\1\ndescription: ' + new_desc,
                fm_raw,
                flags=re.MULTILINE,
                count=1,
            )

    new_content = "---\n" + fm_raw + "\n---\n" + body

    if new_content != original:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated += 1

print(f"Updated {updated} zh-cn files, skipped {skipped}")
