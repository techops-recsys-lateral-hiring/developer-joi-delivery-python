from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .product import Product

if TYPE_CHECKING:
    from .grocery_store import GroceryStore


@dataclass
class GroceryProduct(Product):
    weight: float
    threshold: int
    available_stock: int
    store: GroceryStore | None = None
    selling_price: float | None = None
    expiry_date: int | None = None
    discount: float | None = None

    def to_json(self):
        base_json = super().to_json()
        base_json.update(
            {
                "selling_price": self.selling_price,
                "weight": self.weight,
                "expiry_date": self.expiry_date,
                "threshold": self.threshold,
                "available_stock": self.available_stock,
                "discount": self.discount,
                "store": self.store.to_json() if self.store else None,
                "product_type": "grocery",
            }
        )
        return base_json
