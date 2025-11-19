import pytest
from fastapi.testclient import TestClient
from joi_delivery.main import app


class TestInventoryController:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_should_return_the_health_of_the_store(self, client):
        get_url = "/inventory/health?store_id=store101"

        # add required mocking.

        response = client.get(get_url)

        # Then: Assert the response
        assert response.status_code == 200
