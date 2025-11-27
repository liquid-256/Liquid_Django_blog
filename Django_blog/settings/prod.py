"""
生产环境配置。

特点：
- DEBUG = False
- 通过环境变量配置 ALLOWED_HOSTS
- 强制开启安全相关 Cookie 选项（可通过环境变量微调）
"""

from .base import *  # noqa

from decouple import config, Csv

DEBUG = False

# 如：BLOG_ALLOWED_HOSTS=example.com,www.example.com
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="example.com", cast=Csv())

# 在 HTTPS 部署下建议保持为 True，如在纯 HTTP 测试环境可通过环境变量关闭
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=True, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)

# 推荐设置，防止跨站点请求伪造
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="https://example.com",
    cast=Csv(),
)



