import logging
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .serializers import OrderSerializer
from automation.intent import generate_response, classify_intent_and_order
logger = logging.getLogger(__name__)


class OrderDetailView(APIView):
    """
    Endpoint for AI/Automation layer to retrieve order & return data by Order ID.
    """
    def get(self, request, order_id):
        try:
            # Retrieve order along with related customer, product, and returns
            order = Order.objects.select_related('customer', 'product') \
                                 .prefetch_related('returns') \
                                 .get(order_id=order_id)
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
    Endpoint for AI/Automation layer to process user chat messages with full ORM context.
    """
    def post(self, request):
        message = request.data.get("message", "").strip()
        passed_order_id = request.data.get("order_id")

        if not message:
            return Response(
                {"error": "The 'message' field is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 1. Detect order_id from payload or via AI intent parser
            order_id = passed_order_id
            if not order_id:
                analysis = classify_intent_and_order(message)
                order_id = analysis.get("order_id")

            # 2. Query Django ORM if an order_id was found
            order_data = None
            if order_id:
                try:
                    order = Order.objects.select_related('customer', 'product') \
                                         .prefetch_related('returns') \
                                         .get(order_id=order_id)
                    serializer = OrderSerializer(order)
                    order_data = serializer.data
                except Order.DoesNotExist:
                    order_data = {"error": f"Order #{order_id} was not found in our database."}

            # 3. Generate natural, context-aware Gemini response.
            # Keep only the AI's human text in the reply field; never send raw database dictionaries.
            ai_reply = generate_response(message, order_data=order_data)

            if isinstance(ai_reply, dict):
                ai_reply = ai_reply.get("reply") or ai_reply.get("response") or ai_reply.get("text") or ""
            elif ai_reply is None:
                ai_reply = "Thanks for reaching out. I’m checking your order details and will get back to you shortly."

            cleaned_reply = str(ai_reply).strip()
            if not cleaned_reply:
                cleaned_reply = "Thanks for reaching out. I’m checking your order details and will get back to you shortly."

            return Response({
                "success": True,
                "reply": cleaned_reply
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"ChatAPIView Error: {str(e)}", exc_info=True)
            return Response({
                "success": False,
                "error": "The AI service encountered an issue. Please try again."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)