# 问题修复说明

## 遇到的问题

### 1. 前端显示 500 Internal Server Error
### 2. 后端管理界面没有图形，只显示文字（CSS/JS未加载）

---

## 问题原因

**根本原因**: Nginx无权访问 `/home/lionp` 目录下的文件

Linux系统中，用户home目录（`/home/username`）默认权限通常是 `700` 或 `750`，这意味着：
- `700`: 只有用户自己可以访问
- `750`: 用户和同组用户可以访问

而Nginx通常以 `www-data` 或 `nginx` 用户运行，不属于 `lionp` 用户组，因此无法读取这些文件。

### 错误日志显示：
```
Permission denied: /home/lionp/app_bx/reimbursement-backend/staticfiles/admin/css/base.css
Permission denied: /home/lionp/app_bx/reimbursement-frontend/dist/index.html
```

---

## 解决方案

### 已执行的修复操作：

```bash
# 1. 修改 /home/lionp 目录权限（允许其他用户执行/遍历）
sudo chmod 755 /home/lionp

# 2. 修改项目目录权限
sudo chmod 755 /home/lionp/app_bx
sudo chmod 755 /home/lionp/app_bx/reimbursement-backend

# 3. 修改静态文件目录权限（递归）
sudo chmod -R 755 /home/lionp/app_bx/reimbursement-backend/staticfiles

# 4. 修改前端构建目录权限
sudo chmod 755 /home/lionp/app_bx/reimbursement-frontend
sudo chmod -R 755 /home/lionp/app_bx/reimbursement-frontend/dist

# 5. 重新加载Nginx
sudo systemctl reload nginx
```

### 权限说明：

- `755` = `rwxr-xr-x`
  - 所有者（lionp）: 读写执行 (7 = rwx)
  - 组用户: 读和执行 (5 = r-x)
  - 其他用户（包括nginx）: 读和执行 (5 = r-x)

---

## 验证修复

### 1. 测试后台静态文件
```bash
curl -I http://211.87.236.94/static/admin/css/base.css
# 应该返回: HTTP/1.1 200 OK
```

### 2. 测试前端
```bash
curl -I http://211.87.236.94/
# 应该返回: HTTP/1.1 200 OK
```

### 3. 浏览器访问
- 后台：http://211.87.236.94/admin
  - 现在应该看到完整的蓝色Django管理界面
  - 有图标、按钮、样式等

- 前端：http://211.87.236.94
  - 应该正常显示Vue应用

---

## 避免类似问题的建议

### 方案1: 使用非home目录部署（推荐）
将项目部署到系统目录，如：
```bash
/var/www/reimbursement-backend
/var/www/reimbursement-frontend
```

优点：
- 避免home目录权限问题
- 更符合生产环境最佳实践
- 不需要修改用户home目录权限

### 方案2: 继续使用home目录
如果必须使用home目录，确保：
```bash
chmod 755 /home/lionp  # 允许遍历
chmod 755 /home/lionp/项目目录  # 允许访问
```

---

## 相关文件

修复脚本已创建：
- `/home/lionp/app_bx/fix_all.sh` - 一键修复所有权限问题
- `/home/lionp/app_bx/check_status.sh` - 检查系统状态

如果将来遇到类似问题，直接运行：
```bash
bash /home/lionp/app_bx/fix_all.sh
```

---

## 当前系统状态

✅ 所有服务正常运行
✅ 权限已正确配置
✅ 前端和后端都可以正常访问
✅ 静态文件（CSS/JS）加载正常

---

## 访问信息

**从您的个人电脑（192网段）访问：**

- 前端应用：http://211.87.236.94
- 后台管理：http://211.87.236.94/admin
  - 用户名: admin
  - 密码: admin123

现在后台应该显示完整的Django管理界面，包括：
- 蓝色顶部导航栏
- 左侧边栏
- 图标和按钮
- 完整的CSS样式
