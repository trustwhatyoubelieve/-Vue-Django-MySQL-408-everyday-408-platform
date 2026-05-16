"""
URL 根配置文件

项目所有 URL 路由的入口点。
后续各个 app 的路由会包含进来。
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.views import APIView
from rest_framework.response import Response


class HealthView(APIView):
    """健康检查接口"""
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({
            'code': 0,
            'message': 'backend is running'
        })


urlpatterns = [
    path('admin/', admin.site.urls),

    # 健康检查接口
    path('api/health/', HealthView.as_view(), name='health'),

    # API 路由
    path('api/users/', include('apps.users.urls')),            # 用户模块
    path('api/question-bank/', include('apps.question_bank.urls')),  # 题库模块
    path('api/practice/', include('apps.practice.urls')),      # 练习模块
    path('api/records/', include('apps.records.urls')),       # 学习记录模块（错题本/收藏夹）
    # path('api/recommendation/', include('apps.recommendation.urls')),
    path('api/recommendations/', include('apps.recommendation.urls')),  # 智能推荐模块
]

# 开发环境下，添加媒体文件的访问路由
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
