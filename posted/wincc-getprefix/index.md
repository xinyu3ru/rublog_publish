---
author: xinyu2ru
categories:
- software
date: 2026-03-19 17:27:00
excerpt: 西门子 wincc 获取画面的前缀
focus-keywords: wincc
guid: https://www.rxx0.com/wp-json/wp/v2/posts/4278
image: images/banner.jpg
og:
  image: images/og-banner.jpg
slug: xi-men-zi-wincc-huo-qu-hua-mian-de-qian-zhui
status: publish
tags: ''
title: 西门子 wincc 获取画面的前缀
---

使用 Wincc 做画面的时候，有些画面可以复用，当使用复用画面的时候，wincc 通常是通过脚本添加前缀。

调试过程中，我们有时候需要判断我们的前缀是否正确，下面的代码可以显示当前页面的前缀。

``` wincc 显示当前页面前缀
#include "apdefap.h"
void OnClick(char* lpszPictureName, char*lpszObjectName, char* lpszPropertyName)
{
char Name[20];
HWND hwnd=NULL;

hwnd=FindWindow(NULL,"WinCC-运行系统 -"); //获得句柄
strcpy(Name,GetPropChar(GetParentPicture(lpszPictureName),GetParentPictureWindow(lpszPictureName),"TagPrefix")); //Return-Type: char*

MessageBox(hwnd,Name,"OK",MB_OK);
}
```

还可以使用 ANSI C 的一些函数拼接变量名，比如

C脚本中获得一个画面lpszPictureName中画面窗口lpszObjectName的变量前缀使用以下函数

拼接字符串使用strcat函数

``` 拼接函数
char* GetTagPrefix(LPCTSTR lpszPictureName, LPCTSTR lpszObjectName);
char str[100];
strcat(str,strat(tag1,"run"));
```