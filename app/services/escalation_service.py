from app.utils.config import get_settings


class EscalationService:
    def should_escalate(self, confidence: float, validation: dict, order: dict | None) -> tuple[bool, str | None]:
        threshold = get_settings().auto_reply_confidence_threshold
        if not validation.get("valid"):
            return True, "Validation failed or policy grounding was insufficient."
        if confidence < threshold:
            return True, f"Confidence {confidence:.2f} is below threshold {threshold:.2f}."
        if order is None:
            return True, "Order details could not be found."
        return False, None
