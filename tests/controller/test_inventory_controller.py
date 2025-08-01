import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.main import app


class TestInventoryController:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    @patch('src.controller.inventory_controller.InventoryService')
    def test_should_return_the_health_of_the_store(self, mock_inventory_service, client):
        # Given: Mock the inventory service
        mock_inventory_service.get_store_inventory_health.return_value = None
        
        # When: Perform GET request to inventory health endpoint
        get_url = "/inventory/health/store101"
        response = client.get(get_url)
        
        # Then: Assert the response
 
        
        # Verify the service method was called with correct parameter
