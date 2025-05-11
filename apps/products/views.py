# product/views.py

from rest_framework import generics, filters
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import IsAdminOnly, IsSellerOnly
from rest_framework.permissions import AllowAny


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
