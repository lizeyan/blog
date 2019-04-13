---
title: log format of nginx
categories:
  - nginx
---

In `nginx.conf`, we define a `log_format` called `postdata`:

```
http {
    log_format postdata '{"ts": "$time_iso8601", "status": $status, "req": "$uri", "method": "$request_method", "body": "$request_body"}';
    # ...... other content
}
```

In site configuration, like `site-enabled/default`:

```
server {
        access_log /var/log/nginx/access.log postdata;
        # ...... other content
}
```



