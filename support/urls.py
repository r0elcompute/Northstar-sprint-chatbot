from django.urls import path
from .views import OrderDetailView

urlpatterns = [
    path('orders/<str:order_id>/', OrderDetailView.as_view(), name='order-detail'),
]