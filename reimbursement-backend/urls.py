# reimbursement/urls.py
from django.urls import path
from .views import ReimbursementListCreateView, ReimbursementDetailView

urlpatterns = [
    # POST: 创建申请; GET: 获取当前用户的所有申请列表
    path('', ReimbursementListCreateView.as_view(), name='reimbursement-list-create'),
    # GET: 获取单条申请详情; PUT/PATCH: 更新; DELETE: 删除
    path('<int:pk>/', ReimbursementDetailView.as_view(), name='reimbursement-detail'),
]

# 项目主urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT认证接口
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 报销应用的API
    path('api/reimbursements/', include('reimbursement.urls')),
]

# 在开发环境中服务媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)