# 报销系统开机自启配置说明

## ✅ 当前状态
系统已配置为**开机自动启动**，使用 systemd 服务管理。

## 📋 服务信息

### 服务名称
`reimbursement.service`

### 服务文件位置
`/etc/systemd/system/reimbursement.service`

### 服务配置
```ini
[Unit]
Description=Reimbursement System Gunicorn Daemon
After=network.target

[Service]
User=lionp
Group=lionp
WorkingDirectory=/home/lionp/Reim_app_sys/reimbursement-backend
Environment="PATH=/home/lionp/Reim_app_sys/reimbursement-backend/venv/bin"
ExecStart=/home/lionp/Reim_app_sys/reimbursement-backend/venv/bin/gunicorn \
    --config /home/lionp/Reim_app_sys/reimbursement-backend/gunicorn_config.py \
    reimbursement_system.wsgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

## 🎮 服务管理命令

### 启动服务
```bash
sudo systemctl start reimbursement.service
```

### 停止服务
```bash
sudo systemctl stop reimbursement.service
```

### 重启服务
```bash
sudo systemctl restart reimbursement.service
```

### 查看服务状态
```bash
sudo systemctl status reimbursement.service
```

### 查看服务日志
```bash
# 实时查看日志
sudo journalctl -u reimbursement.service -f

# 查看最近50条日志
sudo journalctl -u reimbursement.service -n 50

# 查看今天的日志
sudo journalctl -u reimbursement.service --since today
```

### 启用开机自启（已启用）
```bash
sudo systemctl enable reimbursement.service
```

### 禁用开机自启
```bash
sudo systemctl disable reimbursement.service
```

### 检查开机自启状态
```bash
systemctl is-enabled reimbursement.service
```

## 🔄 开机启动流程

1. **系统启动** → 加载 systemd
2. **网络就绪** → 触发 `After=network.target`
3. **启动服务** → 执行 gunicorn 命令
4. **自动重启** → 如果服务崩溃，3秒后自动重启（`Restart=always, RestartSec=3`）

## 🛠️ 故障排查

### 检查服务是否在运行
```bash
sudo systemctl is-active reimbursement.service
```

### 服务无法启动
1. 查看详细日志：
   ```bash
   sudo journalctl -u reimbursement.service -n 100
   ```

2. 检查端口是否被占用：
   ```bash
   sudo lsof -i :8000
   ```

3. 手动测试启动：
   ```bash
   cd /home/lionp/Reim_app_sys/reimbursement-backend
   source venv/bin/activate
   gunicorn --config gunicorn_config.py reimbursement_system.wsgi:application
   ```

### 端口冲突
如果有手动启动的进程，需要先停止：
```bash
# 查找进程
ps aux | grep gunicorn

# 停止进程（替换PID）
kill <PID>

# 或停止所有gunicorn
pkill -f gunicorn
```

## 📊 性能监控

### 查看进程资源使用
```bash
sudo systemctl status reimbursement.service
```

### 查看所有worker进程
```bash
ps aux | grep gunicorn
```

### 查看内存使用
```bash
ps aux | grep gunicorn | awk '{sum+=$6} END {print "Total Memory: " sum/1024 " MB"}'
```

## 🔐 权限说明

- 服务以 `lionp` 用户身份运行
- 需要 `sudo` 权限来管理服务（启动/停止/重启）
- 日志查看需要 `sudo` 权限

## 🌐 配合 Nginx

系统已配置 Nginx 反向代理：
- Nginx 在系统启动时自动启动
- Gunicorn 通过 systemd 自动启动
- 两者配合提供完整的 Web 服务

检查 Nginx 状态：
```bash
sudo systemctl status nginx
```

## ✨ 优势

使用 systemd 管理的优势：
1. ✅ **开机自启** - 系统重启后自动启动
2. ✅ **自动恢复** - 进程崩溃后自动重启
3. ✅ **统一管理** - 使用标准的 systemctl 命令
4. ✅ **日志集成** - 日志集成到 journalctl
5. ✅ **资源控制** - 可配置资源限制
6. ✅ **依赖管理** - 等待网络就绪后启动

## 📝 备注

- 服务配置文件已更新为正确的路径
- 使用 16 个 gevent worker 进程（高并发优化）
- 支持 200-300 个并发用户
- 自动重启间隔为 3 秒
