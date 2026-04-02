from django.urls import URLPattern, path

from .views import AddToCartView

urlpatterns: list[URLPattern] = [
    path("cart/add/", AddToCartView.as_view(), name="add-to-cart")
]
