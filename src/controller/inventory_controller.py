from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Path
from ..service.inventory_service import InventoryService
from .models import InventoryHealthResponse

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/health/{store_id}", response_model=InventoryHealthResponse)
def get_store_inventory_health(store_id: str = Path(..., description="Store ID")):
    try:
        health_status = InventoryService.get_store_inventory_health(store_id)
        return InventoryHealthResponse(
            store_id=store_id,
            health_status=health_status
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Failed to get inventory health: {str(e)}") 