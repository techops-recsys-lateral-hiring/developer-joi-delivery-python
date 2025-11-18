from fastapi import APIRouter, HTTPException, Query, Depends
from loguru import logger
from ..service.cart_service import CartService
from .models import AddProductRequest, CartProductInfo
from ..domain.cart import Cart
from ..dependencies import get_cart_service

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/product", response_model=CartProductInfo)
def add_product_to_cart(
    data: AddProductRequest,
    cart_service: CartService = Depends(get_cart_service)
):
    result = cart_service.add_product_to_cart_for_user(data)
    return result


@router.get("/view", response_model= Cart)
def view_cart(
    user_id: str = Query(..., description="User ID"),
    cart_service: CartService = Depends(get_cart_service)
):
    cart = cart_service.get_cart_for_user(user_id)

    return cart