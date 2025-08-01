from typing import Optional, List
from ..domain.product import Product, FoodProduct, GroceryProduct


class ProductRepository:
    def __init__(self):
        self._products = {}

    def initialize_with_data(self, grocery_products: List[GroceryProduct]):
        self._products = {product.product_id: product for product in grocery_products}
        
        # Add some additional food products for testing
        food_products = {
            "food-1": FoodProduct(
                product_id="food-1",
                product_name="Margherita Pizza",
                mrp=18.99
            ),
            "food-2": FoodProduct(
                product_id="food-2",
                product_name="California Roll",
                mrp=12.99
            ),
            "food-3": FoodProduct(
                product_id="food-3",
                product_name="Classic Cheeseburger",
                mrp=14.99
            )
        }
        
        self._products.update(food_products)

    def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        return self._products.get(product_id)