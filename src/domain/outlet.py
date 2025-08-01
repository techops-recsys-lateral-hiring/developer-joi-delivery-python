from dataclasses import dataclass


@dataclass
class Outlet:
    name: str
    description: str
    outlet_id: str

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "outlet_id": self.outlet_id
        } 