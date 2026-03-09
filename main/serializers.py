from rest_framework import serializers
from .models import *

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

        extra_kwargs = {'branch': {'read_only': True}, 'debt': {'read_only': True}}

class ImportProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportProduct
        fields = '__all__'

        extra_kwargs = {'branch': {'read_only': True}}

class DebtRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtRepayment
        fields = '__all__'
        extra_kwargs = {
            'branch': {'read_only': True},
            'user': {'read_only': True},
        }

class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = '__all__'

        extra_kwargs = {
                        'branch': {'read_only': True},
                        'user': {'read_only': True},
                        }