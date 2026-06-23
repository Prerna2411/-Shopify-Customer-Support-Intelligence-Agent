class SupervisorAgent:
    def plan(self, message: str, order_id: str | None = None) -> dict:
        lowered = message.lower()
        needs_order = bool(order_id) or any(word in lowered for word in ["order", "shipment", "tracking", "delivery"])
        needs_policy = any(
            word in lowered
            for word in ["refund", "return", "shipping", "payment", "cancel", "exchange", "warranty", "gift"]
        )
        return {
            "run_intent_agent": True,
            "run_order_agent": needs_order,
            "run_policy_agent": needs_policy or True,
            "run_reasoning_agent": True,
            "run_validation_agent": True,
        }
