import datetime

from typing import Tuple, Any
from functools import reduce

from django.db import models
from django.db.models import DecimalField, Q, Avg
from django.db.models.functions import Cast


class ProductCategory(models.Model):
    code = models.CharField(max_length=255)

    def change_category_price(self, price):
        # Not using the 'self.products.all().update(price=price)'
        # as we need to access the save() method
        # to create a new price history
        for product in self.products.all():
            product.price = price
            product.save()

    def get_category_price_interval(self, start_date, end_date):
        category_products_avg_prices = [
            product.get_price_interval(start_date, end_date) for product in self.products.all()
        ]
        return reduce(lambda x, y: x + y, category_products_avg_prices) / len(category_products_avg_prices)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "ProductCategory"
        verbose_name_plural = "ProductCategory's"


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    sku = models.IntegerField(default=0)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        updated, old_instance = self.get_instance_price_updated()
        if updated:
            ProductHistory.objects.create(
                product=self, old_price=old_instance.price, date_changed=datetime.date.today()
            )
        return super().save(*args, **kwargs)

    def get_instance_price_updated(self) -> Tuple[bool, Any]:
        # Checking if the object price changed and returning the bool statement along with the object
        # (in case in changed its price)
        old_instance = Product.objects.filter(pk=self.pk)
        if old_instance.exists():
            if self.price != old_instance.first().price:
                return True, old_instance.first()
        return False, None

    def set_price(self, price):
        self.price = price
        self.save()

    def get_price_interval(self, start_date, end_date) -> float:
        return float(self.product_history.filter(
            Q(date_changed__gte=start_date) & Q(date_changed__lte=end_date)
        ).annotate(
            old_price_decimal=Cast('old_price', DecimalField())
        ).aggregate(avg_value=Avg('old_price_decimal'))['avg_value'])

    def change_price_interval(self, price, start_date, end_date) -> int:
        # Returning the number of products found in history and price changed
        return self.product_history.filter(
            Q(date_changed__gte=start_date) & Q(date_changed__lte=end_date)
        ).update(old_price=price)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Product's"


class ProductHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_history')
    old_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    date_changed = models.DateField(auto_created=True)

    def __str__(self):
        return f"{self.product.name} - {self.product.category.code} : logged price from : {self.date_changed}"

    class Meta:
        verbose_name = "ProductHistory"
        verbose_name_plural = "ProductHistory's"
