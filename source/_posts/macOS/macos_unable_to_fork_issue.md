---
title: macOS Catalina unable to fork issue
categories:
  - macOS
---

在macOS X Catalina上，cron进程无法被正常关闭。因为有一个每分钟运行一次的cron job，所有很快就会积累很多进程，超过的系统的最大进程限制。

cron进程无法关闭似乎和读写文件有关，将每个cron进程的输出重定向到`/dev/null`即可

```bash
/Users/lizytalk/Projects/blog/keep.sh &> /dev/null
```

