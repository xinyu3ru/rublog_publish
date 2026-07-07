---
author: xinyu2ru
categories:
- jinzhan
date: 2026-07-07 18:20:00
image: images/banner.jpg
og:
  image: images/og-banner.jpg
status: publish
tags: AI
focus-keywords: AI
title: 对不起 Trae 
excerpt: 对不起 Trae 
---

# 对不起 Trae 

我使用 github 推送 md 文档到 WordPress 发布文章。

前段时间服务器到期，我就把网站重构了一下，删除了以前的一些文章，特别是阅读量比较小的文章。

重构的时候是选择的重新安装 WordPress ，结果导致之前给 github 开的账号和授权密码丢失了

最近发文章的时候一直发布不成功，我就认为发布文章的库又失效了或者什么原因导致失败，我就让 Trae 使用 AI 帮我修改代码。

结果 Trae 修改了一天多，我在今天下午突然意识到，是不是 log 中的账号认证失败/没有发布权限，是真的没有权限呢？

再仔细一想，嗯，确定了，不是库的问题，不是什么问题，就是发布账号的授权密码没有了。

登录后台，再次授权，把授权更新到 github 中。

运行 actions 发布，哈哈，发布成功了。

对不起 Trae 这么了你一天多，竟然是因为没有授权密码。不是你代码修改的不好，也不是你找不到原因

是我的错，真的对不起~
