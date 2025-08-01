from typing import Optional
from ..repository.user_repository import UserRepository


class UserService:
    @staticmethod
    def fetch_user_by_id(user_repository: UserRepository, user_id: str) -> Optional['User']:
        return user_repository.get_user(user_id) 