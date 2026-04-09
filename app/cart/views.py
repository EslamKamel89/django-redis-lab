from typing import cast

from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render
from drf_spectacular.utils import OpenApiParameter, extend_schema
from inventory.models import Product
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .redis_cart import add_to_cart, get_cart, remove_from_cart
from .schemas import ProductData
from .serializers import AddToCartSerializer, CartSerializer, RemoveFromCartSerializer


class AddToCartView(APIView):
    def get_session_id(self, request: Request) -> str:
        session: SessionBase = request.session
        if not session.session_key:
            session.save()
        session_id = session.session_key
        assert session_id is not None
        return session_id

    @extend_schema(request=AddToCartSerializer)
    def post(self, request: Request):
        session_id = self.get_session_id(request)
        serializer = AddToCartSerializer(data=request.data)
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
                    "name": product.name,
                    "price": str(product.price),
                }
            )
            add_to_cart(product_data, session_id)
            return Response(product_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: CartSerializer()},
        description="Get all cart items for the current session",
    )
    def get(self, request: Request):
        session_id = self.get_session_id(request)
        cart = get_cart(session_id)
        serializer = CartSerializer({"items": list(cart.values())})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="delete specific product by id from the cart",
        parameters=[
            OpenApiParameter(
                name="product_id", location="query", type=int, required=True
            )
        ],
    )
    def delete(self, request: Request):
        product_id = request.query_params.get("product_id")
        if product_id is None:
            return Response(
                {"product_id": "This query param is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        session_id = self.get_session_id(request)
        serializer = RemoveFromCartSerializer(data={"product_id": product_id})
        if serializer.is_valid():
            validated_data = cast(dict, serializer.validated_data)
            remove_from_cart(session_id, str(validated_data["product_id"]))
            return Response({"message": "Product removed from the cart"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
