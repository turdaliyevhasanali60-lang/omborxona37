from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from main.views import *

router = DefaultRouter()
router.register(r'products', ProductsView, basename='product')
router.register(r'clients', ClientsView, basename='client')
router.register(r'sells', SellsViewSet, basename='sell')
router.register(r'import-products', ImportProductsViewSet, basename='import-products')
router.register(r'debt-repayments', DebtRepaymentsViewSet, basename='debt-repayments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]