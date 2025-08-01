import pytest
from unittest.mock import Mock
from src.service.cart_service import CartService
from src.domain.user import User
from src.domain.store import GroceryStore
from src.domain.product import GroceryProduct
from src.domain.cart import Cart


class TestCartService:
    def setup_method(self):
        CartService.user_carts.clear()

    @pytest.fixture
    def mock_cart_repository(self):
        return Mock()

    @pytest.fixture
    def mock_product_repository(self):
        return Mock()

    @pytest.fixture
    def mock_user_repository(self):
        return Mock()

    @pytest.fixture
    def mock_store_repository(self):
        return Mock()

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

    def test_add_product_to_cart_for_user_success(self, mock_user_repository, mock_store_repository, 
                                                 mock_product_repository, mock_cart_repository,
                                                 sample_user, sample_store, sample_product):
        mock_user_repository.get_user.return_value = sample_user
        mock_store_repository.get_store.return_value = sample_store
        mock_product_repository.get_product.return_value = sample_product
        mock_cart_repository.get_cart_by_user.return_value = None  # Ensure no existing cart
        
        result = CartService.add_product_to_cart_for_user(
            mock_cart_repository, mock_product_repository, mock_user_repository, mock_store_repository,
            "user101", "product101", "store101"
        )
        
        assert result["cart"]["cart_id"] is not None
        assert result["product"]["product_id"] == "product101"
        assert result["selling_price"] == 10.5  # Using selling_price attribute
        mock_user_repository.get_user.assert_called_once_with("user101")
        mock_store_repository.get_store.assert_called_once_with("store101")
        mock_product_repository.get_product.assert_called_once_with("product101")

   
    def test_get_cart_for_user_success(self, mock_user_repository, mock_cart_repository, sample_user, sample_cart):
        mock_user_repository.get_user.return_value = sample_user
        CartService.user_carts[sample_user.user_id] = sample_cart
        
        result = CartService.get_cart_for_user(mock_cart_repository, mock_user_repository, "user101")
        
        assert result == sample_cart
        mock_user_repository.get_user.assert_called_once_with("user101")