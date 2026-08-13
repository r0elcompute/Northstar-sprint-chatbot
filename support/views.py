from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .serializers import OrderSerializer

# Import the AI Lead's function
from .ai_automation import generate_response


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


class ChatAPIView(APIView):
    """
    Endpoint for AI/Automation layer to process user chat messages and order context.
    """
    def post(self, request):
        message = request.data.get("message")
        order_id = request.data.get("order_id")

        if not message:
            return Response(
                {"error": "The 'message' field is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Pass payload to the AI Lead's generator function
            ai_reply = generate_response(message=message, order_id=order_id)
            
            return Response({
                "success": True,
                "reply": ai_reply
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": f"Failed to generate AI response: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)