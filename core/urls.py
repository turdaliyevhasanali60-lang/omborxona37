from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sections/', SectionsView.as_view(), name='sections'),
    path('products/', ProductsView.as_view(), name='products'),
    path('clients/', ClientsView.as_view(), name='clients'),
]
