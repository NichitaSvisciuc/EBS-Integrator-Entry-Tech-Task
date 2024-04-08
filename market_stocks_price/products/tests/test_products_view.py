import random

from functools import reduce

from rest_framework.test import (
    APITestCase,
    APIClient,
)

from django.shortcuts import reverse

from products.models import Product, ProductCategory, ProductHistory


api_client = APIClient()


class TestProductViewSet(APITestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(code='test_category')
        self.product = Product.objects.create(
            name='test_product',
            category=self.category,
            sku=0,
            description='Test',
            price=10.00,
        )

        self.products_price_calculation_url = 'items-price-calculation'
        self.change_price_for_time_period_url = 'change-price-for-time-period'

    def create_mock_any_product_history(self):
        for i in range(0, 10):
            ProductHistory.objects.create(
                product=self.product,
                old_price=random.randint(0, 10),
                date_changed=f'2024-04-{random.randint(0, 31)}'
            )

    def create_mock_product_history(self):
        for i in range(0, 10):
            ProductHistory.objects.create(
                product=self.product,
                old_price=10,
                date_changed=f'2024-04-08'
            )

    def test_products_price_calculation(self):
        self.create_mock_product_history()
        response = self.client.get(
            reverse(
                self.products_price_calculation_url, kwargs={"pk": self.product.pk}
            ) + "?start_date=2024-04-08&end_date=2024-04-08",
        )
        self.assertEqual(response.data['price_interval'], 10.0)

    def test_change_price_for_time_period(self):
        self.create_mock_product_history()
        response = self.client.post(
            reverse(
                self.change_price_for_time_period_url, kwargs={"pk": self.product.pk}
            ) + "?start_date=2024-04-08&end_date=2024-04-08",
            {"price": 300}
        )
        product_history_old_prices = [product_history.old_price for product_history in ProductHistory.objects.all()]
        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            reduce(lambda x, y: x + y, product_history_old_prices) / len(product_history_old_prices),
            300.00
        )
