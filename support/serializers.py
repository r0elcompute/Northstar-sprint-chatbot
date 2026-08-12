from rest_framework import serializers
from .models import Customer, Product, Order, Return

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'email', 'phone']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'category', 'size', 'price', 'stock_quantity']


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = ['return_id', 'reason', 'return_status', 'refund_status', 'refund_amount', 'requested_at', 'completed_at']


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    returns = ReturnSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'customer', 'product', 'quantity', 'status', 'expected_delivery', 'order_date', 'returns']