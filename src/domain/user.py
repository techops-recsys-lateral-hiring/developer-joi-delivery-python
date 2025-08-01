from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    user_id: str
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    cart: Optional['Cart'] = None

    def to_json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "cart": self.cart.to_json() if self.cart else None
        } 