from abc import ABC
from dataclasses import dataclass


@dataclass
class Product(ABC):
    product_id: str
    product_name: str
    mrp: float

    def to_json(self):
        return {"product_id": self.product_id, "product_name": self.product_name, "mrp": self.mrp}
