# 408 刷题系统

基于 Vue 3 + Django + MySQL 的 408 刷题系统

## 项目目录结构

```
408-Everyday/
├── backend/                          # Django 后端
│   ├── config/                       # 项目配置包
│   │   ├── __init__.py
│   │   ├── settings.py               # 主配置文件
│   │   ├── urls.py                   # URL 路由配置
│   │   ├── wsgi.py                   # WSGI 入口
│   │   └── asgi.py                   # ASGI 入口
│   ├── apps/                         # 应用模块
│   │   ├── __init__.py
│   │   ├── users/                    # 用户模块
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── admin.py
│   │   │   ├── models.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   └── views_health.py       # 健康检查接口
│   │   ├── question_bank/            # 题库模块
│   │   ├── practice/                 # 练习模块
│   │   ├── records/                  # 学习记录模块
│   │   └── recommendation/           # 推荐模块
│   ├── utils/                        # 工具包
│   ├── scripts/                      # 脚本目录
│   ├── media/                        # 媒体文件目录
│   ├── static/                       # 静态文件目录
│   ├── requirements.txt              # Python 依赖
│   └── manage.py                     # Django 管理脚本
│
├── frontend/                         # Vue 3 前端
│   ├── src/
│   │   ├── api/                      # API 接口
│   │   │   ├── index.js              # 接口导出
│   │   │   └── request.js            # Axios 封装
│   │   ├── router/                   # 路由配置
│   │   │   └── index.js
│   │   ├── stores/                   # Pinia 状态管理
│   │   │   └── user.js
│   │   ├── views/                    # 页面组件
│   │   │   ├── HomeView.vue          # 首页
│   │   │   ├── LoginView.vue         # 登录页
│   │   │   └── RegisterView.vue      # 注册页
│   │   ├── components/               # 公共组件
│   │   │   └── Layout.vue            # 基础布局
│   │   ├── assets/                   # 静态资源
│   │   │   └── main.css
│   │   ├── utils/                    # 工具函数
│   │   ├── App.vue                   # 根组件
│   │   └── main.js                  # 入口文件
│   ├── public/                       # 公共静态资源
│   ├── index.html                    # HTML 模板
│   ├── vite.config.js                # Vite 配置
│   └── package.json                  # NPM 依赖
│
└── README.md                          # 项目说明
```

## 后端启动步骤

### 1. 创建虚拟环境

```bash
cd 408-Everyday/backend

# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置数据库

在启动前，请修改 `backend/config/settings.py` 中的数据库配置，或设置环境变量：

```bash
# 设置数据库环境变量 (Windows PowerShell)
$env:DB_NAME="408_everyday"
$env:DB_USER="your_username"
$env:DB_PASSWORD="your_password"
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"

# 或者使用 set 命令 (Windows CMD)
set DB_NAME=408_everyday
set DB_USER=root
set DB_PASSWORD=your_password
```

**数据库配置说明：**
- 确保 MySQL 服务已启动
- 创建名为 `408_everyday` 的数据库（使用 utf8mb4 编码）
- 修改上述环境变量为你的实际数据库信息

### 4. 数据库迁移

```bash
cd 408-Everyday/backend
python manage.py migrate
```

### 5. 启动后端服务

```bash
python manage.py runserver 0.0.0.0:8000
```

后端启动成功后，访问 http://127.0.0.1:8000/api/health/ 应返回：

```json
{
  "code": 0,
  "message": "backend is running"
}
```

## 前端启动步骤

### 1. 安装依赖

```bash
cd 408-Everyday/frontend
npm install
```

### 2. 启动前端开发服务器

```bash
npm run dev
```

前端启动成功后，访问 http://localhost:5173/

## 联调验证步骤

1. 确保后端服务运行在 http://127.0.0.1:8000
2. 确保前端服务运行在 http://localhost:5173
3. 在浏览器打开前端首页 http://localhost:5173/
4. 页面会显示"后端连接状态"，如果后端正常，会显示绿色的"后端运行正常 - backend is running"

## 技术栈说明

### 后端
- **Django 4.2+**: Python Web 框架
- **Django REST Framework**: RESTful API 开发
- **django-cors-headers**: 跨域资源共享支持
- **mysqlclient**: MySQL 数据库驱动

### 前端
- **Vue 3**: 渐进式 JavaScript 框架
- **Vite**: 新一代前端构建工具
- **Vue Router 4**: Vue.js 官方路由管理
- **Pinia**: Vue.js 状态管理库
- **Axios**: HTTP 请求库

## 后续开发

当前阶段仅完成项目骨架初始化，包含：
- 健康检查接口 (`/api/health/`)
- 基础页面路由 (`/`, `/login`, `/register`)

后续可按需开发：
1. 用户注册与登录（集成 JWT）
2. 题库管理（CRUD）
3. 在线练习与判题
4. 错题本与收藏夹
5. 学习记录与统计
6. 智能推荐功能
7. 管理员后台

## 注意事项

1. **数据库配置**: 首次启动前必须配置正确的 MySQL 连接信息
2. **跨域问题**: 后端已配置 `cors-headers`，开发环境下允许所有源
3. **生产环境**: 上线前请修改 `settings.py` 中的：
   - `DEBUG = False`
   - `SECRET_KEY` 使用安全的随机密钥
   - `ALLOWED_HOSTS` 设置为实际域名
   - `CORS_ALLOW_ALL_ORIGINS = False` 并指定具体域名
