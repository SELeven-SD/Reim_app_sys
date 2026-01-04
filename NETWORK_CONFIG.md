# 内网访问配置说明

## 网络环境
- **服务器IP**: 211.87.236.94
- **客户端网段**: 192.168.x.x（内网）

## 已完成的配置

### 1. 后端配置
✅ 允许的主机已更新（支持192网段）
✅ CORS配置已更新（允许192.168.x.x访问）
✅ Gunicorn监听 0.0.0.0:8000（所有接口）

### 2. Nginx配置
✅ 监听所有接口
✅ 接受任意域名访问

## 完成部署步骤

### 步骤1: 配置Nginx（需要sudo密码）
```bash
bash /home/lionp/app_bx/setup_nginx.sh
```

或手动执行：
```bash
sudo cp /tmp/reimbursement_nginx.conf /etc/nginx/sites-available/reimbursement
sudo ln -sf /etc/nginx/sites-available/reimbursement /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 步骤2: 确保防火墙开放端口
```bash
# 检查80端口是否开放
sudo netstat -tuln | grep :80

# 如果使用ufw防火墙
sudo ufw allow 80/tcp
sudo ufw status

# 如果使用firewalld
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
```

## 访问方式

### 从内网客户端（192网段）访问：
- **前端**: http://211.87.236.94
- **后台**: http://211.87.236.94/admin
  - 用户名: admin
  - 密码: admin123

### 从服务器本地访问：
- **前端**: http://localhost
- **后台**: http://localhost/admin

## 测试连接

### 1. 从客户端测试能否访问服务器
```bash
# 在您的个人电脑（192网段）上执行
ping 211.87.236.94
curl -I http://211.87.236.94
```

### 2. 测试后端API
```bash
# 在您的个人电脑上执行
curl http://211.87.236.94/admin/
```

### 3. 测试前端
在浏览器打开：http://211.87.236.94

## 常见问题排查

### 问题1: 无法访问网站
**可能原因**:
1. Nginx未启动或配置错误
   ```bash
   sudo systemctl status nginx
   sudo nginx -t
   ```

2. 防火墙阻止80端口
   ```bash
   sudo ufw status
   # 或
   sudo firewall-cmd --list-all
   ```

3. 网络路由问题（内网到211网段不通）
   ```bash
   # 在客户端测试
   ping 211.87.236.94
   traceroute 211.87.236.94
   ```

### 问题2: 能访问前端但API报错
**检查**:
1. 后端是否运行
   ```bash
   ps aux | grep gunicorn
   curl http://127.0.0.1:8000/admin/
   ```

2. 查看后端日志
   ```bash
   tail -f /tmp/gunicorn.log
   ```

3. 查看Nginx错误日志
   ```bash
   sudo tail -f /var/log/nginx/reimbursement_error.log
   ```

### 问题3: CORS错误
**已配置**: 后端已允许所有192.168.x.x的访问

如果仍有问题，检查浏览器控制台的具体错误信息。

## 服务管理命令

### 重启后端
```bash
bash /home/lionp/app_bx/restart.sh
```

### 查看后端日志
```bash
tail -f /tmp/gunicorn.log
```

### 停止后端
```bash
pkill -f gunicorn
```

### 重启Nginx
```bash
sudo systemctl reload nginx
```

### 查看Nginx日志
```bash
# 访问日志
sudo tail -f /var/log/nginx/reimbursement_access.log

# 错误日志
sudo tail -f /var/log/nginx/reimbursement_error.log
```

## 网络架构图

```
[您的电脑]          [服务器]
192.168.x.x  --->  211.87.236.94:80 (Nginx)
                          |
                          ├─> 前端静态文件 (Vue)
                          └─> /api/* → 127.0.0.1:8000 (Gunicorn/Django)
```

## 下一步

1. 执行 `bash /home/lionp/app_bx/setup_nginx.sh` 配置Nginx
2. 在您的个人电脑浏览器打开 http://211.87.236.94
3. 如有问题，查看上述故障排查部分
