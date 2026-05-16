"""
users/urls.py
============
用户模块 URL 配置。
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MeView, RegisterView, LoginView
from .views_health import HealthView

urlpatterns = [
    # 健康检查
    path("health/", HealthView.as_view(), name="health"),
    # 用户相关
    path("users/register/", RegisterView.as_view(), name="user-register"),
    path("users/login/", LoginView.as_view(), name="user-login"),
    path("users/me/", MeView.as_view(), name="user-me"),
    # simplejwt 标准刷新接口
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
