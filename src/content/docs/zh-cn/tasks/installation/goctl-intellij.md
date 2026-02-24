---
title: GoLand 插件
description: 安装并使用 JetBrains GoLand 的 goctl 插件。
sidebar:
  order: 6

---

import DocsButton from '@components/page/native/DocsButton';

## 概述

goctl-intellij 是 go-zero api 描述语言的 intellij 编辑器插件，支持 api 描述语言高亮、语法检测、快速提示、创建模板特性。

项目地址：https://github.com/zeromicro/goctl-intellij

## 安装

goctl-intellij 安装方式有 2 种

- 从磁盘安装
- intellij 插件中心安装

### 1. 从磁盘安装

<div>
    <img src="/logos/logo.svg" class="cordova-ee-img" />
    <p>
      intellij 最低版本要求： 193.0（2019.3）
      安装包大小： 6.55MB
    </p>
    <DocsButton className="native-ee-detail">点击下载</DocsButton>
  </div>

下载的 zip 文件无需解压，然后打开 `Goland` | `Preferences...` | `Plugins`，找到更多图标 <IconMoreVertical />，选择 `Install Plugin from Disk...`

![goland plugin center](/resource/tasks/installation/goland-plugin.png)

### 2. 从插件中心安装

打开 `Goland` | `Preferences...` | `Plugins`，选中 `Marketplace` 选项栏，在搜索框输入 `Goctl` 进行搜索安装

![goland plugin goctl](/resource/tasks/installation/goland-plugin-goctl.png)
