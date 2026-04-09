from rest_framework import serializers


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1, default=1)


class CartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.CharField()
    quantity = serializers.IntegerField()


class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)


class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
