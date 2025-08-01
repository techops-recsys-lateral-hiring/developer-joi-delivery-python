from typing import Optional
import uuid
from ..repository.cart_repository import CartRepository
from ..repository.product_repository import ProductRepository
from ..repository.user_repository import UserRepository
from ..repository.store_repository import StoreRepository
from ..domain.cart import Cart
from ..domain.product import Product, GroceryProduct
from ..domain.user import User
from ..domain.outlet import Outlet


class CartService:
    user_carts = {}

    @staticmethod
    def add_product_to_cart_for_user(cart_repository: CartRepository, 
                                   product_repository: ProductRepository,
                                   user_repository: UserRepository, 
                                   store_repository: StoreRepository,
                                   user_id: str, product_id: str, outlet_id: str) -> dict:
        user = user_repository.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        cart = CartService.fetch_cart_for_user(cart_repository, user)
        if not cart:
            outlet = store_repository.get_store(outlet_id)
            if not outlet:
                raise ValueError(f"Outlet {outlet_id} not found")
            
            cart_id = str(uuid.uuid4())
            cart = Cart(cart_id=cart_id, outlet=outlet, user=user)
            CartService.user_carts[user.user_id] = cart
        
        product = product_repository.get_product(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        
        cart.products.append(product)
        
        selling_price = product.selling_price if isinstance(product, GroceryProduct) else product.mrp
        return {
            "cart": cart.to_json(),
            "product": product.to_json(),
            "selling_price": selling_price
        }

    @staticmethod
    def get_cart_for_user(cart_repository: CartRepository,
                         user_repository: UserRepository,
                         user_id: str) -> Optional[Cart]:
        user = user_repository.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        return CartService.fetch_cart_for_user(cart_repository, user)

    @staticmethod
    def fetch_cart_for_user(cart_repository: CartRepository, user: User) -> Optional[Cart]:
        cart = CartService.user_carts.get(user.user_id)
        if cart:
            return cart
        
        cart = cart_repository.get_cart_by_user(user.user_id)
        if cart:
            CartService.user_carts[user.user_id] = cart
        return cart
