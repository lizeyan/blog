---
title: How did I build this website
date: 2016-07-24 11:41:37
tags: ["Github Pages", "Hexo"]
---
本文介绍我是如何搭建这个博客的。
运行环境是Windows10，但是我使用[Babun][Babun]从而能够直接运行大部分linux命令。

<!-- more -->

1. Github Page
首先你需要一个[GitHub Page][gpage]。
这是Github提供的网站主机服务，你可以为个人，组织或者某个工程建议基于git repo的网站。有很多知名的组织和工程都用[GitHub Page][gpage]制作了主页:
    - [Microsoft][Microsoft]
    - [Google][Google]
    - [Git][Git]
    - [Babun][Babun]
    - [Git For Windows][Git For Windows]
只需要在GitHub上新建一个以 name.github.io 命名的repo即可，name可以自行定义。

2. Hexo
然后使用[Hexo][hexo]搭建博客网站。Hexo是一个简洁的博客框架，容易上手。

    1. 安装Git
    [Git For Windows][Git For Windows]
    2. 安装Node.js
    [Node.js主页][Node.js]
    3. 安装Hexo
    在命令行中执行
    ``` bash
    $ npm install -g hexo-cli
    ```

3. 配置
    安装完成后，执行：
    ``` bash
    $ hexo init <folder>
    $ cd <folder>
    $ npm install
    ```
    <folder>最好是一个空文件夹，它将是你网站的根目录。

    打开 /_config.yml 进行配置，各种选项参阅 [Hexo配置](https://hexo.io/zh-cn/docs/configuration.html)。这里主要讲一下关于部署的配置。
    首先安装[hexo-deployer-git][hexo-deployer-git], 执行
    ``` bash
    $ npm install hexo-deployer-git --save
    ```

    然后在 /_config.yml中修改 deploy配置：
    ```
    deploy:
    type: git
    repo: <repository url>
    branch: [branch]
    message: [message]
    ```
    branch和message可以不写，在GitHub上branch会自动检测。

4. 运行
    部署到[GitHub Page][gpage]上，需要执行
    ``` bash
    $ hexo deploy
    ```
    完成之后在浏览器中访问name.github.io就可以看到你的网站。

    在本地测试的话执行
    ``` bash
    $ hexo server
    ```
    开启之后访问localhost:4000。

5. 修改主题
    在这里有大量的[主题](https://hexo.io/themes/)。
    使用别人的主题只需要在 /themes 下执行
    ``` bash
    $ git clone repo_url
    ```
    然后在/_config.yml中修改theme选项即可。







[gpage]: https://pages.github.com/ "GitHub Page"
[hexo]: https://hexo.io/zh-cn/index.html "Hexo"
[Microsoft]: (https://microsoft.github.io/ "Microsoft"
[Google]: https://github.com/google "Google"
[Git]: https://git.github.io/ "Git"
[Babun]: http://babun.github.io/ "Babun"
[Git For Windows]: https://git-for-windows.github.io/ "Git For Windows"
[Node.js]: https://nodejs.org/en/ "Node.js"
[hexo-deployer-git]: https://github.com/hexojs/hexo-deployer-git "hexo-deployer-git"