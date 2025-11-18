from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cart import Cart


@dataclass
class User:
    user_id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    cart: Cart | None = None
    username: str | None = None

    def to_json(self):
        return {
            "user_id": self.user_id,
            "username": self.username or "",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "cart": self.cart.to_json() if self.cart else None,
        }
