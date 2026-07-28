class InventoryService:

    def __init__(self, inventory_data):
        self.inventory_data = inventory_data

    def get_inventory_health(self, store_id: str):

        if store_id not in self.inventory_data:
            raise ValueError("Store not found")

        inventory = self.inventory_data[store_id]

        total_products = len(inventory)

        out_of_stock = sum(
            1 for item in inventory
            if item.available_stock == 0
        )

        return {
            "store_id": store_id,
            "healthy": out_of_stock == 0,
            "total_products": total_products,
            "out_of_stock": out_of_stock,
        }