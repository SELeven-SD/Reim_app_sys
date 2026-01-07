#!/bin/bash
# 报销系统启动脚本

echo "========================================"
echo "报销管理系统启动脚本"
echo "========================================"
echo ""

# 检查systemd服务是否存在
if systemctl list-unit-files | grep -q "reimbursement.service"; then
    echo "使用systemd服务管理..."
    echo ""
    
    # 启动服务
    sudo systemctl start reimbursement.service
    
    # 等待服务启动
    sleep 3
    
    # 检查服务状态
    if systemctl is-active --quiet reimbursement.service; then
        echo "✓ 后端服务已启动（通过systemd）"
        systemctl status reimbursement.service --no-pager -l | head -10
    else
        echo "✗ 后端服务启动失败"
        echo "查看详细日志："
        echo "  sudo journalctl -u reimbursement.service -n 50"
        exit 1
    fi
else
    echo "使用手动启动方式..."
    echo ""
    
    # 启动后端服务
    echo "启动后端服务..."
    cd /home/lionp/Reim_app_sys/reimbursement-backend
    source venv/bin/activate
    nohup gunicorn --bind 0.0.0.0:8000 --config gunicorn_config.py reimbursement_system.wsgi:application > /tmp/gunicorn.log 2>&1 &
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
fi
echo ""

echo "========================================"
echo "系统访问信息"
echo "========================================"
echo ""
echo "前端访问地址: http://211.87.236.94:8088"
echo "管理后台地址: http://211.87.236.94:8088/admin"
echo ""
echo "服务管理命令:"
echo "  启动: sudo systemctl start reimbursement.service"
echo "  停止: sudo systemctl stop reimbursement.service"
echo "  重启: sudo systemctl restart reimbursement.service"
echo "  状态: sudo systemctl status reimbursement.service"
echo "  日志: sudo journalctl -u reimbursement.service -f"
echo ""
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
