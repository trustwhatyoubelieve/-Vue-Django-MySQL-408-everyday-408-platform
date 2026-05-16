"""
健康检查接口

提供系统健康状态的简单检测接口。
"""
from rest_framework.views import APIView
from rest_framework.response import Response


class HealthView(APIView):
    """
    健康检查接口

    GET /api/health/
    返回系统运行状态
    """
    authentication_classes = []  # 不需要认证
    permission_classes = []     # 不需要权限

    def get(self, request):
        return Response({
            'code': 0,
            'message': 'backend is running'
        })
