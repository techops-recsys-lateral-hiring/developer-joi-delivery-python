from pydantic import BaseModel, Field


class AddProductRequest(BaseModel):
    user_id: str = Field(..., description="User ID")
    product_id: str = Field(..., description="Product ID")
    outlet_id: str = Field(..., description="Outlet ID")


class CartProductInfo(BaseModel):
    cart: dict
    product: dict
    selling_price: float | None = None