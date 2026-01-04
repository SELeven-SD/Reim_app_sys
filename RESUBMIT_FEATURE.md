# 重新提交被拒绝申请功能说明

## 功能概述
用户现在可以修改并重新提交被审核拒绝的报销申请。

## 实现的功能

### 1. 后端 API 改进
**文件**: `reimbursement-backend/reimbursement/views.py`

- ✅ 修改了 `ReimbursementDetailView.update()` 方法
- ✅ 支持 PATCH 部分更新，允许只修改需要改变的字段
- ✅ 只有状态为 `rejected` 的申请才能被修改
- ✅ 更新成功后自动将状态改回 `pending`（待审核）
- ✅ 自动清空 `rejection_reason`（拒绝理由）
- ✅ 支持更新发票文件（可选）

### 2. 前端交互流程
**文件**: `reimbursement-frontend/src/views/MyReimbursements.vue`

- ✅ 在"我的报销申请"页面，被拒绝的申请会显示拒绝原因
- ✅ 显示"重新提交"按钮
- ✅ 点击后跳转到首页，自动填充申请数据

**文件**: `reimbursement-frontend/src/components/ReimbursementForm.vue`

- ✅ 识别重新提交模式（通过URL参数）
- ✅ 自动填充原有申请数据
- ✅ 发票字段变为可选（如不上传新发票则保留原发票）
- ✅ 使用 PATCH 请求更新申请而不是 POST 创建新申请
- ✅ 提交成功后跳转到"我的申请"页面

## 使用方法

### 用户操作流程：

1. **查看被拒绝的申请**
   - 进入"我的报销申请"页面
   - 找到状态为"❌ 未通过"的申请
   - 查看拒绝原因

2. **重新提交**
   - 点击申请卡片中的"🔄 重新提交"按钮
   - 系统自动跳转到首页并填充原申请数据
   - 页面顶部会显示黄色提示："📝 您正在修改被驳回的申请，请修改后重新提交"

3. **修改申请内容**
   - 修改真实姓名、报销事由、金额等字段
   - 可选：上传新的发票PDF（如不上传则保留原发票）
   - 修改备注信息

4. **提交审核**
   - 点击"✅ 重新提交审核"按钮
   - 系统自动将申请状态改为"⏳ 待审核"
   - 清空之前的拒绝理由
   - 跳转到"我的申请"页面查看更新后的申请

## 技术细节

### 后端 API 端点
```
PATCH /api/reimbursements/{id}/
```

**请求头**:
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**请求数据** (FormData):
- `real_name`: 真实姓名
- `reason`: 报销事由
- `amount`: 金额
- `remarks`: 备注（可选）
- `invoice_pdf`: 发票文件（可选，File对象）

**响应**:
- 成功: 200 OK，返回更新后的完整申请数据
- 失败: 
  - 403 Forbidden: 非rejected状态的申请不能修改
  - 401 Unauthorized: 未登录或token过期
  - 400 Bad Request: 数据验证失败

### 前端路由参数

重新提交时的URL参数：
```
/?resubmit=true&id={申请ID}&realName={姓名}&reason={事由}&amount={金额}&remarks={备注}
```

### 状态流转

```
rejected (被拒绝) 
    ↓ 用户修改并重新提交
pending (待审核) 
    ↓ 管理员审核
approved (通过) 或 rejected (再次拒绝)
```

## 权限控制

- ✅ 只有申请的所有者才能修改自己的申请
- ✅ 只有状态为 `rejected` 的申请才能被修改
- ✅ 修改后状态自动重置为 `pending`

## 测试建议

### 测试场景：

1. **正常重新提交流程**
   - 创建一个报销申请
   - 管理员拒绝该申请并填写拒绝理由
   - 用户查看被拒绝的申请
   - 点击"重新提交"按钮
   - 修改数据后重新提交
   - 验证申请状态变为"待审核"

2. **不更换发票**
   - 重新提交时不上传新发票
   - 验证原发票仍然保留

3. **更换发票**
   - 重新提交时上传新发票
   - 验证新发票替换旧发票

4. **权限测试**
   - 尝试修改 pending 或 approved 状态的申请
   - 验证返回403错误
   - 尝试修改其他用户的申请
   - 验证无法访问

## 文件修改清单

✅ 后端修改：
- `reimbursement-backend/reimbursement/views.py` - 修改 ReimbursementDetailView.update() 方法

✅ 前端修改：
- `reimbursement-frontend/src/views/MyReimbursements.vue` - 已有重新提交按钮和处理逻辑
- `reimbursement-frontend/src/components/ReimbursementForm.vue` - 使用PATCH请求而非PUT

✅ 脚本修改：
- `restart.sh` - 修正路径错误

## 启动服务

由于系统环境配置问题，后端服务需要在虚拟环境中运行。请按以下步骤操作：

1. **创建/激活虚拟环境** （如果还没有）:
   ```bash
   cd /home/lionp/Reim_app_sys/reimbursement-backend
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **安装依赖** （如果还没有）:
   ```bash
   pip install -r requirements.txt
   ```

3. **启动后端服务**:
   ```bash
   # 使用gunicorn（生产环境）
   gunicorn --bind 0.0.0.0:8000 --config gunicorn_config.py reimbursement_system.wsgi:application
   
   # 或使用Django开发服务器（测试环境）
   python manage.py runserver 0.0.0.0:8000
   ```

4. **前端服务**应该通过Nginx反向代理访问。

## 注意事项

- ⚠️ 发票文件大小限制：50MB
- ⚠️ 只支持PDF格式的发票
- ⚠️ 重新提交后，申请会回到待审核队列
- ⚠️ 只有被拒绝的申请才能重新提交
- ⚠️ 如果不上传新发票，原发票会被保留

## 后续优化建议

1. 添加申请修改历史记录
2. 支持管理员查看申请的修改次数
3. 限制同一申请的最大重新提交次数
4. 邮件/消息通知功能（通知用户申请被拒绝）
5. 批量操作功能
