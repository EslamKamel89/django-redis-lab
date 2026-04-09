import json
from typing import Optional, cast

from core.redis import redis_client

from .schemas import CartData, ProductData


def get_cart_key(session_id: str) -> str:
    return f"cart:{session_id}"


def add_to_cart(product_data: ProductData, session_id: str) -> None:
    cart_key = get_cart_key(session_id)
    field = str(product_data["product_id"])
    existing = cast(Optional[str], redis_client.hget(cart_key, field))
    if existing:
        existing_data = cast(ProductData, json.loads(existing))
        product_data["quantity"] += existing_data["quantity"]
    assert product_data["quantity"] > 0
    redis_client.hset(
        cart_key,
        field,
        json.dumps(product_data),
    )
    redis_client.expire(cart_key, 60 * 60 * 24)


def get_cart(session_id: str) -> CartData:
    cart_key = get_cart_key(session_id)
    res = cast(dict, redis_client.hgetall(cart_key))
    cart: CartData = {}
    for product_id, product_str in res.items():
        cart[product_id] = cast(ProductData, json.loads(product_str))
    return cart


def remove_from_cart(session_id: str, product_id: str) -> None:
    cart_key = get_cart_key(session_id)
    redis_client.hdel(cart_key, product_id)
