---
title: Install Homebrew
categories:
  - macOS
---

在国内用homebrew默认的安装会比较慢

``` bash
cd ~
curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install >> brew_instal
vim ~/brew_install
```

对应行修改为：

```
BREW_REPO = "https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git".freeze
CORE_TAP_REPO = "https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git".freeze
```

然后安装完之后

```bash
cd "$(brew --repo)"
git remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git

cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git

brew update
```

