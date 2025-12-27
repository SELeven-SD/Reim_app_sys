# reimbursement/urls.py
from django.urls import path
from .views import (
    ReimbursementListCreateView, 
    ReimbursementDetailView, 
    NoticeListView
)

urlpatterns = [
    path('', ReimbursementListCreateView.as_view(), name='reimbursement-list-create'),
    path('<int:pk>/', ReimbursementDetailView.as_view(), name='reimbursement-detail'),
    path('notices/', NoticeListView.as_view(), name='notice-list'),
]
