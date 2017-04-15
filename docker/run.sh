#!/bin/bash

nohup mysqld & /usr/local/openresty/nginx/sbin/nginx -p /opt/stock/ngx-runtime/ -c /opt/stock/ngx-runtime/conf/nginx.conf &
/opt/stock/venv/bin/python /opt/stock/run_with_tornado.py >/var/log/stock/stock-stdout.log 2>/var/log/stock/stock-stderr.log