from fastapi import APIRouter, Query, Depends
from ..dependencies import get_product_service
from ..service.product_service import ProductService

router = APIRouter(prefix="/product", tags=["product"])


@router.get("/")
def fetch_product(
    product_id: str = Query(..., alias="product_id", description="Product ID"),
    outlet_id: str = Query(..., alias="outlet_id", description="Outlet ID"),
    product_service: ProductService = Depends(get_product_service),
): return product_service.get_product(product_id, outlet_id)
