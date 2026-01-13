from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    buy_price = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)])
    sell_price = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    debt = models.FloatField(default=0, validators=[MinValueValidator(0)])

    created_at = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Sell(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)

    details = models.TextField(blank=True, null=True)

    total_price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    paid_price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    debt_price = models.FloatField(default=0, validators=[MinValueValidator(0)])

    created_at = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f'{self.client} -- {self.product}'


class ImportProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)
    buy_price = models.FloatField(validators=[MinValueValidator(0)])
    details = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.product} -- {self.quantity} {self.product.unit}'

    def total_price(self):
        try:
            return self.buy_price * self.quantity
        except:
            return None
    def save(self, *args, **kwargs):
        self.product.buy_price = self.buy_price
        self.product.quantity += float(self.quantity)
        self.product.save()
        super().save(*args, **kwargs)

class DebtRepayment(models.Model):
    info = models.TextField()
    amount = models.FloatField()
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.amount}'

    def save(self, *args, **kwargs):
        self.client.debt -= float(self.amount)
        self.client.save()
        super().save(*args, **kwargs)

class Action (models.Model):
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.text}'
