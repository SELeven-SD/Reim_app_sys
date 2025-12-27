# 报销管理系统

一个基于 Django + Vue.js 的企业报销管理系统，支持员工提交报销申请、上传发票PDF、管理员审核等功能。

## 技术栈

### 后端
- Python 3.12
- Django 6.0
- Django REST Framework 3.16
- djangorestframework-simplejwt 5.5
- Gunicorn 23.0

### 前端
- Vue 3.5
- Vue Router 4.5
- Axios 1.10
- Vite 7.0

### 部署
- Nginx 1.24
- Ubuntu 24.04

## 功能特性

### 用户功能
- ✅ 用户注册与登录（JWT认证）
- ✅ 提交报销申请（支持上传PDF发票，最大50MB）
- ✅ 查看个人申请记录
- ✅ 重新提交被驳回的申请
- ✅ 查看系统公告通知

### 管理员功能
- ✅ 审核报销申请（通过/驳回）
- ✅ 批量下载已审核发票（ZIP打包）
- ✅ 导出申请记录到Excel
- ✅ 删除未审核申请
- ✅ 删除PDF文件
- ✅ 发布系统公告
- ✅ 用户权限管理（只有超级用户和staff用户可访问后台）

### UI特性
- 🎨 现代渐变紫色主题设计
- 📱 响应式布局
- ✨ 流畅的动画效果
- 🔔 系统公告实时显示

## 项目结构

```
app_bx/
├── reimbursement-backend/     # Django后端
│   ├── manage.py
│   ├── requirements.txt
│   ├── reimbursement/         # 核心应用
│   │   ├── models.py          # 数据模型
│   │   ├── views.py           # API视图
│   │   ├── serializers.py     # 序列化器
│   │   ├── admin.py           # 管理后台
│   │   └── urls.py
│   └── reimbursement_system/  # 项目配置
│       └── settings.py
│
└── reimbursement-frontend/    # Vue前端
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.vue            # 根组件
        ├── main.js
        ├── router/            # 路由配置
        ├── views/             # 页面组件
        └── components/        # 可复用组件
```

## 部署说明

### 环境要求
- Python 3.12+
- Node.js 16+
- Nginx
- SQLite（或PostgreSQL/MySQL）

### 后端部署

1. 创建虚拟环境并安装依赖：
```bash
cd reimbursement-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. 配置环境变量（创建.env文件）：
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-server-ip,localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

3. 执行数据库迁移：
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. 收集静态文件：
```bash
python manage.py collectstatic
```

5. 启动Gunicorn：
```bash
gunicorn --bind 0.0.0.0:8000 reimbursement_system.wsgi:application
```

### 前端部署

1. 安装依赖：
```bash
cd reimbursement-frontend
npm install
```

2. 构建生产版本：
```bash
npm run build
```

3. 配置Nginx：
```nginx
server {
    listen 80;
    server_name your-server-ip;
    client_max_body_size 50M;

    location / {
        root /path/to/reimbursement-frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /admin {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /media {
        alias /path/to/reimbursement-backend/media;
    }
}
```

## 开发指南

### 本地开发

后端：
```bash
cd reimbursement-backend
source venv/bin/activate
python manage.py runserver
```

前端：
```bash
cd reimbursement-frontend
npm run dev
```

### API端点

- `POST /api/register/` - 用户注册
- `POST /api/token/` - 获取JWT token
- `GET/POST /api/reimbursements/` - 获取/创建报销申请
- `GET/PUT/DELETE /api/reimbursements/<id>/` - 操作单个申请
- `GET /api/reimbursements/notices/` - 获取系统公告

## 许可证

MIT License

## 作者

项目开源于 2025年12月
