# reimbursement/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ReimbursementRequest, Notice

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    real_name = serializers.CharField(max_length=100, required=False, help_text="真实姓名")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'real_name']
    
    def create(self, validated_data):
        real_name = validated_data.pop('real_name', '')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        # 如果提供了真实姓名，尝试拆分为姓和名
        if real_name:
            # 中文名通常第一个字是姓
            if len(real_name) >= 2:
                user.last_name = real_name[0]  # 姓
                user.first_name = real_name[1:]  # 名
            else:
                user.first_name = real_name
            user.save()
        
        return user

class ReimbursementRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    invoice_pdf = serializers.FileField(required=True)  # 可读可写，新建时必须
    invoice_pdf_url = serializers.SerializerMethodField()  # 只读，用于返回完整URL
    
    class Meta:
        model = ReimbursementRequest
        fields = ['id', 'user', 'real_name', 'reason', 'amount', 'invoice_pdf', 'invoice_pdf_url', 'remarks', 'status', 'rejection_reason', 'submission_date']
        read_only_fields = ['id', 'user', 'status', 'rejection_reason', 'submission_date', 'invoice_pdf_url']
    
    def get_invoice_pdf_url(self, obj):
        """返回PDF文件的完整访问URL"""
        if obj.invoice_pdf and obj.invoice_pdf.name:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.invoice_pdf.url)
            return obj.invoice_pdf.url
        return None
    
    def to_representation(self, instance):
        """自定义返回格式，保持向后兼容"""
        ret = super().to_representation(instance)
        # 同时提供invoice_pdf（URL）和invoice_pdf_url字段，保持兼容性
        ret['invoice_pdf'] = ret.get('invoice_pdf_url')
        return ret

class ReimbursementRequestUpdateSerializer(serializers.ModelSerializer):
    invoice_pdf = serializers.FileField(required=False)  # 重新提交时发票可选
    
    class Meta:
        model = ReimbursementRequest
        fields = ['real_name', 'reason', 'amount', 'invoice_pdf', 'remarks']
    
    def update(self, instance, validated_data):
        """更新时，如果上传了新的PDF，删除旧的PDF文件"""
        import os
        
        # 检查是否上传了新的PDF文件
        new_pdf = validated_data.get('invoice_pdf')
        if new_pdf and instance.invoice_pdf:
            # 获取旧文件的路径
            old_file_path = instance.invoice_pdf.path
            
            # 先更新实例（这会保存新文件）
            instance = super().update(instance, validated_data)
            
            # 删除旧文件
            if os.path.exists(old_file_path):
                try:
                    os.remove(old_file_path)
                except Exception as e:
                    print(f"删除旧文件失败: {old_file_path}, 错误: {e}")
            
            return instance
        
        # 如果没有上传新PDF，正常更新
        return super().update(instance, validated_data)
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'priority', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']        