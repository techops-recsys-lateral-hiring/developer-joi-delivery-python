import random
from typing import Dict, List
from loguru import logger
from ..domain.cart import Cart
from ..domain.user import User
from ..domain.grocery_store import GroceryStore
from ..domain.grocery_product import GroceryProduct


class SeedData:
    @staticmethod
    def create_cart_for_user(
        user_id: str, first_name: str, last_name: str, cart_id: str, outlet: GroceryStore, user: User
    ) -> Cart:
        return Cart(cart_id=cart_id, outlet=outlet, user=user)

    @staticmethod
    def create_store(outlet_name: str, store_id: str) -> GroceryStore:
        return GroceryStore(name=outlet_name, outlet_id=store_id)

    @staticmethod
    def create_user(user_id: str, first_name: str, last_name: str) -> User:
        return User(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name}.{last_name}@gmail.com",
            phone_number=str(SeedData.get_random_number_using_next_int(100000000, 900000000)),
        )

    @staticmethod
    def get_random_number_using_next_int(min_val: int, max_val: int) -> int:
        return random.randint(min_val, max_val)

    @staticmethod
    def create_grocery_product(product_name: str, product_id: str, store: GroceryStore) -> GroceryProduct:
        return GroceryProduct(
            product_name=product_name,
            product_id=product_id,
            mrp=10.5,
            weight=500.00,
            threshold=10,
            available_stock=30,
            store=store,
        )


store101 = SeedData.create_store("Fresh Picks", "store101")
store102 = SeedData.create_store("Natural Choice", "store102")
user101 = SeedData.create_user("user101", "John", "Doe")

cart_for_users = {
    "user101": SeedData.create_cart_for_user("user101", "John", "Doe", "cart101", store101, user101),
    "user102": SeedData.create_cart_for_user("user102", "Rachel", "Zane", "cart102", store101, user101),
}

grocery_products = [
    SeedData.create_grocery_product("Wheat Bread", "product101", store101),
    SeedData.create_grocery_product("Spinach", "product102", store101),
    SeedData.create_grocery_product("Crackers", "product103", store101),
]

users = [user101]
stores = [store101, store102]


def initialize_data():
    logger.info("Initializing application with seed data...")

    # Log seed data information
    logger.info(f"Initialized {len(users)} users")
    logger.info(f"Initialized {len(cart_for_users)} carts")
    logger.info(f"Initialized {len(grocery_products)} grocery products")
    logger.info(f"Initialized 2 stores: {store101.name}, {store102.name}")

    logger.info("Application initialization completed successfully!")

    return {"users": users, "grocery_products": grocery_products, "stores": stores, "cart_for_users": cart_for_users}
