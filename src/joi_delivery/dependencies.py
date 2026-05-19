from fastapi import Request

from joi_delivery.service.cart_service import CartService
from joi_delivery.service.inventory_service import InventoryService
from joi_delivery.service.product_service import ProductService
from joi_delivery.service.user_service import UserService


def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service


def get_product_service(request: Request) -> ProductService:
    return request.app.state.product_service


def get_cart_service(request: Request) -> CartService:
    return request.app.state.cart_service


def get_inventory_service(request: Request) -> InventoryService:
    return request.app.state.inventory_service
