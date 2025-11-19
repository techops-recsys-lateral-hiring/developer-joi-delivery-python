from http import HTTPStatus
from fastapi import APIRouter, Query, Response

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/health")
def fetch_store_inventory_health(store_id: str = Query(..., alias="store_id", description="Store ID")):
    return Response(status_code=HTTPStatus.OK)
