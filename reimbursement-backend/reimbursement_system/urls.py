# reimbursement_system/urls.py
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from reimbursement.views import UserRegistrationView, RestrictedTokenObtainPairView
from reimbursement.admin_site import restricted_admin_site

urlpatterns = [
    path('admin/', restricted_admin_site.urls),
    path('api/token/', RestrictedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', UserRegistrationView.as_view(), name='user_register'),
    path('api/reimbursements/', include('reimbursement.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)