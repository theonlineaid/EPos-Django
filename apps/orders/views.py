# apps/orders/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from apps.products.models import Product
from .serializers import OrderSerializer
from datetime import datetime
from .serializers import ProductSerializer


# class OrderCreateView(generics.CreateAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]


class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.filter(customer=self.request.user) \
            .select_related('customer') \
            .prefetch_related('items__product')

        category = self.request.query_params.get('category')
        product = self.request.query_params.get('product')
        sales_date = self.request.query_params.get('date')

        if category:
            queryset = queryset.filter(items__product__category__id=category)
        if product:
            queryset = queryset.filter(items__product__id=product)
        if sales_date:
            try:
                date_obj = datetime.strptime(sales_date, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date=date_obj)
            except ValueError:
                pass  # optionally raise a validation error

        return queryset


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.filter(customer=self.request.user) \
            .select_related('customer') \
            .prefetch_related('items__product')

        category = self.request.query_params.get('category')
        product = self.request.query_params.get('product')
        sales_date = self.request.query_params.get('date')

        if category:
            queryset = queryset.filter(items__product__category__id=category)
        if product:
            queryset = queryset.filter(items__product__id=product)
        if sales_date:
            try:
                date_obj = datetime.strptime(sales_date, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date=date_obj)
            except ValueError:
                pass  # optionally raise a validation error

        return queryset


class OrderInvoiceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, customer=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)

        # Build invoice-like data
        invoice_data = {
            "order_id": order.id,
            "status": order.status,
            "customer": order.customer.username,
            "date": order.created_at,
            "items": [
                {
                    "product": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": item.product.price,
                    "total_price": item.product.price * item.quantity
                }
                for item in order.items.all()
            ],
            "total_amount": sum(
                item.product.price * item.quantity for item in order.items.all()
            )
        }

        return Response(invoice_data)


class ProductStockView(generics.ListAPIView):
    queryset = Product.objects.all()  # Fetch all products
    serializer_class = ProductSerializer  # You need to define a Product serializer
    # Only authenticated users can view the stock
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Override the list method to include the stock in the response
        products = self.get_queryset()
        stock_data = []

        for product in products:
            stock_data.append({
                'product_id': product.id,
                'product_name': product.name,
                'stock_quantity': product.stock_quantity,
            })

        return Response(stock_data)
