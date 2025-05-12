# product/serializers.py

from rest_framework import serializers
from .models import Product, Category, Review
from apps.users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.SerializerMethodField()  # Custom field for seller info

    class Meta:
        model = Product
        fields = ['id', 'name', 'category',
                  'stock_quantity', 'price', 'seller']

    def get_seller(self, obj):
        # Only return seller info if the user is a seller or if it's an admin view
        user = self.context['request'].user
        if user.user_type == 'seller' and obj.seller == user:
            return {
                'id': obj.seller.id,
                'username': obj.seller.username
            }
        return None  # Admins or others will not see the seller field in the response

    def create(self, validated_data):
        user = self.context['request'].user
        # Assign seller if user is seller, else set seller to None for admin
        if user.user_type == 'seller':
            validated_data['seller'] = user
        else:
            validated_data['seller'] = None

        # Create the product and return it
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'customer', 'product',
                  'rating', 'comment', 'created_at']
        # Make sure customers cannot modify 'customer' or 'product' fields
        read_only_fields = ['customer', 'product', 'created_at']
