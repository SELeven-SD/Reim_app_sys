# 🎉 报销系统已成功修复并启动！

## 📍 访问地址

**前端应用**: http://211.87.236.94:9999
**后台管理**: http://211.87.236.94:9999/admin

## 🔐 管理员账户
- 用户名: `admin`
- 密码: `admin123`

---

## ✅ 系统状态

### 后端服务 (Django + Gunicorn)
- ✅ 运行中
- 端口: 8000
- 进程数: 3个worker进程
- 日志: `/tmp/gunicorn.log`

### 前端服务 (Vue.js)
- ✅ 已构建
- 通过Nginx提供静态文件

### Nginx反向代理
- ✅ 运行中
- 监听端口: 9999
- 配置文件: `/etc/nginx/sites-enabled/reimbursement`

---

## 🔧 服务管理命令

### 查看后端状态
```bash
ps aux | grep gunicorn | grep -v grep
netstat -tuln | grep 8000
```

### 查看后端日志
```bash
tail -f /tmp/gunicorn.log
```

### 重启后端服务
```bash
cd /home/lionp/Reim_app_sys
./restart.sh
```

### 停止后端服务
```bash
pkill -f "gunicorn.*reimbursement_system"
```

### 手动启动后端
```bash
cd /home/lionp/Reim_app_sys/reimbursement-backend
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 --config gunicorn_config.py reimbursement_system.wsgi:application
```

### 重新加载Nginx
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 查看Nginx日志
```bash
sudo tail -f /var/log/nginx/reimbursement_access.log
sudo tail -f /var/log/nginx/reimbursement_error.log
```

---

## 🆕 重新提交功能说明

用户现在可以修改被拒绝的报销申请并重新提交！

### 使用流程：
1. 进入"我的报销申请"页面
2. 找到状态为"❌ 未通过"的申请
3. 查看拒绝原因
4. 点击"🔄 重新提交"按钮
5. 修改申请内容（可选择是否更换发票）
6. 点击"✅ 重新提交审核"
7. 申请状态自动变为"⏳ 待审核"

详细说明请查看: [RESUBMIT_FEATURE.md](RESUBMIT_FEATURE.md)

---

## 🌐 API端点测试

### 获取公告列表（无需认证）
```bash
curl http://127.0.0.1:9999/api/reimbursements/notices/
```

### 用户注册
```bash
curl -X POST http://127.0.0.1:9999/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123","email":"test@example.com"}'
```

### 用户登录获取Token
```bash
curl -X POST http://127.0.0.1:9999/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### 查看我的报销申请
```bash
curl http://127.0.0.1:9999/api/reimbursements/ \
  -H "Authorization: Bearer {your_access_token}"
```

---

## 🛠️ 故障排查

### 502 Bad Gateway错误
**原因**: 后端服务未运行
**解决**:
```bash
cd /home/lionp/Reim_app_sys
./restart.sh
```

### 前端无法访问
**检查Nginx状态**:
```bash
sudo systemctl status nginx
sudo nginx -t
```

### API返回404
**检查URL路径**: 确保使用正确的API路径
- 公告: `/api/reimbursements/notices/`
- 报销列表: `/api/reimbursements/`
- 注册: `/api/register/`
- 登录: `/api/token/`

### 无法上传发票
**检查文件大小**: 最大50MB
**检查文件格式**: 只支持PDF

---

## 📂 重要文件路径

```
/home/lionp/Reim_app_sys/
├── reimbursement-backend/        # 后端代码
│   ├── db.sqlite3                 # 数据库
│   ├── media/invoices/            # 发票存储目录
│   ├── venv/                      # Python虚拟环境
│   └── manage.py                  # Django管理命令
├── reimbursement-frontend/       # 前端代码
│   └── dist/                      # 构建后的静态文件
├── restart.sh                     # 重启脚本
├── setup_nginx.sh                 # Nginx配置脚本
└── RESUBMIT_FEATURE.md           # 重新提交功能文档
```

---

## 🎯 下一步建议

1. **测试重新提交功能**
   - 创建一个报销申请
   - 使用管理员账户拒绝该申请
   - 使用普通用户账户修改并重新提交

2. **配置防火墙** (如果需要外网访问)
   ```bash
   sudo ufw allow 9999/tcp
   ```

3. **设置开机自启动**
   - 创建systemd服务文件
   - 或在crontab中添加启动命令

4. **备份数据库**
   ```bash
   cp /home/lionp/Reim_app_sys/reimbursement-backend/db.sqlite3 ~/backup/
   ```

---

## 📞 技术支持

如有问题，请检查：
1. 后端日志: `/tmp/gunicorn.log`
2. Nginx日志: `/var/log/nginx/reimbursement_error.log`
3. 确保所有服务正常运行

---

**系统已就绪，可以开始使用！** 🚀
