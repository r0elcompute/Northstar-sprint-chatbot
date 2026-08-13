from django.contrib import admin
from .models import Customer, Product, Order, Return
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'category', 'price', 'stock_quantity')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'product', 'quantity', 'status', 'expected_delivery')
    list_filter = ('status',)
    search_fields = ('order_id', 'customer__name', 'customer__email')

@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ('return_id', 'order', 'reason', 'return_status', 'refund_status', 'refund_amount')
    list_filter = ('return_status', 'refund_status')