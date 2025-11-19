from dataclasses import dataclass, field
from typing import Set
from .outlet import Outlet
from .food_product import FoodProduct


@dataclass
class Restaurant(Outlet):
    pass
