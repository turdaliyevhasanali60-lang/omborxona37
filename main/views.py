from email._header_value_parser import Section
from django.shortcuts import render
from django.views import View
from .models import *

class SectionsView(View):
    def get(self, request):
        return render(request, 'sections.html')

class ProductsView(View):
    def get(self, request):
        return render(request, 'products.html')

class ClientsView(View):
    def get(self, request):
        return render(request, 'clients.html')