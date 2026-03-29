from django.urls import URLPattern, path

from .views import ProductListCreateApiView

urlpatterns: list[URLPattern] = [
    path(
        "products/",
        ProductListCreateApiView.as_view(),
        name="product-list-create",
    ),
]
