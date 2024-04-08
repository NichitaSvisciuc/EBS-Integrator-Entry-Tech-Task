from django.contrib import admin
from products.models import Product, ProductHistory, ProductCategory


class ProductHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ['date_changed']


admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductHistory, ProductHistoryAdmin)
