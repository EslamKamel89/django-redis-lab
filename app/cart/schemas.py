from typing import TypedDict


class ProductData(TypedDict):
    session_id: str
    product_id: int
    name: str
    quantity: int
    price: str
