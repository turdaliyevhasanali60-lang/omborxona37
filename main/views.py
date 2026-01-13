from django.db.models import ExpressionWrapper, F
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import DecimalField
from .models import *


def home(request):
    return render(request, 'sections.html')

class SectionsView(View):
    def get(self, request):
        return render(request, 'sections.html')

class ProductsView(View):
    def get(self, request):
        products = Product.objects.annotate(
            value=ExpressionWrapper(
                F('quantity') * F('sell_price'),
                output_field=models.DecimalField()
            ),
        ).order_by(
            '-value'
        )
        context = {
            'products': products,
        }
        return render(request, 'products.html', context)

class AddProductView(View):
    def post(self, request):
        Product.objects.create(
            name=request.POST.get('name'),
            brand=request.POST.get('brand'),
            sell_price=request.POST.get('sell_price'),
            quantity=request.POST.get('quantity'),
            unit=request.POST.get('unit')
        )
        return redirect('products')

class ProductUpdateView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        context = {
            'product': product,
        }

        return render(request, 'product-update.html', context)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.name = request.POST.get('name')
        product.brand = request.POST.get('brand')
        product.buy_price = request.POST.get('buy_price') if request.POST.get('buy_price') != "" else None
        product.sell_price = request.POST.get('sell_price')
        product.quantity = request.POST.get('quantity')
        product.unit = request.POST.get('unit')
        product.save()
        return redirect('products')

class ProductDeleteView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        context = {
            'product': product,
        }
        return render(request, 'product-delete.html', context)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('products')

class ClientsView(View):
    def get(self, request):
        clients = Client.objects.order_by('name')
        context = {
            'clients': clients,
        }
        return render(request, 'clients.html', context)

class AddClientView(View):
    def post(self, request):
        Client.objects.create(
        name = request.POST.get('name'),
        shop_name = request.POST.get('shop_name'),
        phone_number = request.POST.get('phone_number'),
        address = request.POST.get('address'),
        )
        return redirect('clients')

class ClientUpdateView(View):
    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        context = {
            'client': client,
        }
        return render(request, 'client-update.html', context)

    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.name = request.POST.get('name')
        client.shop_name = request.POST.get('shop_name')
        client.phone_number = request.POST.get('phone_number')
        client.address = request.POST.get('address')
        client.save()
        return redirect('clients')

class ClientDeleteView(View):
    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        context = {
            'client': client,
        }
        return render(request, 'client-delete.html', context)

    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return redirect('clients')

class SellsView(View):
    def get(self, request):
        sells = Sell.objects.all()
        products = Product.objects.order_by('name')
        clients = Client.objects.order_by('name')
        context = {
            'sells': sells,
            'products': products,
            'clients': clients,
        }
        return render(request, 'sells.html', context)

    def post(self, request):
        product = get_object_or_404(Product, pk=request.POST.get('product_id'))
        client = get_object_or_404(Client, pk=request.POST.get('client_id'))
        quantity = float(request.POST.get('quantity')) if request.POST.get('quantity') != "" else None
        debt_price = float(request.POST.get('debt_price')) if request.POST.get('debt_price') != "" else None
        if product.quantity < quantity:
            pass


        sell = Sell.objects.create(
            product=product,
            client=client,
            quantity=quantity,
            total_price=request.POST.get('total_price'),
            paid_price=request.POST.get('paid_price'),
            debt_price=debt_price,
            details=request.POST.get('details'),
        )
        product.quantity -= quantity
        product.save()

        client.debt += debt_price
        client.save()

        return self.get(request)

class SellUpdateView(View):
    def get(self, request, pk):
        sell = get_object_or_404(Sell, pk=pk)

        products = Product.objects.order_by('name')
        clients = Client.objects.order_by('name')

        context = {
            'sell': sell,
            'products': products,
            'clients': clients,
        }
        return render(request, 'sell-update.html', context)

    def post(self, request, pk):
        sell = get_object_or_404(Sell, pk=pk)

        product = get_object_or_404(Product, pk=request.POST.get('product_id'))
        client = get_object_or_404(Client, pk=request.POST.get('client_id'))

        sell.product = product
        sell.client = client
        sell.quantity = request.POST.get('quantity')
        sell.total_price = request.POST.get('total_price')
        sell.paid_price = request.POST.get('paid_price')
        sell.debt_price = request.POST.get('debt_price')
        sell.details = request.POST.get('details')
        sell.save()
        return redirect('sells')



class ImportProductsView(View):
    def get(self, request):
        import_products = ImportProduct.objects.order_by('-created_at')
        products = Product.objects.order_by('name')
        context = {
            'import_products': import_products,
            'products': products,
        }
        return render(request, 'import-products.html', context)

    def post(self, request):
        product = get_object_or_404(Product, pk=request.POST.get('product_id'))
        ImportProduct.objects.create(
            product=product,
            quantity=request.POST.get('quantity'),
            buy_price=request.POST.get('buy_price'),
            details=request.POST.get('details'),
        )
        return self.get(request)

class ImportProductUpdateView(View):
    def get(self, request, pk):
        import_product = get_object_or_404(ImportProduct, pk=pk)
        products = Product.objects.order_by('name')
        context = {
            'import_product': import_product,
            'products': products,
        }
        return render(request, 'import-product-update.html', context)

    def post(self, request, pk):
        import_product = get_object_or_404(ImportProduct, pk=pk)
        import_product.product = get_object_or_404(Product, pk=request.POST.get('product_id'))
        import_product.quantity = request.POST.get('quantity')
        import_product.buy_price = request.POST.get('buy_price')
        import_product.details = request.POST.get('details')
        import_product.save()
        return redirect('import-products')


class ImportProductDeleteView(View):
    def get(self, request, pk):
        import_product = get_object_or_404(ImportProduct, pk=pk)
        context = {
            'import_product': import_product,
        }
        return render(request, 'import-product-delete.html', context)

    def post(self, request, pk):
        import_product = get_object_or_404(ImportProduct, pk=pk)
        import_product.delete()
        return redirect('import-products')




class DebtRepaymentView(View):
    def get(self, request):
        debt_repayments = DebtRepayment.objects.order_by('-created_at')
        clients = Client.objects.order_by('name')
        context = {
            'debt_repayments': debt_repayments,
            'clients': clients,
        }
        return render(request, 'debt-repayment.html', context)

    def post(self, request):
        client = get_object_or_404(Client, pk=request.POST.get('client_id'))
        DebtRepayment.objects.create(
            client=client,
            amount=request.POST.get('amount'),
            info=request.POST.get('info', '')
        )
        return redirect('debt-repayments')

class DebtRepaymentUpdateView(View):
    def get(self, request, pk):
        debt_repayment = get_object_or_404(DebtRepayment, pk=pk)
        context = {
            'debt_repayment': debt_repayment,
        }
        return render(request, 'debt-repayment-update.html', context)

    def post(self, request, pk):
        debt_repayment = get_object_or_404(DebtRepayment, pk=pk)
        old_amount = float(debt_repayment.amount)
        new_amount = float(request.POST.get('amount'))
        
        debt_repayment.info = request.POST.get('info', '')
        debt_repayment.amount = new_amount
        debt_repayment.save()
        client = debt_repayment.client
        client.debt += old_amount - new_amount
        client.save()

        # Adjust client debt by the difference
        debt_repayment.client.debt += old_amount - new_amount
        debt_repayment.client.save()

        return redirect('debt-repayments')

class DebtRepaymentDeleteView(View):
    def get(self, request, pk):
        debt_repayment = get_object_or_404(DebtRepayment, pk=pk)
        context = {
            'debt_repayment': debt_repayment,
        }
        return render(request, 'debt-repayment-delete.html', context)

    def post(self, request, pk):
        debt_repayment = get_object_or_404(DebtRepayment, pk=pk)
        debt_repayment.delete()
        return redirect('debt-repayments')