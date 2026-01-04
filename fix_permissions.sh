#!/bin/bash
# 修复权限和配置问题

echo "========================================="
echo "修复静态文件和权限问题"
echo "========================================="
echo ""

echo "【1】修复文件权限..."
echo "执行以下命令（需要sudo密码）："
echo ""
echo "sudo chmod 755 /home/lionp"
echo "sudo chmod 755 /home/lionp/app_bx"
echo "sudo chmod 755 /home/lionp/app_bx/reimbursement-backend"
echo "sudo chmod -R 755 /home/lionp/app_bx/reimbursement-backend/staticfiles"
echo "sudo chmod -R 755 /home/lionp/app_bx/reimbursement-frontend"
echo "sudo chmod -R 755 /home/lionp/app_bx/reimbursement-frontend/dist"
echo ""

read -p "按回车继续执行权限修复..." 

sudo chmod 755 /home/lionp
sudo chmod 755 /home/lionp/app_bx
sudo chmod 755 /home/lionp/app_bx/reimbursement-backend
sudo chmod -R 755 /home/lionp/app_bx/reimbursement-backend/staticfiles
sudo chmod -R 755 /home/lionp/app_bx/reimbursement-frontend
sudo chmod -R 755 /home/lionp/app_bx/reimbursement-frontend/dist

echo "✓ 权限修复完成"
echo ""

echo "【2】测试静态文件访问..."
if curl -s -I http://211.87.236.94/static/admin/css/base.css | grep -q "200 OK"; then
    echo "✓ 静态文件访问正常"
else
    echo "✗ 静态文件仍无法访问，检查Nginx错误日志："
    sudo tail -20 /var/log/nginx/reimbursement_error.log
fi
echo ""

echo "【3】重新加载Nginx..."
sudo systemctl reload nginx
echo "✓ Nginx已重新加载"
echo ""

echo "========================================="
echo "测试访问"
echo "========================================="
echo ""
echo "1. 前端: http://211.87.236.94"
echo "2. 后台: http://211.87.236.94/admin (应该有样式了)"
echo ""
