from http import HTTPStatus

from fastapi import APIRouter, Query, Response, Depends
from ..dependencies import get_inventory_service
from ..service.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/health")
def fetch_store_inventory_health(
     store_id: str = Query(..., alias="store_id", description="Store ID"),
     inventory_service: InventoryService = Depends(get_inventory_service),):
     return inventory_service.get_inventory_health(store_id)
    #return Response(status_code=HTTPStatus.OK)
