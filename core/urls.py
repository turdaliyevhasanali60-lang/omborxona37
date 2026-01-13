from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('sections/', SectionsView.as_view(), name='sections'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('add-product/', AddProductView.as_view(), name='add-product'),
    path('clients/', ClientsView.as_view(), name='clients'),
    path('add-client/', AddClientView.as_view(), name='add-client'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),
    path('sells/', SellsView.as_view(), name='sells'),
    path('sells/<int:pk>/update/', SellUpdateView.as_view(), name='sell-update'),
    path('import-products/', ImportProductsView.as_view(), name='import-products'),
    path('import-products/<int:pk>/update/', ImportProductUpdateView.as_view(), name='import-product-update'),
    path('import-products/<int:pk>/delete/', ImportProductDeleteView.as_view(), name='import-product-delete'),
    path('debt-repayments/', DebtRepaymentView.as_view(), name='debt-repayments'),
    path('debt-repayments/<int:pk>/update/', DebtRepaymentUpdateView.as_view(), name='debt-repayment-update'),
    path('debt-repayments/<int:pk>/delete/', DebtRepaymentDeleteView.as_view(), name='debt-repayment-delete')
]
