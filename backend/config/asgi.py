"""
ASGI 入口配置文件

用于在 ASGI 兼容的 Web 服务器上部署 Django 项目。
支持异步操作。
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
