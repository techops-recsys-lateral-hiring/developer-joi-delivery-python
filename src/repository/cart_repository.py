from typing import Optional, List, Dict
from datetime import datetime
from ..domain.cart import Cart
from ..domain.user import User
from ..domain.outlet import Outlet
from ..domain.store import GroceryStore, Restaurant


class CartRepository:
    def __init__(self):
        self._carts: Dict[str, Cart] = {}

    def initialize_with_data(self, carts: Dict[str, Cart]):
        self._carts = carts

    def get_cart_by_user(self, user_id: str) -> Optional[Cart]:
        for cart in self._carts.values():
            if cart.user and cart.user.user_id == user_id:
                return cart
        return None 