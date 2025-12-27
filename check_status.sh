#!/bin/bash
# 部署状态检查脚本

echo "========================================="
echo "报销系统部署状态检查"
echo "========================================="
echo ""

# 检查后端进程
echo "【1】检查后端服务..."
if pgrep -f "gunicorn.*reimbursement" > /dev/null; then
    echo "✓ 后端服务正在运行"
    echo "  进程数: $(pgrep -f "gunicorn.*reimbursement" | wc -l)"
    echo "  监听端口: $(netstat -tuln 2>/dev/null | grep :8000 || ss -tuln 2>/dev/null | grep :8000)"
else
    echo "✗ 后端服务未运行"
    echo "  请执行: bash /home/lionp/app_bx/restart.sh"
fi
echo ""

# 检查前端构建
echo "【2】检查前端构建..."
if [ -d "/home/lionp/app_bx/reimbursement-frontend/dist" ]; then
    echo "✓ 前端已构建"
    echo "  文件数: $(find /home/lionp/app_bx/reimbursement-frontend/dist -type f | wc -l)"
else
    echo "✗ 前端未构建"
    echo "  请执行: cd /home/lionp/app_bx/reimbursement-frontend && npm run build"
fi
echo ""

# 检查Nginx配置
echo "【3】检查Nginx配置..."
if [ -f "/etc/nginx/sites-enabled/reimbursement" ]; then
    echo "✓ Nginx配置已启用"
else
    echo "✗ Nginx配置未启用"
    echo "  请执行: bash /home/lionp/app_bx/setup_nginx.sh"
fi
echo ""

# 检查Nginx运行状态
echo "【4】检查Nginx服务..."
if systemctl is-active --quiet nginx 2>/dev/null; then
    echo "✓ Nginx服务正在运行"
elif pgrep nginx > /dev/null; then
    echo "✓ Nginx进程正在运行"
else
    echo "✗ Nginx未运行"
    echo "  请执行: sudo systemctl start nginx"
fi
echo ""

# 检查端口
echo "【5】检查端口监听..."
if netstat -tuln 2>/dev/null | grep -q ":80 " || ss -tuln 2>/dev/null | grep -q ":80 "; then
    echo "✓ 80端口正在监听"
else
    echo "✗ 80端口未监听"
    echo "  请检查Nginx是否正常启动"
fi
echo ""

# 服务器IP
echo "【6】服务器信息..."
echo "  IP地址: $(hostname -I)"
echo "  主机名: $(hostname)"
echo ""

# 测试后端API
echo "【7】测试后端连接..."
if curl -s -m 5 http://127.0.0.1:8000/admin/ > /dev/null 2>&1; then
    echo "✓ 后端API响应正常"
else
    echo "✗ 后端API无响应"
    echo "  请检查: tail -f /tmp/gunicorn.log"
fi
echo ""

echo "========================================="
echo "访问地址"
echo "========================================="
echo ""
echo "从内网访问（192.168.x.x）："
echo "  http://211.87.236.61"
echo ""
echo "后台管理："
echo "  http://211.87.236.61/admin"
echo "  用户名: admin"
echo "  密码: admin123"
echo ""

echo "========================================="
echo "下一步操作"
echo "========================================="
echo ""

# 根据检查结果给出建议
NEED_NGINX=false
NEED_BACKEND=false

if ! [ -f "/etc/nginx/sites-enabled/reimbursement" ]; then
    NEED_NGINX=true
fi

if ! pgrep -f "gunicorn.*reimbursement" > /dev/null; then
    NEED_BACKEND=true
fi

if [ "$NEED_NGINX" = true ]; then
    echo "⚠️  需要配置Nginx:"
    echo "   bash /home/lionp/app_bx/setup_nginx.sh"
    echo ""
fi

if [ "$NEED_BACKEND" = true ]; then
    echo "⚠️  需要启动后端:"
    echo "   bash /home/lionp/app_bx/restart.sh"
    echo ""
fi

if [ "$NEED_NGINX" = false ] && [ "$NEED_BACKEND" = false ]; then
    echo "✅ 所有服务运行正常！"
    echo ""
    echo "现在可以从您的个人电脑访问："
    echo "http://211.87.236.61"
    echo ""
fi

echo "查看详细配置说明："
echo "  cat /home/lionp/app_bx/NETWORK_CONFIG.md"
echo ""
