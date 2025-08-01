from dataclasses import dataclass, field
from typing import Set
from .outlet import Outlet
from .product import GroceryProduct


@dataclass
class GroceryStore(Outlet):
    inventory: Set[GroceryProduct] = field(default_factory=set)

    def to_json(self):
        base_json = super().to_json()
        base_json.update({
            "inventory": [product.to_json() for product in self.inventory]
        })
        return base_json

@dataclass
class Restaurant(Outlet):
    pass 