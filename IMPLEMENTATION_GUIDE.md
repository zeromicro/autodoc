# go-zero 风格文档网站实现指南

> 本文档为 Agent 提供详尽的实现规范，用于生成类似 go-zero.dev 的技术框架文档网站。

---

## 一、项目概述

### 1.1 目标
为开源技术框架创建一个专业、易用、结构清晰的文档网站，具备以下特点：
- 渐进式内容组织（从入门到精通）
- 多语言支持（中英文）
- 代码示例与架构图结合
- 搜索与导航便捷

### 1.2 技术栈选择

| 框架 | 适用场景 | 特点 |
|------|---------|------|
| **Astro + Starlight** (当前项目) | 现代文档站 | 构建快、Markdown 优先、组件化 |
| Docusaurus (go-zero 官方) | React 生态 | 社区成熟、插件丰富 |
| VitePress | Vue 生态 | 轻量、Vite 驱动 |

本项目使用 **Astro + Starlight**，以下规范基于此技术栈。

---

## 二、目录结构规范

### 2.1 整体结构

```
zerodoc/
├── public/                    # 静态资源
│   ├── favicon.svg
│   └── og-image.png          # 社交分享图
├── src/
│   ├── assets/               # 图片、SVG 图表
│   │   ├── architecture.svg  # 架构图
│   │   ├── resilience.svg    # 弹性设计图
│   │   └── benchmark/        # 性能图表
│   ├── content/
│   │   └── docs/             # 文档内容（核心）
│   │       ├── index.mdx     # 首页
│   │       ├── concepts/     # 概念篇
│   │       ├── getting-started/ # 快速开始
│   │       ├── tutorials/    # 指南教程
│   │       ├── components/   # 组件文档
│   │       ├── reference/    # API 参考
│   │       ├── faq/          # 常见问题
│   │       └── contributing/ # 贡献指南
│   ├── components/           # 自定义组件
│   └── content.config.ts     # 内容配置
├── astro.config.mjs          # Astro 配置
├── package.json
└── tsconfig.json
```

### 2.2 文档目录详细规划

```
src/content/docs/
├── index.mdx                 # 首页（框架介绍 + 快速导航）
│
├── concepts/                 # 【概念篇】理解框架设计
│   ├── index.md              # 概述：框架定位与优势
│   ├── glossary.md           # 名词术语表
│   ├── architecture.md       # 架构设计（含架构图）
│   ├── design-principles.md  # 设计原则
│   └── project-structure.md  # 项目结构说明
│
├── getting-started/          # 【快速开始】新手入门
│   ├── index.md              # 开始之前（总览）
│   ├── installation/         # 安装环境
│   │   ├── golang.md         # Go 环境安装
│   │   ├── goctl.md          # goctl 工具安装
│   │   ├── protoc.md         # protoc 安装
│   │   └── ide-plugins.md    # IDE 插件安装
│   ├── dsl/                  # 领域语言
│   │   ├── api-syntax.md     # API 语法规范
│   │   └── proto-syntax.md   # Proto 语法规范
│   ├── quickstart/           # 快速上手
│   │   ├── hello-world.md    # Hello World 示例
│   │   ├── api-service.md    # 创建 API 服务
│   │   └── rpc-service.md    # 创建 RPC 服务
│   └── project-creation.md   # 项目创建方式
│
├── tutorials/                # 【指南篇】场景化教程
│   ├── index.md              # 教程目录
│   ├── http/                 # HTTP 服务开发
│   │   ├── basic.md          # 基础开发
│   │   ├── middleware.md     # 中间件
│   │   ├── jwt-auth.md       # JWT 认证
│   │   └── file-upload.md    # 文件上传
│   ├── grpc/                 # gRPC 服务开发
│   │   ├── server.md         # 服务端开发
│   │   ├── client.md         # 客户端调用
│   │   └── interceptor.md    # 拦截器
│   ├── database/             # 数据库操作
│   │   ├── mysql.md          # MySQL
│   │   ├── mongodb.md        # MongoDB
│   │   └── redis.md          # Redis
│   ├── microservice/         # 微服务实战
│   │   ├── service-discovery.md  # 服务发现
│   │   ├── load-balancing.md     # 负载均衡
│   │   └── distributed-tracing.md # 链路追踪
│   └── deployment/           # 部署运维
│       ├── docker.md         # Docker 部署
│       └── kubernetes.md     # K8s 部署
│
├── components/               # 【组件篇】内置组件详解
│   ├── index.md              # 组件总览
│   ├── resilience/           # 弹性组件
│   │   ├── rate-limiter.md   # 限流器
│   │   ├── circuit-breaker.md # 熔断器
│   │   ├── load-shedding.md  # 降载
│   │   └── timeout.md        # 超时控制
│   ├── cache/                # 缓存组件
│   │   ├── memory-cache.md   # 内存缓存
│   │   └── redis-cache.md    # Redis 缓存
│   ├── queue/                # 队列组件
│   │   ├── kafka.md          # Kafka
│   │   └── rabbitmq.md       # RabbitMQ
│   └── observability/        # 可观测性
│       ├── logging.md        # 日志
│       ├── metrics.md        # 指标
│       └── tracing.md        # 追踪
│
├── reference/                # 【参考篇】API 与配置
│   ├── index.md              # 参考文档目录
│   ├── goctl/                # goctl 命令参考
│   │   ├── commands.md       # 命令一览
│   │   ├── api.md            # api 子命令
│   │   ├── rpc.md            # rpc 子命令
│   │   └── model.md          # model 子命令
│   ├── configuration/        # 配置参考
│   │   ├── api-config.md     # API 服务配置
│   │   └── rpc-config.md     # RPC 服务配置
│   └── changelog.md          # 更新日志
│
├── faq/                      # 【FAQ】常见问题
│   ├── index.md              # FAQ 首页
│   ├── installation.md       # 安装问题
│   ├── goctl.md              # goctl 问题
│   └── deployment.md         # 部署问题
│
└── contributing/             # 【贡献指南】
    ├── index.md              # 如何贡献
    ├── code-style.md         # 代码规范
    ├── pull-request.md       # PR 流程
    └── documentation.md      # 文档贡献
```

---

## 三、内容编写规范

### 3.1 文档 Frontmatter 结构

每个 Markdown 文件必须包含 frontmatter：

```yaml
---
title: 页面标题
description: 页面描述，用于 SEO 和预览
sidebar:
  order: 1                    # 侧边栏排序
  badge:                      # 可选徽章
    text: New
    variant: tip
tableOfContents:              # 目录配置
  minHeadingLevel: 2
  maxHeadingLevel: 4
---
```

### 3.2 首页结构（index.mdx）

首页应包含以下模块（按顺序）：

```markdown
# 框架名称

## 一句话定位
> go-zero 是一个集成了各种工程实践的 web 和 rpc 框架

## 核心优势（3-5 点）
- ✅ 优势一：简要说明
- ✅ 优势二：简要说明
- ✅ 优势三：简要说明

## 架构图
![架构图](../../assets/architecture.svg)

## 快速开始
```bash
# 安装命令
go install github.com/zeromicro/go-zero/tools/goctl@latest
```

## 功能特性
以分类表格或卡片形式展示

## 谁在使用
展示用户 logo（如有授权）

## 社区与资源
- GitHub
- Discord / 微信群
- 文档链接
```

### 3.3 概念类文档结构

```markdown
---
title: 架构设计
description: 了解 go-zero 的整体架构与设计理念
---

# 架构设计

## 概述
1-2 段介绍本章主题

## 架构图
![架构图](path/to/architecture.svg)
*图注说明*

## 核心层次

### 层次一：网关层
- 功能说明
- 关键组件

### 层次二：服务治理层
- 功能说明
- 关键组件

## 设计原则
1. **原则名称**：详细说明
2. **原则名称**：详细说明

## 下一步
引导读者继续阅读相关文档
```

### 3.4 教程类文档结构

```markdown
---
title: 创建第一个 API 服务
description: 从零开始创建一个 HTTP API 服务
---

# 创建第一个 API 服务

## 前置条件
- [ ] Go 1.18+
- [ ] goctl 已安装

## 目标
本教程完成后，你将学会：
- 目标 1
- 目标 2

## 步骤

### 第一步：创建项目
```bash
goctl api new greet
```

详细说明这一步做了什么

### 第二步：编写业务逻辑
```go
func (l *GreetLogic) Greet(req *types.Request) (resp *types.Response, err error) {
    return &types.Response{
        Message: "Hello " + req.Name,
    }, nil
}
```

### 第三步：运行服务
```bash
go run greet.go
```

## 验证结果
```bash
curl http://localhost:8888/from/you
```

预期输出：
```json
{"message": "Hello you"}
```

## 完整代码
提供 GitHub 链接或完整代码块

## 常见问题
- **问题 1**：解答
- **问题 2**：解答

## 下一步
- [添加中间件](./middleware.md)
- [连接数据库](./database.md)
```

### 3.5 组件/API 参考文档结构

```markdown
---
title: 限流器 (Rate Limiter)
description: 自适应限流器的使用与配置
---

# 限流器

## 概述
一句话说明组件用途

## 使用场景
- 场景 1
- 场景 2

## 基础用法

```go
import "github.com/zeromicro/go-zero/core/limit"

limiter := limit.NewTokenLimiter(rate, burst, store, key)
if limiter.Allow() {
    // 处理请求
}
```

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| rate | int | 100 | 每秒允许的请求数 |
| burst | int | 100 | 突发容量 |

## 高级配置

### 分布式限流
```go
// 代码示例
```

### 自定义策略
```go
// 代码示例
```

## 最佳实践
- 实践 1
- 实践 2

## 相关组件
- [熔断器](./circuit-breaker.md)
- [降载](./load-shedding.md)
```

---

## 四、视觉元素规范

### 4.1 架构图要求

使用 SVG 格式，遵循以下规范：

1. **布局**：分层结构，从上到下或从左到右
2. **配色**：使用语义化颜色
   - 蓝色系：网关/入口层
   - 黄色系：服务治理层
   - 绿色系：业务服务层
   - 紫色系：基础设施层
   - 粉色系：工具链
3. **字体**：使用中文友好字体 `PingFang SC, Microsoft YaHei, system-ui`
4. **尺寸**：宽度 700-800px，确保在文档中清晰展示

### 4.2 需要的图表清单

| 图表名称 | 用途 | 放置位置 |
|---------|------|---------|
| 架构总览图 | 展示框架整体结构 | 首页、概念/架构设计 |
| 弹性设计图 | 展示高可用机制 | 概念/设计原则、组件/弹性 |
| 请求流程图 | 展示请求处理链路 | 教程/HTTP 开发 |
| 服务调用图 | 展示微服务调用关系 | 教程/微服务实战 |
| goctl 工作流程图 | 展示代码生成流程 | 快速开始、参考/goctl |
| 部署架构图 | 展示生产环境部署 | 教程/部署运维 |

### 4.3 代码块规范

1. **语言标注**：必须标注语言类型
   ```go
   // Go 代码
   ```
   ```bash
   # Shell 命令
   ```
   ```yaml
   # 配置文件
   ```

2. **文件路径**：复杂示例标注文件路径
   ```go title="greet/internal/logic/greetlogic.go"
   // 代码内容
   ```

3. **高亮行**：重点行使用高亮
   ```go {3-5}
   // 高亮第 3-5 行
   ```

4. **命令输出**：区分输入和输出
   ```bash
   $ goctl api new greet  # 输入
   Done.                  # 输出
   ```

---

## 五、Astro/Starlight 配置

### 5.1 astro.config.mjs 配置

```javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'go-zero',
      logo: {
        src: './src/assets/logo.svg',
      },
      social: {
        github: 'https://github.com/zeromicro/go-zero',
        discord: 'https://discord.gg/xxx',
      },
      defaultLocale: 'zh-cn',
      locales: {
        'zh-cn': {
          label: '简体中文',
          lang: 'zh-CN',
        },
        en: {
          label: 'English',
          lang: 'en',
        },
      },
      sidebar: [
        {
          label: '概念',
          translations: { en: 'Concepts' },
          items: [
            { label: '框架概述', link: '/concepts/' },
            { label: '名词介绍', link: '/concepts/glossary' },
            { label: '架构设计', link: '/concepts/architecture' },
            { label: '设计原则', link: '/concepts/design-principles' },
            { label: '项目结构', link: '/concepts/project-structure' },
          ],
        },
        {
          label: '快速开始',
          translations: { en: 'Getting Started' },
          collapsed: false,
          autogenerate: { directory: 'getting-started' },
        },
        {
          label: '指南',
          translations: { en: 'Tutorials' },
          collapsed: true,
          autogenerate: { directory: 'tutorials' },
        },
        {
          label: '组件',
          translations: { en: 'Components' },
          collapsed: true,
          autogenerate: { directory: 'components' },
        },
        {
          label: '参考',
          translations: { en: 'Reference' },
          collapsed: true,
          autogenerate: { directory: 'reference' },
        },
        {
          label: 'FAQ',
          link: '/faq/',
        },
        {
          label: '贡献指南',
          translations: { en: 'Contributing' },
          link: '/contributing/',
        },
      ],
      editLink: {
        baseUrl: 'https://github.com/zeromicro/go-zero.dev/edit/main/',
      },
      customCss: ['./src/styles/custom.css'],
      head: [
        {
          tag: 'meta',
          attrs: {
            property: 'og:image',
            content: '/og-image.png',
          },
        },
      ],
    }),
  ],
});
```

### 5.2 自定义样式（src/styles/custom.css）

```css
/* 主题色覆盖 */
:root {
  --sl-color-accent-low: #dbeafe;
  --sl-color-accent: #3b82f6;
  --sl-color-accent-high: #1e40af;
}

/* 中文字体优化 */
:root {
  --sl-font: 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif;
}

/* 代码块样式 */
.expressive-code pre {
  border-radius: 8px;
}
```

---

## 六、内容生成流程

### 6.1 Agent 执行步骤

1. **环境检查**
   - 确认项目已初始化（package.json 存在）
   - 确认 Starlight 依赖已安装

2. **创建目录结构**
   - 按照 2.2 节规划创建所有目录
   - 为每个目录创建 index.md 占位文件

3. **生成核心配置**
   - 更新 astro.config.mjs（按 5.1 节）
   - 创建自定义样式文件

4. **生成首页**
   - 创建 src/content/docs/index.mdx
   - 包含框架介绍、架构图、快速开始

5. **生成概念文档**（按优先级）
   - concepts/index.md - 框架概述
   - concepts/architecture.md - 架构设计
   - concepts/glossary.md - 名词术语

6. **生成快速开始**
   - getting-started/index.md
   - getting-started/installation/*.md
   - getting-started/quickstart/*.md

7. **生成教程文档**
   - tutorials/http/*.md
   - tutorials/grpc/*.md
   - tutorials/database/*.md

8. **生成组件文档**
   - components/resilience/*.md
   - components/cache/*.md

9. **生成参考文档**
   - reference/goctl/*.md
   - reference/configuration/*.md

10. **生成 FAQ 和贡献指南**
    - faq/*.md
    - contributing/*.md

11. **生成图表资源**
    - 使用 svg-diagram skill 生成架构图
    - 放置到 src/assets/ 目录

12. **验证构建**
    - 运行 `npm run build`
    - 检查无报错

### 6.2 内容来源

文档内容应从以下来源获取：

1. **官方 README**：https://github.com/zeromicro/go-zero
2. **官方文档**：https://go-zero.dev
3. **源码注释**：go-zero 源码中的 GoDoc 注释
4. **示例代码**：https://github.com/zeromicro/go-zero/tree/master/example

### 6.3 质量检查清单

- [ ] 所有链接可访问
- [ ] 代码示例可运行
- [ ] 图片正确显示
- [ ] 侧边栏导航正确
- [ ] 多语言切换正常
- [ ] 搜索功能可用
- [ ] 移动端适配正常
- [ ] 构建无警告/错误

---

## 七、多语言支持

### 7.1 目录结构

```
src/content/docs/
├── zh-cn/              # 简体中文（默认）
│   ├── index.mdx
│   └── concepts/
└── en/                 # 英文
    ├── index.mdx
    └── concepts/
```

或使用 Starlight 的翻译机制：

```
src/content/docs/
├── index.mdx           # 默认语言
├── concepts/
└── en/                 # 翻译
    ├── index.mdx
    └── concepts/
```

### 7.2 翻译优先级

1. 首页
2. 快速开始
3. 核心概念
4. FAQ
5. 其他教程（按需）

---

## 八、部署配置

### 8.1 GitHub Pages

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v2
        with:
          path: ./dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v2
        id: deployment
```

### 8.2 Vercel / Netlify

无需额外配置，直接连接 GitHub 仓库即可自动部署。

---

## 九、维护与更新

### 9.1 版本管理

- 使用 Git tag 管理文档版本
- 主要版本发布时归档旧版本文档
- 在文档中标注适用的框架版本

### 9.2 持续更新

- 监听 go-zero 主仓库的 Release
- 同步更新 Changelog
- 更新受影响的 API 文档

---

## 附录

### A. 常用组件

Starlight 内置组件使用示例：

```mdx
import { Tabs, TabItem, Card, CardGrid, Aside } from '@astrojs/starlight/components';

<Aside type="tip">
提示内容
</Aside>

<Tabs>
  <TabItem label="Go">Go 代码</TabItem>
  <TabItem label="API">API 定义</TabItem>
</Tabs>

<CardGrid>
  <Card title="功能一" icon="rocket">说明</Card>
  <Card title="功能二" icon="star">说明</Card>
</CardGrid>
```

### B. 图标参考

Starlight 支持的图标：https://starlight.astro.build/reference/icons/

### C. 参考文档

- [Starlight 官方文档](https://starlight.astro.build/)
- [Astro 官方文档](https://docs.astro.build/)
- [go-zero 官方文档源码](https://github.com/zeromicro/go-zero.dev)
