from fastapi import HTTPException

from ..controller.models import InventoryHealthResponse, InventoryProductHealth
from ..domain.grocery_product import GroceryProduct
from ..domain.grocery_store import GroceryStore


class InventoryService:
    def __init__(self, products: list[GroceryProduct], stores: list[GroceryStore]):
        self.products = products
        self.stores = stores

    def get_inventory_health(self, store_id: str) -> InventoryHealthResponse:
        store = self._get_store_by_id(store_id)
        if store is None:
            raise HTTPException(status_code=404, detail=f"Store not found for store_id={store_id}")

        store_products = self._get_products_for_store(store_id)
        product_health = [self._build_product_health(product) for product in store_products]

        return InventoryHealthResponse(
            store_id=store.outlet_id,
            store_name=store.name,
            total_products=len(product_health),
            in_stock_products=sum(product.available_stock > 0 for product in store_products),
            healthy_products=sum(item.health_status == "healthy" for item in product_health),
            low_stock_products=sum(item.health_status == "low_stock" for item in product_health),
            out_of_stock_products=sum(item.health_status == "out_of_stock" for item in product_health),
            products=product_health,
        )

    def _get_store_by_id(self, store_id: str) -> GroceryStore | None:
        for store in self.stores:
            if store.outlet_id == store_id:
                return store
        return None

    def _get_products_for_store(self, store_id: str) -> list[GroceryProduct]:
        return [product for product in self.products if product.store and product.store.outlet_id == store_id]

    def _build_product_health(self, product: GroceryProduct) -> InventoryProductHealth:
        return InventoryProductHealth(
            product_id=product.product_id,
            product_name=product.product_name,
            available_stock=product.available_stock,
            threshold=product.threshold,
            health_status=self._resolve_health_status(product.available_stock, product.threshold),
        )

    @staticmethod
    def _resolve_health_status(available_stock: int, threshold: int) -> str:
        if available_stock == 0:
            return "out_of_stock"
        if available_stock <= threshold:
            return "low_stock"
        return "healthy"
