from typing import cast

from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from inventory.models import Product
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .redis_cart import add_to_cart
from .schemas import ProductData
from .serializers import AddToCartSerializer


class AddToCartView(APIView):
    @extend_schema(request=AddToCartSerializer)
    def post(self, request: Request):
        session: SessionBase = request.session
        if not session.session_key:
            session.save()
        session_id = session.session_key
        serializer = AddToCartSerializer(data=request.data)
        # for now i just return the valid data or error later i will implement the add to cart functionality
        if serializer.is_valid():
            validated_data = cast(dict, serializer.validated_data)
            product = Product.objects.filter(id=validated_data["product_id"]).first()
            if product is None:
                return Response(
                    {"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )
            product_data = ProductData(
                **{
                    **validated_data,
                    "session_id": session_id,
                    "name": product.name,
                    "price": str(product.price),
                }
            )
            add_to_cart(product_data)
            return Response(product_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
