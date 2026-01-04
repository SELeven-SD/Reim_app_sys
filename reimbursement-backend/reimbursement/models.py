# reimbursement/models.py
import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from datetime import datetime

def get_invoice_path(instance, filename):
    date_str = datetime.now().strftime('%Y_%m_%d')
    safe_reason = "".join([c for c in instance.reason if c.isalnum() or c.isspace()]).rstrip().replace(' ', '_')
    unique_id = uuid4().hex[:6]
    new_filename = f"{date_str}-{instance.real_name}-{safe_reason}-{unique_id}.pdf"
    return os.path.join('invoices', new_filename)

class ReimbursementRequest(models.Model):
    STATUS_CHOICES = [('pending', '待审核'), ('approved', '审核通过'), ('rejected', '审核不通过')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="提交用户")
    real_name = models.CharField(max_length=100, verbose_name="真实姓名")
    reason = models.CharField(max_length=255, verbose_name="报销事由")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金额")
    invoice_pdf = models.FileField(upload_to=get_invoice_path, verbose_name="发票PDF", blank=True, null=True)
    remarks = models.TextField(blank=True, verbose_name="备注")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="审核状态")
    rejection_reason = models.TextField(blank=True, verbose_name="不通过理由")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="提交日期")
    last_modified_date = models.DateTimeField(auto_now=True, verbose_name="最后修改日期")
    
    def __str__(self):
        return f"{self.submission_date.strftime('%Y-%m-%d')} - {self.real_name} - {self.reason}"

class Notice(models.Model):
    """系统公告/注意事项"""
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    priority = models.IntegerField(default=0, verbose_name="优先级")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "注意事项"
        verbose_name_plural = "注意事项"
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return self.title

# 信号处理：删除报销申请时自动删除关联的PDF文件
@receiver(post_delete, sender=ReimbursementRequest)
def delete_invoice_file(sender, instance, **kwargs):
    """删除报销申请时，自动删除对应的发票PDF文件"""
    if instance.invoice_pdf:
        if os.path.isfile(instance.invoice_pdf.path):
            try:
                os.remove(instance.invoice_pdf.path)
            except Exception as e:
                print(f"删除文件失败: {instance.invoice_pdf.path}, 错误: {e}")
