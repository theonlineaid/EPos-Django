# apps/orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.models import Product


class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value

    def validate(self, data):
        product = Product.objects.filter(id=data['product_id']).first()
        if product and product.stock_quantity < data['quantity']:
            raise serializers.ValidationError(
                f"Not enough stock for product '{product.name}'. Available: {product.stock_quantity}")
        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    items_detail = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status',
                  'created_at', 'items', 'items_detail']
        read_only_fields = ['customer']

    def get_items_detail(self, obj):
        return [{
            'product_id': item.product.id,
            'product_name': item.product.name,
            'quantity': item.quantity
        } for item in obj.items.all()]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # You already get the customer from the request user
        customer = self.context['request'].user
        # Do not pass 'customer' here
        order = Order.objects.create(**validated_data)

        # Proceed with creating the order items and updating stock
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])

            # Create the order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity']
            )

            # Update stock
            product.stock_quantity -= item_data['quantity']
            product.save()

        return order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'stock_quantity']
