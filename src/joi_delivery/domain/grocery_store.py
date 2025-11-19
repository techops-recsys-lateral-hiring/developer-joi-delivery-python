from __future__ import annotations

from dataclasses import dataclass, field

from .grocery_product import GroceryProduct
from .outlet import Outlet


@dataclass
class GroceryStore(Outlet):
    inventory: set[GroceryProduct] = field(default_factory=set)

    def to_json(self):
        base_json = super().to_json()
        base_json.update({"inventory": [product.to_json() for product in self.inventory]})
        return base_json
