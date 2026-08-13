from django.urls import path
from .views import OrderDetailView, ChatAPIView

urlpatterns = [
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('chat/', ChatAPIView.as_view(), name='support-chat'),
]