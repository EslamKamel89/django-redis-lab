from typing import TypedDict


class ProductData(TypedDict):
    product_id: int
    name: str
    quantity: int
    price: str


CartData = dict[str, ProductData]
