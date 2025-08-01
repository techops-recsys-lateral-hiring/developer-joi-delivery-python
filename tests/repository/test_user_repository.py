import pytest
from src.repository.user_repository import UserRepository
from src.domain.user import User


class TestUserRepository:
    @pytest.fixture
    def user_repository(self):
        return UserRepository()

    @pytest.fixture
    def sample_users(self):
        return [
            User(
                user_id="user101",
                username="johndoe",
                first_name="John",
                last_name="Doe",
                email="john.doe@gmail.com",
                phone_number="123456789"
            ),
            User(
                user_id="user102",
                username="janesmith",
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@gmail.com",
                phone_number="987654321"
            )
        ]

    def test_initialization(self, user_repository):
        assert user_repository._users == {}

    def test_initialize_with_data(self, user_repository, sample_users):
        user_repository.initialize_with_data(sample_users)
        
        assert len(user_repository._users) == 2
        assert "user101" in user_repository._users
        assert "user102" in user_repository._users
        assert user_repository._users["user101"].username == "johndoe"
        assert user_repository._users["user102"].username == "janesmith"

    def test_get_user_success(self, user_repository, sample_users):
        user_repository.initialize_with_data(sample_users)
        
        user = user_repository.get_user("user101")
        
        assert user is not None
        assert user.user_id == "user101"
        assert user.username == "johndoe"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
