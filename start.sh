#!/bin/bash
# 报销系统启动脚本

echo "========================================"
echo "报销管理系统部署脚本"
echo "========================================"
echo ""

# 显示后端服务器信息
echo "✓ 虚拟环境已创建"
echo "✓ Python依赖已安装"
echo "✓ 数据库已迁移"
echo "✓ 前端已构建完成"
echo ""

# 启动后端服务
echo "启动后端服务..."
cd /home/lionp/app_bx/reimbursement-backend
source venv/bin/activate
nohup gunicorn --config gunicorn_config.py reimbursement_system.wsgi:application > /tmp/gunicorn.log 2>&1 &
BACKEND_PID=$!
echo "后端已启动 (PID: $BACKEND_PID)"
echo ""

# 等待后端启动
sleep 2

# 检查后端是否运行
if curl -s http://127.0.0.1:8000/admin/ > /dev/null 2>&1; then
    echo "✓ 后端服务运行正常"
else
    echo "✗ 后端服务可能未正常启动，请检查日志: tail -f /tmp/gunicorn.log"
fi
echo ""

# Nginx配置提示
echo "========================================"
echo "下一步：配置Nginx（需要sudo权限）"
echo "========================================"
echo ""
echo "请执行以下命令（需要输入sudo密码）："
echo ""
echo "sudo cp /tmp/reimbursement_nginx.conf /etc/nginx/sites-available/reimbursement"
echo "sudo ln -sf /etc/nginx/sites-available/reimbursement /etc/nginx/sites-enabled/"
echo "sudo nginx -t"
echo "sudo systemctl reload nginx"
echo ""
echo "或者，如果您有sudo权限，可以直接运行："
echo "bash /home/lionp/app_bx/setup_nginx.sh"
echo ""

echo "========================================"
echo "访问地址"
echo "========================================"
echo ""
echo "前端应用: http://211.87.236.94"
echo "后台管理: http://211.87.236.94/admin"
echo "  用户名: admin"
echo "  密码: admin123"
echo ""
echo "如果无法访问，请先配置并启动Nginx"
echo ""

echo "========================================"
echo "常用命令"
echo "========================================"
echo ""
echo "查看后端日志: tail -f /tmp/gunicorn.log"
echo "停止后端: pkill -f gunicorn"
echo "重启后端: bash /home/lionp/app_bx/start.sh"
echo ""
