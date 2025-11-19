from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from joi_delivery.domain.cart import Cart
from joi_delivery.domain.grocery_product import GroceryProduct
from joi_delivery.domain.grocery_store import GroceryStore
from joi_delivery.domain.user import User
from joi_delivery.main import app


class TestCartController:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    @pytest.fixture
    def sample_user(self):
        return User(
            user_id="user101",
            username="johndoe",
            first_name="John",
            last_name="Doe",
            email="john.doe@gmail.com",
            phone_number="123456789",
        )

    @pytest.fixture
    def sample_store(self):
        return GroceryStore(name="Fresh Picks", description="Fresh grocery store", outlet_id="store101")

    @pytest.fixture
    def sample_product(self, sample_store):
        return GroceryProduct(
            product_name="Wheat Bread",
            product_id="product101",
            mrp=10.5,
            selling_price=10.5,
            weight=500.00,
            expiry_date=7,
            threshold=10,
            available_stock=30,
            discount=0.0,
            store=sample_store,
        )

    @pytest.fixture
    def sample_cart(self, sample_user, sample_store):
        return Cart(cart_id="cart101", outlet=sample_store, user=sample_user)

    @patch("joi_delivery.controller.cart_controller.CartService.add_product_to_cart_for_user")
    def test_should_add_the_requested_product_to_the_cart(self, mock_add_product, client):
        # Mock the service method to return the expected format
        mock_add_product.return_value = {
            "cart": {"cart_id": "cart101", "outlet": {}, "user": {}, "products": []},
            "product": {
                "product_id": "product101",
                "product_name": "Wheat Bread",
                "mrp": 10.5,
            },
            "selling_price": 10.5,
        }

        url = "/cart/product"
        add_product_request = {
            "product_id": "product101",
            "user_id": "user101",
            "outlet_id": "store101",
        }

        response = client.post(url, json=add_product_request)

        assert response.status_code == 200

    @patch("joi_delivery.controller.cart_controller.CartService.get_cart_for_user")
    def test_should_return_the_cart(self, mock_get_cart, client):
        # Mock the service method to return a Cart object
        mock_cart = Cart(
            cart_id="cart101",
            outlet=GroceryStore(
                name="Fresh Picks",
                description="Fresh grocery store",
                outlet_id="store101",
            ),
            user=User(
                user_id="user101",
                username="johndoe",
                first_name="John",
                last_name="Doe",
                email="john.doe@gmail.com",
                phone_number="123456789",
            ),
            products=[],
        )
        mock_get_cart.return_value = mock_cart

        url = "/cart/view?user_id=user101"

        response = client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data["cart_id"] == "cart101"
        # Check that all required fields are present
        assert "outlet" in data
        assert "user" in data
        assert "products" in data
