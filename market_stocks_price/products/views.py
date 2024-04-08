from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body

from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer, ProductPriceSerializer


start = openapi.Parameter(
    'start_date', openapi.IN_QUERY,
    description="Start date : Manual query parameter defined as ?start_date=%Y-%m-%d", type=openapi.FORMAT_DATE
)
end = openapi.Parameter(
    'end_date', openapi.IN_QUERY,
    description="End date : Manual query parameter defined as ?end_date=%Y-%m-%d", type=openapi.FORMAT_DATE
)


class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    @swagger_auto_schema(
        request_body=ProductPriceSerializer,
        responses={status.HTTP_204_NO_CONTENT: ''}
    )
    @action(
        methods=['post'],
        detail=True,
        url_path=r"change_category_price",
        url_name='change_category_price'
    )
    def change_category_price(self, request, pk):
        instance = self.get_queryset().get(pk=pk)
        instance.change_category_price(price=request.data['price'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        manual_parameters=[start, end],
        request_body=no_body,
        responses={status.HTTP_200_OK: 'category_price_interval'}
    )
    @action(
        methods=['get'],
        detail=True,
        url_path=r"category_price_calculation",
        url_name='category_price_calculation'
    )
    def category_price_calculation(self, request, pk):
        instance = self.get_queryset().get(pk=pk)
        return Response({"category_price_interval": instance.get_category_price_interval(
            start_date=request.GET.get('start_date'),
            end_date=request.GET.get('end_date')
        )})


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        manual_parameters=[start, end],
        request_body=no_body,
        responses={status.HTTP_200_OK: 'price_interval'}
    )
    @action(
        methods=['get'],
        detail=True,
        url_path=r"price_calculation",
        url_name='price_calculation'
    )
    def price_calculation(self, request, pk):
        instance = self.get_queryset().get(pk=pk)
        return Response({"price_interval": instance.get_price_interval(
            start_date=request.GET.get('start_date'),
            end_date=request.GET.get('end_date')
        )})

    @swagger_auto_schema(
        manual_parameters=[start, end],
        request_body=ProductPriceSerializer,
        responses={status.HTTP_204_NO_CONTENT: ''}
    )
    @action(
        methods=['post'],
        detail=True,
        url_path=r"change_price_for_time_period",
        url_name='change_price_for_time_period'
    )
    def change_price_for_time_period(self, request, pk):
        instance = self.get_queryset().get(pk=pk)
        instance.change_price_interval(
            price=request.data['price'],
            start_date=request.GET.get('start_date'),
            end_date=request.GET.get('end_date')
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
