"""
保留旧 settings.py 以兼容可能的导入，但实际不再使用。

推荐在开发环境使用：
    DJANGO_SETTINGS_MODULE=Django_blog.settings.dev

生产环境使用：
    DJANGO_SETTINGS_MODULE=Django_blog.settings.prod
"""

from .settings.dev import *  # noqa