#!/bin/bash
# 重启服务以应用新配置

echo "========================================="
echo "重启服务以应用新配置"
echo "========================================="
echo ""

# 停止旧的后端进程
echo "停止旧的后端进程..."
pkill -f "gunicorn.*reimbursement_system" 2>/dev/null
sleep 2

# 启动新的后端服务
echo "启动后端服务..."
cd /home/lionp/app_bx/reimbursement-backend
source venv/bin/activate
nohup gunicorn --bind 0.0.0.0:8000 --config gunicorn_config.py reimbursement_system.wsgi:application > /tmp/gunicorn.log 2>&1 &
BACKEND_PID=$!
echo "✓ 后端已启动 (PID: $BACKEND_PID)"
sleep 2

# 检查后端状态
if curl -s http://127.0.0.1:8000/admin/ > /dev/null 2>&1; then
    echo "✓ 后端服务运行正常"
else
    echo "✗ 后端可能未正常启动，请检查日志"
fi

echo ""
echo "========================================="
echo "配置Nginx（需要sudo权限）"
echo "========================================="
echo ""
echo "执行以下命令："
echo "bash /home/lionp/app_bx/setup_nginx.sh"
echo ""
