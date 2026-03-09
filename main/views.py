# main/views.py
from rest_framework.viewsets import ModelViewSet
from .serializers import *

class ProductsView(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

class ClientsView(ModelViewSet):
    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)


class SellsViewSet(ModelViewSet):
    serializer_class = SellSerializer

    def get_queryset(self):
        return Sell.objects.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        sell = serializer.save(branch=self.request.user.branch, user=self.request.user)
        sell.product.quantity -= sell.quantity
        sell.product.save()
        sell.client.debt += sell.debt_price
        sell.client.save()


class ImportProductsViewSet(ModelViewSet):
    serializer_class = ImportProductSerializer

    def get_queryset(self):
        return ImportProduct.objects.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch, user=self.request.user)


class DebtRepaymentsViewSet(ModelViewSet):
    serializer_class = DebtRepaymentSerializer

    def get_queryset(self):
        return DebtRepayment.objects.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch, user=self.request.user)

    def perform_update(self, serializer):
        old_amount = serializer.instance.amount
        instance = serializer.save()
        instance.client.debt += old_amount - instance.amount
        instance.client.save()