import pytest
from src.repository.cart_repository import CartRepository
from src.domain.cart import Cart
from src.domain.user import User
from src.domain.store import GroceryStore


class TestCartRepository:
    @pytest.fixture
    def cart_repository(self):
        return CartRepository()

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
    def sample_carts(self, sample_user, sample_store):
        user2 = User(
            user_id="user102",
            username="janesmith",
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@gmail.com",
            phone_number="987654321"
        )
        
        return {
            "cart101": Cart(
                cart_id="cart101",
                outlet=sample_store,
                user=sample_user
            ),
            "cart102": Cart(
                cart_id="cart102",
                outlet=sample_store,
                user=user2
            )
        }

    def test_initialization(self, cart_repository):
        assert cart_repository._carts == {}

    def test_initialize_with_data(self, cart_repository, sample_carts):
        cart_repository.initialize_with_data(sample_carts)
        
        assert len(cart_repository._carts) == 2
        assert "cart101" in cart_repository._carts
        assert "cart102" in cart_repository._carts
        assert cart_repository._carts["cart101"].cart_id == "cart101"
        assert cart_repository._carts["cart102"].cart_id == "cart102"

    def test_get_cart_by_user_success(self, cart_repository, sample_carts):
        cart_repository.initialize_with_data(sample_carts)
        
        cart = cart_repository.get_cart_by_user("user101")
        
        assert cart is not None
        assert cart.cart_id == "cart101"
        assert cart.user.user_id == "user101"
        assert cart.outlet.outlet_id == "store101"