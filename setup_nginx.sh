#!/bin/bash
# Nginx配置脚本（需要sudo权限）

echo "配置Nginx..."
sudo cp /tmp/reimbursement_nginx.conf /etc/nginx/sites-available/reimbursement
sudo ln -sf /etc/nginx/sites-available/reimbursement /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

echo ""
echo "✓ Nginx配置完成"
echo ""
echo "访问地址: http://211.87.236.61"
