from django.shortcuts import render
from inventory.models import Product
from inventory.serializers import ProductSerializer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProductListCreateApiView2(APIView):
    def get(self, request: Request):
        products = Product.objects.select_related("category").all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListCreateApiView(ListCreateAPIView):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
