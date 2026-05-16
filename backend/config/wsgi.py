"""
WSGI 入口配置文件

用于在 WSGI 兼容的 Web 服务器上部署 Django 项目。
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
