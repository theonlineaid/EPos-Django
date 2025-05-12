from django.db import models
from apps.products.models import Product


class StockUpdate(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
