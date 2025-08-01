import pytest
from unittest.mock import patch
from src.generator.app_initializer import initialize_data
from src.domain.user import User
from src.domain.store import GroceryStore
from src.domain.product import GroceryProduct
from src.domain.cart import Cart


class TestInitializeData:
    @patch('src.generator.app_initializer.logger')
    def test_initialize_data_structure(self, mock_logger):
        result = initialize_data()
        
        assert isinstance(result, dict)
        assert 'users' in result
        assert 'grocery_products' in result
        assert 'stores' in result
        assert 'cart_for_users' in result

    @patch('src.generator.app_initializer.logger')
    def test_initialize_data_users(self, mock_logger):
        result = initialize_data()
        
        users = result['users']
        assert len(users) == 1
        assert users[0].user_id == "user101"
        assert users[0].first_name == "John"
        assert users[0].last_name == "Doe"

    @patch('src.generator.app_initializer.logger')
    def test_initialize_data_stores(self, mock_logger):
        result = initialize_data()
        
        stores = result['stores']
        assert len(stores) == 2
        assert stores[0].name == "Fresh Picks"
        assert stores[0].outlet_id == "store101"
        assert stores[1].name == "Natural Choice"
        assert stores[1].outlet_id == "store102"

    @patch('src.generator.app_initializer.logger')
    def test_initialize_data_grocery_products(self, mock_logger):
        result = initialize_data()
        
        grocery_products = result['grocery_products']
        assert len(grocery_products) == 3
        
        assert grocery_products[0].product_name == "Wheat Bread"
        assert grocery_products[0].product_id == "product101"
        assert grocery_products[0].store.name == "Fresh Picks"
        
        assert grocery_products[1].product_name == "Spinach"
        assert grocery_products[1].product_id == "product102"
        assert grocery_products[1].store.name == "Fresh Picks"
        
        assert grocery_products[2].product_name == "Crackers"
        assert grocery_products[2].product_id == "product103"
        assert grocery_products[2].store.name == "Fresh Picks"

    @patch('src.generator.app_initializer.logger')
    def test_initialize_data_cart_for_users(self, mock_logger):
        result = initialize_data()
        
        cart_for_users = result['cart_for_users']
        assert len(cart_for_users) == 2
        assert "user101" in cart_for_users
        assert "user102" in cart_for_users
        
        cart101 = cart_for_users["user101"]
        assert cart101.cart_id == "cart101"
        assert cart101.user.user_id == "user101"
        assert cart101.user.first_name == "John"
        assert cart101.user.last_name == "Doe"
        assert cart101.outlet.name == "Fresh Picks"
        
        cart102 = cart_for_users["user102"]
        assert cart102.cart_id == "cart102"
        assert cart102.user.user_id == "user102"
        assert cart102.user.first_name == "Rachel"
        assert cart102.user.last_name == "Zane"
        assert cart102.outlet.name == "Fresh Picks"

   