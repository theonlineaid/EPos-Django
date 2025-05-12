# apps/orders/urls.py
from django.urls import path
from .views import OrderCreateView, OrderHistoryView, OrderInvoiceView, ProductStockView

urlpatterns = [
    path('place/', OrderCreateView.as_view(), name='place-order'),
    path('history/', OrderHistoryView.as_view(), name='order-history'),
    path('invoice/<int:pk>/', OrderInvoiceView.as_view(), name='order-invoice'),
    path('stock/', ProductStockView.as_view(), name='stock-list'),
]
