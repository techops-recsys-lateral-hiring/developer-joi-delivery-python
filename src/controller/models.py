from pydantic import BaseModel, Field
from typing import List, Optional


class UserCreateRequest(BaseModel):
    username: str = Field(..., description="Username")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    email: str = Field(..., description="Email address")
    phone_number: str = Field(..., description="Phone number")


class UserResponse(BaseModel):
    user_id: str
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str


class OutletResponse(BaseModel):
    name: str
    description: str
    outlet_id: str


class GroceryStoreResponse(OutletResponse):
    inventory_count: int
    total_inventory_value: float


class RestaurantResponse(OutletResponse):
    pass


class ProductResponse(BaseModel):
    product_id: str
    product_name: str
    mrp: float
    selling_price: float
    product_type: str


class GroceryProductResponse(ProductResponse):
    weight: float
    expiry_date: int
    threshold: int
    available_stock: int
    discount: float
    is_low_stock: bool
    is_out_of_stock: bool


class FoodProductResponse(ProductResponse):
    pass


class AddProductRequest(BaseModel):
    user_id: str = Field(..., description="User ID")
    product_id: str = Field(..., description="Product ID")
    outlet_id: str = Field(..., description="Outlet ID")


class CartProductInfo(BaseModel):
    cart: dict
    product: dict
    selling_price: float


class CartResponse(BaseModel):
    cart_id: str
    outlet: OutletResponse
    user: UserResponse
    products: List[ProductResponse]
    total_amount: float
    product_count: int
    grocery_products: List[ProductResponse]
    food_products: List[ProductResponse]
    is_empty: bool


class CartSummaryResponse(BaseModel):
    cart_id: str
    outlet: OutletResponse
    user: UserResponse
    total_amount: float
    product_count: int
    grocery_products: int
    food_products: int
    is_empty: bool


class CartValidationResponse(BaseModel):
    is_valid: bool
    errors: List[str]
    total_amount: float
    product_count: int


class InventoryHealthResponse(BaseModel):
    store_id: str
    health_status: Optional[str] = None


class CartStatisticsResponse(BaseModel):
    total_carts: int
    active_carts: int
    grocery_carts: int
    restaurant_carts: int
    total_value: float
    average_cart_value: float 