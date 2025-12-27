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
    class Meta:
        model = ReimbursementRequest
        fields = ['id', 'user', 'real_name', 'reason', 'amount', 'invoice_pdf', 'remarks', 'status', 'rejection_reason', 'submission_date']
        read_only_fields = ['id', 'user', 'status', 'rejection_reason', 'submission_date']

class ReimbursementRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReimbursementRequest
        fields = ['real_name', 'reason', 'amount', 'invoice_pdf', 'remarks']
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'priority', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']        