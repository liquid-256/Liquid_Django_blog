"""
Gunicorn 配置文件（仅用于 Linux / 服务器环境）。

使用方式（示例）：

    gunicorn -c gunicorn_conf.py a_Django_blog.wsgi:application

在启动前请确保已设置：
    export DJANGO_SETTINGS_MODULE=a_Django_blog.settings.prod
    export DJANGO_SECRET_KEY='your-secret-key'
"""

import multiprocessing
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Django WSGI 模块
wsgi_app = "a_Django_blog.wsgi:application"

# 绑定地址（建议在宝塔 / Nginx 中做反向代理）
bind = "0.0.0.0:8000"

# 工作进程数：CPU * 2 + 1
workers = multiprocessing.cpu_count() * 2 + 1

# 每个 worker 的线程数
threads = 2

# 使用的 worker 类型，部署 Django 一般使用 sync
worker_class = "sync"

# 超时时间，秒
timeout = 30

# 日志配置
accesslog = os.path.join(BASE_DIR, "logs", "gunicorn_access.log")
errorlog = os.path.join(BASE_DIR, "logs", "gunicorn_error.log")
loglevel = "info"


