import json
from decimal import Decimal

from core.redis import redis_client

from .schemas import ProductData


def _cart_key(session_id: str) -> str:
    return f"cart:{session_id}"


def add_to_cart(product_data: ProductData):
    cart_key = _cart_key(product_data["session_id"])
    redis_client.hset(
        cart_key,
        str(product_data["product_id"]),
        json.dumps(product_data),
    )
    redis_client.expire(cart_key, 60 * 60 * 24)
