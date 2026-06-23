import json
from pathlib import Path

from app.utils.config import get_settings


class ShopifyService:
    def __init__(self, orders_path: Path | None = None):
        self.orders_path = orders_path or get_settings().orders_path

    def get_order(self, order_id: str | None) -> dict | None:
        if not order_id or not self.orders_path.exists():
            return None
        data = json.loads(self.orders_path.read_text(encoding="utf-8"))
        normalized = order_id.replace("#", "").upper()
        for order in data.get("orders", []):
            if str(order.get("order_id", "")).upper() == normalized:
                return order
        return None
