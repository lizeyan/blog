---
categories:
  - Proxmox Virtual Environment
title: Unable to Access Host via PVE API
---
## Issue

Host is alive and accessible, but all vm states are not accessable, and web GUI is not accessable either.

I can ssh to this host.

``` bash
lsof -i :8006
# there are processes listening on it
```

``` bash
curl -s -k https://localhost:8006
# nothing respond
```

``` bash
tail /var/log/pveproxy/access.log
# nothing
```

## Solution

``` bash
service pve-cluster restart
```





