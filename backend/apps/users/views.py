"""
users/views.py
=============
用户注册、登录、用户信息视图。
"""
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer


def build_response(code=0, message="", data=None):
    """统一响应格式"""
    return Response({
        "code": code,
        "message": message,
        "data": data
    })


class RegisterView(APIView):
    """用户注册"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return build_response(
                code=0,
                message="注册成功",
                data={"id": user.id, "username": user.username}
            )
        # 收集第一个错误信息
        first_field = next(iter(serializer.errors))
        first_error = serializer.errors[first_field][0]
        return build_response(
            code=1,
            message=str(first_error),
            data=serializer.errors
        )


class LoginView(APIView):
    """用户登录，返回 JWT token"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return build_response(code=1, message="用户名和密码不能为空")

        user = authenticate(username=username, password=password)
        if not user:
            return build_response(code=1, message="用户名或密码错误")

        refresh = RefreshToken.for_user(user)
        return build_response(
            code=0,
            message="登录成功",
            data={
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {"id": user.id, "username": user.username}
            }
        )


class MeView(APIView):
    """获取当前登录用户信息"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return build_response(code=0, message="获取成功", data=serializer.data)
