from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Query
from ..service.cart_service import CartService
from .models import AddProductRequest, CartProductInfo, CartResponse
from ..domain.product import GroceryProduct, FoodProduct

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/product", response_model=CartProductInfo)
def add_product_to_cart(data: AddProductRequest):
    try:
        from ..main import app
        user_repository = app.state.user_repository
        product_repository = app.state.product_repository
        store_repository = app.state.store_repository
        cart_repository = app.state.cart_repository
        
        result = CartService.add_product_to_cart_for_user(
            cart_repository=cart_repository,
            product_repository=product_repository,
            user_repository=user_repository,
            store_repository=store_repository,
            user_id=data.user_id,
            product_id=data.product_id,
            outlet_id=data.outlet_id
        )
        return CartProductInfo(**result)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Failed to add product to cart: {str(e)}")


@router.get("/view", response_model=CartResponse)
def view_cart(user_id: str = Query(..., description="User ID")):
    try:
        from ..main import app
        user_repository = app.state.user_repository
        cart_repository = app.state.cart_repository
        
        cart = CartService.get_cart_for_user(
            cart_repository=cart_repository,
            user_repository=user_repository,
            user_id=user_id
        )
        if not cart:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cart not found for user")
        
        total_amount = sum(product.selling_price if hasattr(product, 'selling_price') else product.mrp 
                          for product in cart.products)
        product_count = len(cart.products)
        grocery_products = [product.to_json() for product in cart.products 
                          if isinstance(product, GroceryProduct)]
        food_products = [product.to_json() for product in cart.products 
                        if isinstance(product, FoodProduct)]
        is_empty = len(cart.products) == 0
        
        return CartResponse(
            cart_id=cart.cart_id,
            outlet=cart.outlet.to_json(),
            user=cart.user.to_json() if cart.user else None,
            products=[product.to_json() for product in cart.products],
            total_amount=total_amount,
            product_count=product_count,
            grocery_products=grocery_products,
            food_products=food_products,
            is_empty=is_empty
        )
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Failed to get cart: {str(e)}") 