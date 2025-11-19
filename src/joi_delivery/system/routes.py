from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/health")
async def health_check():
    return {"status": "healthy"}


@router.get("/")
async def root():
    return {
        "message": "Welcome to JOI Delivery",
        "description": "A thoughtful, technology-first food and grocery delivery platform",
        "version": "0.1.0",
        "endpoints": {
            "cart": {"add_product": "/cart/product", "view_cart": "/cart/view?user_id={user_id}"},
            "inventory": {"health_check": "/inventory/health?store_id={store_id}"},
            "system": {"health": "/health", "root": "/"},
        },
    }
