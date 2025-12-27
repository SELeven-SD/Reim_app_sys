# reimbursement/admin_site.py
from django.contrib.admin import AdminSite
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.shortcuts import redirect
from django.urls import reverse

class RestrictedAdminSite(AdminSite):
    """限制只有超级用户和指定的管理员才能访问后台"""
    
    site_header = '报销管理系统后台'
    site_title = '报销管理系统'
    index_title = '欢迎使用报销管理系统'
    
    def has_permission(self, request):
        """
        检查用户是否有权限访问后台
        只允许超级用户或被指定为 staff 的用户登录
        """
        # 用户必须已认证
        if not request.user.is_authenticated:
            return False
        
        # 只允许超级用户或管理员访问
        return request.user.is_active and (request.user.is_superuser or request.user.is_staff)
    
    def login(self, request, extra_context=None):
        """
        自定义登录页面，显示权限提示
        """
        if extra_context is None:
            extra_context = {}
        extra_context['site_header'] = self.site_header
        extra_context['site_title'] = self.site_title
        return super().login(request, extra_context)

# 创建自定义的 admin 站点实例
restricted_admin_site = RestrictedAdminSite(name='restricted_admin')

# 注册 Django 默认的用户和组管理
restricted_admin_site.register(User, UserAdmin)
restricted_admin_site.register(Group, GroupAdmin)
