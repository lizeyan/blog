---
title: Install supervisor via brew
categories:
  - macOS
---

## Install brew

Google it.

## Install brew services

``` bash
brew services
```

## Install supervisor

``` bash
brew install supervisor
```

## Configuration

`/usr/local/etc/supervisord.ini`

```
;[unix_http_server]
;file=/usr/local/var/run/supervisor.sock   ; the path to the socket file
;chmod=0700                 ; socket file mode (default 0700)
;chown=nobody:nogroup       ; socket file uid:gid owner
;username=user              ; default is no username (open server)
;password=123               ; default is no password (open server)

[inet_http_server]         ; inet (TCP) server disabled by default
port=*:9001                 ; ip_address:port specifier, *:port for all iface
;username=user              ; default is no username (open server)
;password=123               ; default is no password (open server)

[supervisorctl]
;serverurl=unix:///usr/local/var/run/supervisor.sock ; use a unix:// URL  for a unix socket
serverurl=http://127.0.0.1:9001 ; use an http:// url to specify an inet socket
;username=chris              ; should be same as in [*_http_server] if set
;password=123                ; should be same as in [*_http_server] if set
;prompt=mysupervisor         ; cmd line prompt (default "supervisor")
;history_file=~/.sc_history  ; use readline history if available
```

