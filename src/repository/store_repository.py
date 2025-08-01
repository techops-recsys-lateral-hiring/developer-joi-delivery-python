from typing import Optional, List, Dict
from ..domain.store import GroceryStore, Restaurant
from ..domain.outlet import Outlet


class StoreRepository:
    def __init__(self):
        self._stores: Dict[str, Outlet] = {}

    def initialize_with_data(self, stores: List[Outlet]):
        self._stores = {store.outlet_id: store for store in stores}

    def get_store(self, store_id: str) -> Optional[Outlet]:
        return self._stores.get(store_id) 