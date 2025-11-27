from typing import List, Optional

from ..domain.user import User


class UserService:
    def __init__(self, users: List[User]):
        self.users = users

    def fetch_user_by_id(self, user_id: str) -> Optional[User]:
        for user in self.users:
            if user_id == user.user_id:
                return user
        return None
