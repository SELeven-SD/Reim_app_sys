#!/bin/bash
# 一键修复所有问题

echo "========================================="
echo "修复权限和500错误问题"
echo "========================================="
echo ""
echo "问题原因："
echo "  - Nginx无法访问 /home/lionp 目录（权限拒绝）"
echo "  - 静态文件CSS/JS无法加载"
echo ""
echo "解决方案："
echo "  1. 修改目录权限让Nginx可以访问"
echo "  2. 重新加载Nginx配置"
echo ""
echo "请输入sudo密码以继续..."
echo ""

# 修复权限
sudo chmod 755 /home/lionp
sudo chmod 755 /home/lionp/app_bx
sudo chmod 755 /home/lionp/app_bx/reimbursement-backend
sudo chmod -R 755 /home/lionp/app_bx/reimbursement-backend/staticfiles
sudo chmod 755 /home/lionp/app_bx/reimbursement-frontend
sudo chmod -R 755 /home/lionp/app_bx/reimbursement-frontend/dist

echo "✓ 权限已修复"
echo ""

# 重新加载Nginx
sudo systemctl reload nginx
echo "✓ Nginx已重新加载"
echo ""

# 测试静态文件
echo "========================================="
echo "测试访问"
echo "========================================="
echo ""

echo "【1】测试后台静态文件..."
if curl -s -I http://211.87.236.94/static/admin/css/base.css | grep -q "200 OK"; then
    echo "✓ 后台CSS加载正常"
else
    echo "✗ 后台CSS仍然有问题"
    echo "错误信息："
    sudo tail -5 /var/log/nginx/reimbursement_error.log
fi
echo ""

echo "【2】测试前端首页..."
if curl -s -I http://211.87.236.94/ | grep -q "200 OK"; then
    echo "✓ 前端首页访问正常"
else
    echo "✗ 前端首页仍然有问题"
fi
echo ""

echo "========================================="
echo "修复完成！"
echo "========================================="
echo ""
echo "现在请在浏览器中访问："
echo ""
echo "  前端: http://211.87.236.94"
echo "  后台: http://211.87.236.94/admin"
echo "    用户名: admin"
echo "    密码: admin123"
echo ""
echo "后台现在应该有完整的样式和图形界面了！"
echo ""
