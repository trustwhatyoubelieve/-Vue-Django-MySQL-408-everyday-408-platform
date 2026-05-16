"""
Django 主配置文件

本项目采用拆分式配置，将不同类型的配置分开管理。
当前阶段以清晰能跑为主，不过度设计。
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

from datetime import timedelta

# ==================== 基础路径配置 ====================
# 项目根目录 (backend/)
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================== 安全配置 ====================
# SECRET_KEY 用于加密签名，请在生产环境中使用环境变量
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# DEBUG 模式，生产环境务必设为 False
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

# 允许访问的域名列表
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ==================== 应用配置 ====================
# 已安装的应用
INSTALLED_APPS = [
    # Django 内置应用
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 第三方应用
    'rest_framework',          # Django REST Framework
    'corsheaders',             # 跨域支持

    # 本地应用 (apps 下的应用)
    'apps.users',
    'apps.question_bank',
    'apps.practice',
    'apps.records',
    'apps.recommendation',
]

# ==================== 中间件配置 ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 跨域中间件
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==================== URL 配置 ====================
ROOT_URLCONF = 'config.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 配置
WSGI_APPLICATION = 'config.wsgi.application'

# ==================== 数据库配置 ====================
# MySQL 数据库配置
# 请修改以下占位符为你的实际数据库信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', '408_everyday'),      # 数据库名
        'USER': os.environ.get('DB_USER', 'root'),      # 数据库用户名
        'PASSWORD': os.environ.get('DB_PASSWORD', '123456'),  # 数据库密码
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),          # 数据库主机
        'PORT': os.environ.get('DB_PORT', '3306'),               # 数据库端口
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# ==================== 密码验证 ====================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==================== 国际化配置 ====================
# 语言代码 - 简体中文
LANGUAGE_CODE = 'zh-hans'

# 时区 - 中国上海
TIME_ZONE = 'Asia/Shanghai'

# 是否使用 UTC 时间
USE_I18N = True
USE_TZ = True

# ==================== 静态文件配置 ====================
# 静态文件 (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 额外静态文件目录
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# ==================== 媒体文件配置 ====================
# 用户上传的文件
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==================== 跨域配置 ====================
# 允许所有域名访问 API (开发环境使用)
# 生产环境请改为具体的前端域名
CORS_ALLOW_ALL_ORIGINS = True

# 或者指定允许的域名
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:5173',
#     'http://127.0.0.1:5173',
# ]

# ==================== DRF 配置 ====================
REST_FRAMEWORK = {
    # 默认的渲染器
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # 默认的分页器
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # 默认的权限类
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # 异常处理 (后续可扩展)
    # 'EXCEPTION_HANDLER': 'utils.exceptions.custom_exception_handler',
}

# ==================== JWT 配置 ====================
SIMPLE_JWT = {
    # Access Token 有效期（必须是 timedelta 对象）
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    # Refresh Token 有效期（必须是 timedelta 对象）
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    # Token 前缀
    'AUTH_HEADER_PREFIX': 'Bearer',
    # Token 类型
    'TOKEN_TYPE': 'access',
    # 是否启用旋转刷新令牌
    'ROTATE_REFRESH_TOKENS': False,
    # 是否将刷新令牌加入黑名单
    'BLACKLIST_AFTER_ROTATION': False,
}

# ==================== 默认主键字段类型 ====================
# 使用 BigAutoField 生成较长的主键
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
