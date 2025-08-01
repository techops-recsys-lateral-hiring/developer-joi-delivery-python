import pytest
from src.domain.product import Product, GroceryProduct, FoodProduct
from src.domain.store import GroceryStore


class TestProduct:
    @pytest.fixture
    def sample_store(self):
        return GroceryStore(
            name="Fresh Picks",
            description="Fresh grocery store",
            outlet_id="store101"
        )

    def test_food_product_initialization(self):
        product = FoodProduct(
            product_name="Margherita Pizza",
            product_id="food101",
            mrp=18.99
        )
        
        assert product.product_id == "food101"
        assert product.product_name == "Margherita Pizza"
        assert product.mrp == 18.99

    def test_food_product_to_json(self):
        product = FoodProduct(
            product_name="Margherita Pizza",
            product_id="food101",
            mrp=18.99
        )
        
        json_data = product.to_json()
        
        assert json_data["product_id"] == "food101"
        assert json_data["product_name"] == "Margherita Pizza"
        assert json_data["mrp"] == 18.99

    def test_grocery_product_initialization(self, sample_store):
        product = GroceryProduct(
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
        
        assert product.product_id == "product101"
        assert product.product_name == "Wheat Bread"
        assert product.mrp == 10.5
        assert product.selling_price == 10.5
        assert product.weight == 500.00
        assert product.expiry_date == 7
        assert product.threshold == 10
        assert product.available_stock == 30
        assert product.discount == 0.0
        assert product.store == sample_store

    def test_grocery_product_to_json(self, sample_store):
        product = GroceryProduct(
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
        
        json_data = product.to_json()
        
        assert json_data["product_id"] == "product101"
        assert json_data["product_name"] == "Wheat Bread"
        assert json_data["mrp"] == 10.5
        assert json_data["selling_price"] == 10.5
        assert json_data["weight"] == 500.00
        assert json_data["expiry_date"] == 7
        assert json_data["threshold"] == 10
        assert json_data["available_stock"] == 30
        assert json_data["discount"] == 0.0
        assert json_data["product_type"] == "grocery"
        assert json_data["store"] is not None

    def test_grocery_product_without_store(self):
        product = GroceryProduct(
            product_name="Wheat Bread",
            product_id="product101",
            mrp=10.5,
            selling_price=10.5,
            weight=500.00,
            expiry_date=7,
            threshold=10,
            available_stock=30,
            discount=0.0
        )
        
        assert product.store is None
        
        json_data = product.to_json()
        assert json_data["store"] is None

    def test_product_inheritance(self):
        food_product = FoodProduct(
            product_name="Test Food",
            product_id="food101",
            mrp=10.0
        )
        
        grocery_product = GroceryProduct(
            product_name="Test Grocery",
            product_id="grocery101",
            mrp=10.0,
            selling_price=10.0,
            weight=100.0,
            expiry_date=7,
            threshold=5,
            available_stock=10,
            discount=0.0
        )
        
        assert isinstance(food_product, Product)
        assert isinstance(grocery_product, Product) 