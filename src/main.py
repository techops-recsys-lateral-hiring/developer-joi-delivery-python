from http import HTTPStatus

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.responses import JSONResponse

from .generator.app_initializer import initialize_data
from .router import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="JOI Delivery",
        description="A thoughtful, technology-first food and grocery delivery platform",
        version="0.1.0"
    )

    app.include_router(router)

    app_data = initialize_data()
    
    from .repository.user_repository import UserRepository
    from .repository.product_repository import ProductRepository
    from .repository.store_repository import StoreRepository
    from .repository.cart_repository import CartRepository
    
    user_repository = UserRepository()
    product_repository = ProductRepository()
    store_repository = StoreRepository()
    cart_repository = CartRepository()
    
    user_repository.initialize_with_data(app_data['users'])
    product_repository.initialize_with_data(app_data['grocery_products'])
    store_repository.initialize_with_data(app_data['stores'])
    cart_repository.initialize_with_data(app_data['cart_for_users'])
    
    app.state.user_repository = user_repository
    app.state.product_repository = product_repository
    app.state.store_repository = store_repository
    app.state.cart_repository = cart_repository
    
    logger.info("Repositories initialized with seed data")

    @app.exception_handler(RequestValidationError)
    async def custom_validation_exception_handler(request, e):
        exc_str = f"{e}".replace("\n", " ").replace("   ", " ")
        logger.warning(f"{request}: {exc_str}")
        content = {"message": exc_str, "data": None}
        return JSONResponse(content=content, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)

    return app


app = create_app() 