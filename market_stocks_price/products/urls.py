from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, ProductCategoryViewSet


router = DefaultRouter()
router.register(r'items', ProductViewSet, basename='items')
router.register(r'categories', ProductCategoryViewSet, basename='categories')


urlpatterns = [
    path(
        'items/<int:pk>/price_calculation',
        ProductViewSet.as_view({'get': 'price_calculation'}),
        name='items-price-calculation'
    ),
    path(
        'items/<int:pk>/change_price_for_time_period',
        ProductViewSet.as_view({'post': 'change_price_for_time_period'}),
        name='change-price-for-time-period'
    ),
    path(
        'categories/<int:pk>/change_category_price',
        ProductCategoryViewSet.as_view({'post': 'change_category_price'}),
        name='change-category-price'
    ),
    path(
        'categories/<int:pk>/category_price_calculation',
        ProductCategoryViewSet.as_view({'get': 'category_price_calculation'}),
        name='category-price-calculation'
    )
] + router.urls
