from app.models.model_router import ModelRouter


class IntentAgent:
    INTENT_KEYWORDS = {
        "refund_request": ["refund", "money back", "reimburse"],
        "return_request": ["return", "send back"],
        "shipping_status": ["where", "shipping", "shipment", "tracking", "arrived", "delivery", "delayed"],
        "payment_issue": ["payment", "card", "charged", "failed"],
        "cancellation_request": ["cancel", "cancellation"],
        "exchange_request": ["exchange", "replace", "size"],
        "warranty_claim": ["warranty", "repair", "defective", "broken"],
    }

    def __init__(self, router: ModelRouter | None = None):
        self.router = router or ModelRouter()

    def classify(self, message: str) -> dict:
        if self.router.intent_model.api_key:
            try:
                return self._classify_with_groq(message)
            except Exception:
                pass
        return self._classify_locally(message)

    def _classify_with_groq(self, message: str) -> dict:
        prompt = f"""
Classify this Shopify customer support ticket.
Return only JSON with keys: intent, priority, confidence.
Allowed intents: refund_request, return_request, shipping_status, payment_issue,
cancellation_request, exchange_request, warranty_claim, general_support.
Allowed priority values: low, normal, high.

Message: {message}
"""
        result = self.router.intent_model.complete_json(
            prompt,
            system="You are an intent classification agent for ecommerce customer support.",
        )
        return {
            "intent": result.get("intent", "general_support"),
            "priority": result.get("priority", "normal"),
            "confidence": float(result.get("confidence", 0.7)),
        }

    def _classify_locally(self, message: str) -> dict:
        lowered = message.lower()
        intent = "general_support"
        for candidate, keywords in self.INTENT_KEYWORDS.items():
            if any(keyword in lowered for keyword in keywords):
                intent = candidate
                break
        priority = "high" if any(word in lowered for word in ["urgent", "angry", "refund", "failed", "broken"]) else "normal"
        return {"intent": intent, "priority": priority, "confidence": 0.86 if intent != "general_support" else 0.62}
