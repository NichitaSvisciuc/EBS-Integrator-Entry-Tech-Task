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
        self.product_1 = Product.objects.create(
            name='test_product_1',
            category=self.category,
            sku=0,
            description='Test',
            price=10.00,
        )
        self.product_2 = Product.objects.create(
            name='test_product_2',
            category=self.category,
            sku=0,
            description='Test',
            price=10.00,
        )

        self.change_category_price_url = 'change-category-price'
        self.category_price_calculation_url = 'category-price-calculation'

    def create_mock_any_products_history(self):
        for product in (self.product_1, self.product_2):
            for i in range(0, 10):
                ProductHistory.objects.create(
                    product=product,
                    old_price=random.randint(0, 10),
                    date_changed=f'2024-04-{random.randint(0, 31)}'
                )

    def create_mock_products_history(self):
        for product in (self.product_1, self.product_2):
            for i in range(0, 10):
                ProductHistory.objects.create(
                    product=product,
                    old_price=10,
                    date_changed=f'2024-04-08'
                )

    def test_change_category_price(self):
        self.create_mock_products_history()
        response = self.client.post(
            reverse(
                self.change_category_price_url, kwargs={"pk": self.category.pk}
            ),
            {"price": 300}
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            float(reduce(lambda x, y: x + y, (p.price for p in Product.objects.all())) / Product.objects.all().count()),
            300.00
        )

    def test_category_price_calculation(self):
        self.create_mock_products_history()
        response = self.client.get(
            reverse(
                self.category_price_calculation_url, kwargs={"pk": self.category.pk}
            ) + "?start_date=2024-04-08&end_date=2024-04-08",
        )
        self.assertEqual(
            response.data['category_price_interval'],
            10.0
        )
