from typing import Optional
from ..repository.product_repository import ProductRepository
from ..domain.product import GroceryProduct


class ProductService:
    @staticmethod
    def get_product(product_repository: ProductRepository, product_id: str, outlet_id: str) -> Optional[GroceryProduct]:
        product = product_repository.get_product(product_id)
        if (isinstance(product, GroceryProduct) and 
            product.store and 
            product.store.outlet_id == outlet_id):
            return product
        return None 