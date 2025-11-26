"""
开发环境配置。

特点：
- DEBUG = True
- 允许本机访问
"""

from .base import *  # noqa

from decouple import config, Csv

DEBUG = True

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost",
    cast=Csv()
)

SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, cast=bool)