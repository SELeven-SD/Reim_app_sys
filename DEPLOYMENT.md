# 报销管理系统部署指南

## 部署架构

- **后端**: Django + Gunicorn
- **前端**: Vue 3 + Vite (构建为静态文件)
- **Web服务器**: Nginx
- **数据库**: PostgreSQL 或 MySQL
- **操作系统**: Linux (Ubuntu/CentOS)

---

## 一、服务器准备

### 1. 更新系统
```bash
sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
# 或
sudo yum update -y  # CentOS/RHEL
```

### 2. 安装必要软件
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib -y

# CentOS/RHEL
sudo yum install python3 python3-pip nginx postgresql-server postgresql-contrib -y
```

### 3. 安装 Node.js (用于构建前端)
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs  # Ubuntu
# 或
sudo yum install -y nodejs  # CentOS
```

---

## 二、部署后端

### 1. 上传代码到服务器
```bash
# 在本地执行
scp -r /home/lionp/app_bx/reimbursement-backend user@your-server-ip:/var/www/

# 或使用 git
ssh user@your-server-ip
cd /var/www/
git clone your-repository-url reimbursement-backend
```

### 2. 创建虚拟环境并安装依赖
```bash
cd /var/www/reimbursement-backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install python-decouple dj-database-url
```

### 3. 配置环境变量
```bash
# 创建 .env 文件
cat > .env << 'EOF'
SECRET_KEY=your-very-long-random-secret-key-here-change-this
DEBUG=False
DATABASE_URL=postgresql://db_user:db_password@localhost:5432/reimbursement_db
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip
EOF

# 生成安全的 SECRET_KEY
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# 将生成的key替换到 .env 文件中
```

### 4. 配置数据库

#### PostgreSQL
```bash
# 切换到 postgres 用户
sudo -u postgres psql

# 在 PostgreSQL 中执行
CREATE DATABASE reimbursement_db;
CREATE USER db_user WITH PASSWORD 'db_password';
ALTER ROLE db_user SET client_encoding TO 'utf8';
ALTER ROLE db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE db_user SET timezone TO 'Asia/Shanghai';
GRANT ALL PRIVILEGES ON DATABASE reimbursement_db TO db_user;
\q
```

#### MySQL (可选)
```bash
sudo mysql
CREATE DATABASE reimbursement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'db_user'@'localhost' IDENTIFIED BY 'db_password';
GRANT ALL PRIVILEGES ON reimbursement_db.* TO 'db_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 修改 .env 中的 DATABASE_URL
# DATABASE_URL=mysql://db_user:db_password@localhost:3306/reimbursement_db
```

### 5. 修改 settings.py
```bash
nano /var/www/reimbursement-backend/reimbursement_system/settings.py
```

更新以下内容：
```python
# 添加到文件开头
import os

# 修改 ALLOWED_HOSTS
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# 添加 CORS 支持（如果前后端分离）
INSTALLED_APPS = [
    # ... 其他应用
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 静态文件服务
    'corsheaders.middleware.CorsMiddleware',  # CORS
    # ... 其他中间件
]

# CORS 设置
CORS_ALLOWED_ORIGINS = [
    "https://your-domain.com",
    "https://www.your-domain.com",
]

# 静态文件配置（使用 WhiteNoise）
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 安全设置
SECURE_SSL_REDIRECT = True  # 强制 HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 6. 安装额外依赖
```bash
pip install corsheaders whitenoise
```

### 7. 迁移数据库
```bash
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # 创建管理员账户
python manage.py collectstatic --noinput
```

### 8. 配置 Gunicorn
```bash
# 创建 Gunicorn 配置文件
cat > gunicorn_config.py << 'EOF'
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
max_requests = 1000
timeout = 30
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
EOF

# 创建日志目录
sudo mkdir -p /var/log/gunicorn
sudo chown -R $USER:$USER /var/log/gunicorn
```

### 9. 创建 Systemd 服务
```bash
sudo nano /etc/systemd/system/reimbursement.service
```

添加以下内容：
```ini
[Unit]
Description=Reimbursement System Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/reimbursement-backend
Environment="PATH=/var/www/reimbursement-backend/venv/bin"
ExecStart=/var/www/reimbursement-backend/venv/bin/gunicorn \
    --config /var/www/reimbursement-backend/gunicorn_config.py \
    reimbursement_system.wsgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl start reimbursement
sudo systemctl enable reimbursement
sudo systemctl status reimbursement
```

---

## 三、部署前端

### 1. 上传前端代码
```bash
# 在本地或服务器上
cd /var/www/
# 如果已上传，跳过这步
```

### 2. 配置 API 地址
```bash
cd /var/www/reimbursement-frontend
nano vite.config.js
```

添加代理配置：
```javascript
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

### 3. 构建前端
```bash
cd /var/www/reimbursement-frontend
npm install
npm run build

# 构建后的文件在 dist/ 目录
```

---

## 四、配置 Nginx

### 1. 创建 Nginx 配置文件
```bash
sudo nano /etc/nginx/sites-available/reimbursement
```

添加以下配置：
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL 证书配置（使用 Let's Encrypt）
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # 前端静态文件
    location / {
        root /var/www/reimbursement-frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 10M;  # 允许上传大文件
    }

    # Django Admin
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态文件（Django）
    location /static/ {
        alias /var/www/reimbursement-backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 媒体文件（上传的发票）
    location /media/ {
        alias /var/www/reimbursement-backend/media/;
        expires 30d;
    }

    # 安全头
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # 日志
    access_log /var/log/nginx/reimbursement_access.log;
    error_log /var/log/nginx/reimbursement_error.log;
}
```

### 2. 启用站点
```bash
sudo ln -s /etc/nginx/sites-available/reimbursement /etc/nginx/sites-enabled/
sudo nginx -t  # 测试配置
sudo systemctl restart nginx
```

### 3. 配置 SSL 证书（使用 Let's Encrypt）
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
sudo certbot renew --dry-run  # 测试自动续期
```

---

## 五、设置文件权限

```bash
# 设置目录权限
sudo chown -R www-data:www-data /var/www/reimbursement-backend
sudo chmod -R 755 /var/www/reimbursement-backend

# 确保 media 目录可写
sudo chmod -R 775 /var/www/reimbursement-backend/media
sudo chown -R www-data:www-data /var/www/reimbursement-backend/media
```

---

## 六、防火墙配置

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable

# Firewalld (CentOS)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## 七、监控和维护

### 1. 查看日志
```bash
# Gunicorn 日志
tail -f /var/log/gunicorn/access.log
tail -f /var/log/gunicorn/error.log

# Nginx 日志
tail -f /var/log/nginx/reimbursement_access.log
tail -f /var/log/nginx/reimbursement_error.log

# Systemd 日志
sudo journalctl -u reimbursement -f
```

### 2. 重启服务
```bash
sudo systemctl restart reimbursement  # 后端
sudo systemctl restart nginx          # Nginx
```

### 3. 数据库备份
```bash
# PostgreSQL
pg_dump -U db_user reimbursement_db > backup_$(date +%Y%m%d).sql

# MySQL
mysqldump -u db_user -p reimbursement_db > backup_$(date +%Y%m%d).sql

# 设置自动备份 (crontab)
crontab -e
# 添加: 0 2 * * * /path/to/backup-script.sh
```

---

## 八、快速部署脚本

创建一个自动化部署脚本：

```bash
cat > deploy.sh << 'EOF'
#!/bin/bash
set -e

echo "=== 开始部署 ==="

# 1. 拉取最新代码
cd /var/www/reimbursement-backend
git pull origin main

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 安装/更新依赖
pip install -r requirements.txt

# 4. 数据库迁移
python manage.py migrate

# 5. 收集静态文件
python manage.py collectstatic --noinput

# 6. 重启 Gunicorn
sudo systemctl restart reimbursement

# 7. 部署前端
cd /var/www/reimbursement-frontend
git pull origin main
npm install
npm run build

# 8. 重启 Nginx
sudo systemctl reload nginx

echo "=== 部署完成 ==="
EOF

chmod +x deploy.sh
```

---

## 九、测试部署

1. 访问前端：`https://your-domain.com`
2. 访问后台：`https://your-domain.com/admin`
3. 测试 API：`curl https://your-domain.com/api/reimbursements/`

---

## 十、故障排查

### 问题 1: 502 Bad Gateway
```bash
# 检查 Gunicorn 是否运行
sudo systemctl status reimbursement
# 检查日志
sudo journalctl -u reimbursement -n 50
```

### 问题 2: 静态文件404
```bash
python manage.py collectstatic --noinput
sudo systemctl restart reimbursement
```

### 问题 3: 文件上传失败
```bash
# 检查 media 目录权限
ls -la /var/www/reimbursement-backend/media
sudo chown -R www-data:www-data /var/www/reimbursement-backend/media
```

### 问题 4: CORS 错误
- 确保 settings.py 中配置了正确的 CORS_ALLOWED_ORIGINS
- 检查 Nginx 配置中的 proxy_set_header

---

## 性能优化建议

1. **使用 Redis 缓存**
   ```bash
   pip install django-redis
   ```

2. **启用 Gzip 压缩** (Nginx)
   ```nginx
   gzip on;
   gzip_types text/plain text/css application/json application/javascript;
   ```

3. **CDN 加速静态资源**

4. **数据库索引优化**

5. **使用进程管理器** (如 Supervisor，可选替代 systemd)

---

## 联系与支持

部署过程中遇到问题，请检查：
- 日志文件
- 防火墙设置
- 文件权限
- 环境变量配置
