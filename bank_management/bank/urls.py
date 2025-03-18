# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, UserLimitViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'user-limits', UserLimitViewSet, basename='user-limits')
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    path('api/', include(router.urls)),
    path('auth-api/', include('rest_framework.urls', namespace='rest_framework')),
]
