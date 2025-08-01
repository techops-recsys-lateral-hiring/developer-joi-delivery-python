from typing import Optional, List
from ..domain.user import User


class UserRepository:
    def __init__(self):
        self._users = {}

    def initialize_with_data(self, users: List[User]):
        self._users = {user.user_id: user for user in users}

    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)