from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Outlet:
    name: str
    outlet_id: str
    description: str | None = None

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "outlet_id": self.outlet_id,
        }
