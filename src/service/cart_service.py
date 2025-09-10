from typing import Optional
from ..domain.cart import Cart
from ..domain.user import User
from ..service.user_service import UserService
from ..service.product_service import ProductService
from ..controller.models import AddProductRequest, CartProductInfo


class CartService:
    def __init__(self, user_service: UserService, product_service: ProductService, cart_for_users: dict):
        self.user_service = user_service
        self.product_service = product_service
        self.user_carts = cart_for_users

    def add_product_to_cart_for_user(self, add_product_request: AddProductRequest) -> CartProductInfo:
        user = self.user_service.fetch_user_by_id(add_product_request.user_id)
        cart = self.fetch_cart_for_user(user)
        product = self.product_service.get_product(add_product_request.product_id, add_product_request.outlet_id)
        cart.products.append(product)
        
        result = CartProductInfo(
            cart=cart.to_json(),
            product=product.to_json(),
            selling_price=product.selling_price
        )
        return result

    def get_cart_for_user(self, user_id: str) -> Optional[Cart]:
        user = self.user_service.fetch_user_by_id(user_id)
        return self.fetch_cart_for_user(user)
  

    def fetch_cart_for_user(self, user: User) -> Optional[Cart]:
        if user is None:
            return None
        return self.user_carts.get(user.user_id)
