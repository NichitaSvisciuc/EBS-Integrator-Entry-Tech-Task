from products.models import Product, ProductCategory

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'sku', 'description', 'price']


class ProductPriceSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=100, decimal_places=2)

    class Meta:
        fields = ['price']


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'code']
