from http import HTTPStatus

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.responses import JSONResponse

from joi_delivery.generator.app_initializer import initialize_data
from joi_delivery.router import router
from joi_delivery.service.cart_service import CartService
from joi_delivery.service.user_service import UserService
from joi_delivery.service.product_service import ProductService


def create_app() -> FastAPI:
    app = FastAPI(
        title="JOI Delivery",
        description="A thoughtful, technology-first food and grocery delivery platform",
        version="0.1.0",
    )

    app.include_router(router)

    # Initialize services with static seed data
    seed_data = initialize_data()

    app.state.user_service = UserService(users=seed_data["users"])
    app.state.product_service = ProductService(products=seed_data["grocery_products"])
    app.state.cart_service = CartService(
        user_service=app.state.user_service,
        product_service=app.state.product_service,
        cart_for_users=seed_data["cart_for_users"],
    )

    logger.info("Services initialized with static seed data")

    @app.exception_handler(RequestValidationError)
    async def custom_validation_exception_handler(request, e):
        exc_str = f"{e}".replace("\n", " ").replace("   ", " ")
        logger.warning(f"{request}: {exc_str}")
        content = {"message": exc_str, "data": None}
        return JSONResponse(content=content, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8020)
