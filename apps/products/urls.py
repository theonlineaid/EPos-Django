# product/urls.py

from django.urls import path
from .views import ProductListView, ProductCreateView, CategoryListCreateView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(),
         name='category-list-create'),
    path('', ProductListView.as_view(), name='product-list'),
    path('product/', ProductCreateView.as_view(), name='product-create'),
]
