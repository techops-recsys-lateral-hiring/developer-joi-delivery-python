from pydantic import BaseModel, Field


class AddProductRequest(BaseModel):
    user_id: str = Field(..., description="User ID")
    product_id: str = Field(..., description="Product ID")
    outlet_id: str = Field(..., description="Outlet ID")


class CartProductInfo(BaseModel):
    cart: dict
    product: dict
    selling_price: float | None = None


class InventoryProductHealth(BaseModel):
    product_id: str
    product_name: str
    available_stock: int
    threshold: int
    health_status: str


class InventoryHealthResponse(BaseModel):
    store_id: str
    store_name: str
    total_products: int
    in_stock_products: int
    healthy_products: int
    low_stock_products: int
    out_of_stock_products: int
    products: list[InventoryProductHealth]
