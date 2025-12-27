# reimbursement/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import ReimbursementRequest, Notice
from .serializers import (
    ReimbursementRequestSerializer, 
    ReimbursementRequestUpdateSerializer,
    UserRegistrationSerializer,
    NoticeSerializer
)

class RestrictedTokenObtainPairView(TokenObtainPairView):
    """限制只有超级用户或管理员才能登录"""
    
    def post(self, request, *args, **kwargs):
        # 先获取用户名
        username = request.data.get('username')
        
        if not username:
            return Response(
                {"detail": "请提供用户名"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(username=username)
            
            # 检查用户是否有权限访问后台
            if not (user.is_superuser or user.is_staff):
                return Response(
                    {"detail": "您没有权限访问系统，请联系管理员"},
                    status=status.HTTP_403_FORBIDDEN
                )
        except User.DoesNotExist:
            # 用户不存在，让默认的认证流程处理（会返回认证失败）
            pass
        
        # 调用父类方法进行正常的 token 生成
        return super().post(request, *args, **kwargs)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

class ReimbursementListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReimbursementRequestSerializer
    def get_queryset(self):
        return ReimbursementRequest.objects.filter(user=self.request.user).order_by('-submission_date')
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReimbursementDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return ReimbursementRequest.objects.filter(user=self.request.user)
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReimbursementRequestUpdateSerializer
        return ReimbursementRequestSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'rejected':
            return Response({"detail": "只有审核不通过的申请才能被修改。"}, status=status.HTTP_403_FORBIDDEN)
        response = super().update(request, *args, **kwargs)
        if response.status == 200:
            instance.status = 'pending'
            instance.rejection_reason = ""
            instance.save()
            response.data = ReimbursementRequestSerializer(instance).data
        return response

class NoticeListView(generics.ListAPIView):
    """获取所有启用的注意事项（无需认证）"""
    permission_classes = [AllowAny]
    serializer_class = NoticeSerializer
    
    def get_queryset(self):
        return Notice.objects.filter(is_active=True)
