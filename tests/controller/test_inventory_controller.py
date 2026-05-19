import pytest
from fastapi.testclient import TestClient
from joi_delivery.main import app


class TestInventoryController:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_should_return_the_health_of_the_store(self, client):
        get_url = "/inventory/health?store_id=store101"

        response = client.get(get_url)

        assert response.status_code == 200
        data = response.json()
        assert data["store_id"] == "store101"
        assert data["store_name"] == "Fresh Picks"
        assert data["total_products"] == 3
        assert data["in_stock_products"] == 3
        assert data["healthy_products"] == 3
        assert data["low_stock_products"] == 0
        assert data["out_of_stock_products"] == 0
        assert len(data["products"]) == 3
        assert data["products"][0]["health_status"] == "healthy"

    def test_should_return_404_for_unknown_store(self, client):
        response = client.get("/inventory/health?store_id=missing-store")

        assert response.status_code == 404
        assert response.json() == {"detail": "Store not found for store_id=missing-store"}
