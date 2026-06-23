from app.services.shopify_service import ShopifyService
from app.utils.helpers import extract_order_id


class OrderAgent:
    def __init__(self, service: ShopifyService | None = None):
        self.service = service or ShopifyService()

    def fetch(self, message: str, order_id: str | None = None) -> dict | None:
        resolved_order_id = order_id or extract_order_id(message)
        return self.service.get_order(resolved_order_id)
