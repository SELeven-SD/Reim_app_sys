#!/bin/bash
# 测试报销申请反馈功能

echo "========================================="
echo "测试报销申请审核反馈功能"
echo "========================================="
echo ""

echo "【功能说明】"
echo "1. 新增了'我的申请'页面，用户可以查看所有报销申请"
echo "2. 显示申请状态：待审核、审核通过、审核不通过"
echo "3. 对于审核不通过的申请，会显示详细的不通过原因"
echo "4. 用户可以针对被拒绝的申请重新提交"
echo ""

echo "【测试步骤】"
echo ""
echo "1. 在后台创建测试数据："
echo "   访问: http://211.87.236.94/admin"
echo "   用户名: admin"
echo "   密码: admin123"
echo ""
echo "2. 进入 '报销申请' 管理"
echo ""
echo "3. 添加或修改报销申请："
echo "   - 创建一个待审核的申请"
echo "   - 创建一个审核通过的申请"
echo "   - 创建一个审核不通过的申请，并填写'不通过理由'"
echo ""
echo "4. 在前端查看："
echo "   访问: http://211.87.236.94"
echo "   点击顶部导航栏的 '我的申请'"
echo ""
echo "【期望结果】"
echo "✓ 能看到所有报销申请列表"
echo "✓ 每个申请显示不同的状态标签（待审核/审核通过/审核不通过）"
echo "✓ 审核不通过的申请会显示红色提示框，包含不通过原因"
echo "✓ 审核通过的申请显示绿色成功标志"
echo ""

# 检查后端API
echo "【检查后端API】"
if curl -s http://127.0.0.1:8000/api/reimbursements/ > /dev/null 2>&1; then
    echo "✓ 后端API运行正常"
else
    echo "✗ 后端API无响应"
fi
echo ""

# 检查前端
echo "【检查前端】"
if [ -f "/home/lionp/app_bx/reimbursement-frontend/dist/index.html" ]; then
    echo "✓ 前端已构建"
    echo "  文件数: $(find /home/lionp/app_bx/reimbursement-frontend/dist -type f | wc -l)"
else
    echo "✗ 前端未构建"
fi
echo ""

echo "========================================="
echo "访问地址"
echo "========================================="
echo ""
echo "前端首页（提交申请）: http://211.87.236.94"
echo "我的申请（查看反馈）: http://211.87.236.94/my-reimbursements"
echo "后台管理: http://211.87.236.94/admin"
echo ""
