from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer

class OrderDetailView(APIView):
    """
    Endpoint for AI/Automation layer to retrieve order & return data by Order ID.
    """
    def get(self, request, order_id):
        try:
            # Retrieve order along with related customer, product, and returns
            order = Order.objects.select_related('customer', 'product').prefetch_related('returns').get(order_id=order_id)
            serializer = OrderSerializer(order)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Order.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Order with ID '{order_id}' not found."
            }, status=status.HTTP_404_NOT_FOUND)