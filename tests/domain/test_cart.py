import pytest
from src.domain.cart import Cart
from src.domain.user import User
from src.domain.store import GroceryStore
from src.domain.product import GroceryProduct, FoodProduct


class TestCart:
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
    def sample_grocery_product(self, sample_store):
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
    def sample_food_product(self):
        return FoodProduct(
            product_name="Margherita Pizza",
            product_id="food101",
            mrp=18.99
        )

    @pytest.fixture
    def sample_cart(self, sample_user, sample_store):
        return Cart(
            cart_id="cart101",
            outlet=sample_store,
            user=sample_user
        )

    def test_cart_initialization(self, sample_user, sample_store):
        cart = Cart(
            cart_id="cart101",
            outlet=sample_store,
            user=sample_user
        )
        
        assert cart.cart_id == "cart101"
        assert cart.outlet == sample_store
        assert cart.user == sample_user
        assert len(cart.products) == 0

    def test_cart_to_json(self, sample_user, sample_store):
        cart = Cart(
            cart_id="cart101",
            outlet=sample_store,
            user=sample_user
        )
        
        json_data = cart.to_json()
        
        assert json_data["cart_id"] == "cart101"
        assert json_data["outlet"] is not None
        assert json_data["user"] is not None
        assert json_data["products"] == []

    def test_cart_with_products(self, sample_cart, sample_grocery_product, sample_food_product):
        sample_cart.products.append(sample_grocery_product)
        sample_cart.products.append(sample_food_product)
        
        assert len(sample_cart.products) == 2
        assert sample_cart.products[0] == sample_grocery_product
        assert sample_cart.products[1] == sample_food_product

    def test_cart_to_json_with_products(self, sample_cart, sample_grocery_product, sample_food_product):
        sample_cart.products.append(sample_grocery_product)
        sample_cart.products.append(sample_food_product)
        
        json_data = sample_cart.to_json()
        
        assert json_data["cart_id"] == "cart101"
        assert json_data["outlet"] is not None
        assert json_data["user"] is not None
        assert len(json_data["products"]) == 2
        assert json_data["products"][0]["product_id"] == "product101"
        assert json_data["products"][1]["product_id"] == "food101"

    def test_cart_empty_products(self, sample_cart):
        assert len(sample_cart.products) == 0
        assert sample_cart.products == []

    def test_cart_without_user(self, sample_store):
        cart = Cart(
            cart_id="cart101",
            outlet=sample_store
        )
        
        assert cart.cart_id == "cart101"
        assert cart.outlet == sample_store
        assert cart.user is None
        assert len(cart.products) == 0

    def test_cart_to_json_without_user(self, sample_store):
        cart = Cart(
            cart_id="cart101",
            outlet=sample_store
        )
        
        json_data = cart.to_json()
        
        assert json_data["cart_id"] == "cart101"
        assert json_data["outlet"] is not None
        assert json_data["user"] is None
        assert json_data["products"] == [] 