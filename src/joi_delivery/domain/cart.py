from __future__ import annotations

from dataclasses import dataclass, field

from .outlet import Outlet
from .product import Product
from .user import User


@dataclass
class Cart:
    cart_id: str
    outlet: Outlet | None
    products: list[Product] = field(default_factory=list)
    user: User | None = None

    def to_json(self):
        return {
            "cart_id": self.cart_id,
            "outlet": self.outlet.to_json() if self.outlet else None,
            "products": [product.to_json() for product in self.products],
            "user": self.user.to_json() if self.user else None,
        }
