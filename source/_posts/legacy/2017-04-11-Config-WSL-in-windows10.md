---
title: Config WSL in windows10
date: 2017-04-11 15:40:42
tags: ["WSL", "Windows10"]
---

配置WSL，使得能够在WSL上运行图形程序，以及使用一个更加科学的终端模拟器

<!--more-->

# WSL-Terminal

首先是使用一个更加科学的终端模拟器，因为自带的cmd太烂了。

[wsl-terminal](https://github.com/goreliu/wsl-terminal)是一个开源项目，目标是为WSL写一个好用的终端模拟器。这个项目的做法似乎是打开一个隐藏的cmd，在WSL中运行`opensshd`，然后再通过`ssh`连接。

其他的比如`cmder`, `babun`, `con-emu`似乎支持WSL，not sure。

如果将WSL-Terminal的启动程序`open-wsl.exe`直接添加到开始菜单，会使得每次运行之后进入的是WSL-Terminal的目录。我的解决办法是在`.bashrc`中添加下面一段:

``` bash
if [ $(pwd) = "/mnt/c/Users/lizeyan/Downloads/wsl-terminal" ]; then
    cd ~
fi
```



# Run Graphic Program

WSL默认是没有显示设备的，这个时候运行不了图形界面的程序。

`Xming`是一个在Windows上运行X Server的程序，下载安装之后就有了一个Linux支持的显示设备。

然后在WSL中运行:

``` bash
export DISPLAY=:0
```

或者将这一句加到`.bashrc`/`.zshrc`中

然后就可以运行大多数的图形界面程序了
