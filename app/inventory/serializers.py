from inventory.models import Category, Product
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "level"]


class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    category_data = CategorySerializer(source="category", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "category", "category_data"]
        read_only_fields = ["id", "category_data"]
