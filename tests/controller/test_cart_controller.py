import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.main import app
from src.domain.user import User
from src.domain.store import GroceryStore
from src.domain.product import GroceryProduct
from src.domain.cart import Cart


class TestCartController:
    def setup_method(self):
        from src.service.cart_service import CartService
        CartService.user_carts.clear()

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
            phone_number="123456789"
        )

    @pytest.fixture
    def sample_store(self):
        return GroceryStore(
            name="Fresh Picks",
            description="Fresh grocery store",
            outlet_id="store101"
        )

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
            store=sample_store
        )

    @pytest.fixture
    def sample_cart(self, sample_user, sample_store):
        return Cart(
            cart_id="cart101",
            outlet=sample_store,
            user=sample_user
        )

    @patch('src.main.app.state.user_repository')
    @patch('src.main.app.state.product_repository')
    @patch('src.main.app.state.store_repository')
    @patch('src.main.app.state.cart_repository')
    def test_add_product_to_cart_success(self, mock_cart_repo, mock_store_repo, mock_product_repo, mock_user_repo,
                                        client, sample_user, sample_store, sample_product):
        mock_user_repo.get_user.return_value = sample_user
        mock_store_repo.get_store.return_value = sample_store
        mock_product_repo.get_product.return_value = sample_product
        mock_cart_repo.get_cart_by_user.return_value = None  # Ensure no existing cart
        
        response = client.post("/cart/product", json={
            "user_id": "user101",
            "product_id": "product101",
            "outlet_id": "store101"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "cart" in data
        assert "product" in data
        assert "selling_price" in data


    @patch('src.main.app.state.user_repository')
    @patch('src.main.app.state.cart_repository')
    def test_view_cart_success(self, mock_cart_repo, mock_user_repo, client, sample_user, sample_cart):
        mock_user_repo.get_user.return_value = sample_user
        mock_cart_repo.get_cart_by_user.return_value = sample_cart
        
        response = client.get("/cart/view?user_id=user101")
        
        assert response.status_code == 200
        data = response.json()
        assert data["cart_id"] == "cart101"
        assert "outlet" in data
        assert "user" in data
        assert "products" in data
