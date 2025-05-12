# product/views.py

from rest_framework import generics, filters, permissions
from rest_framework.generics import CreateAPIView
from .models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from .permissions import IsAdminOnly, IsSellerOnly
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOnly]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # anyone can view
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name']


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    # Allow admins and sellers to create products
    permission_classes = [IsAdminOnly | IsSellerOnly]

    def perform_create(self, serializer):
        user = self.request.user
        # If the user is a seller, automatically assign them as the seller
        if user.user_type == 'seller':
            serializer.save(seller=user)
        else:
            # Admins will not set a seller for the product
            serializer.save(seller=None)


class ReviewCreateView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        product_id = self.request.data.get("product")
        product = get_object_or_404(Product, id=product_id)
        serializer.save(customer=self.request.user, product=product)
