from fastapi import APIRouter

from .controller.cart_controller import router as cart_router
from .controller.inventory_controller import router as inventory_router
from .system.routes import router as system_router

router = APIRouter()

router.include_router(cart_router)
router.include_router(inventory_router)
router.include_router(system_router)
