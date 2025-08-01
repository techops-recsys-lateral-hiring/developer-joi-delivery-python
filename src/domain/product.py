from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional


@dataclass
class Product(ABC):
    product_id: str
    product_name: str
    mrp: float

    def to_json(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "mrp": self.mrp
        }


@dataclass
class FoodProduct(Product):
    pass


@dataclass
class GroceryProduct(Product):
    selling_price: float
    weight: float
    expiry_date: int
    threshold: int
    available_stock: int
    discount: float
    store: Optional['GroceryStore'] = None

    def to_json(self):
        base_json = super().to_json()
        base_json.update({
            "selling_price": self.selling_price,
            "weight": self.weight,
            "expiry_date": self.expiry_date,
            "threshold": self.threshold,
            "available_stock": self.available_stock,
            "discount": self.discount,
            "store": self.store.to_json() if self.store else None,
            "product_type": "grocery"
        })
        return base_json
