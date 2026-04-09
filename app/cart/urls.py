from django.urls import URLPattern, path

from .views import AddToCartView

urlpatterns: list[URLPattern] = [path("cart/", AddToCartView.as_view(), name="cart")]
