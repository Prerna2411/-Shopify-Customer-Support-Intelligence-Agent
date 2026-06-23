from app.models.model_router import ModelRouter


class ReasoningAgent:
    def __init__(self, router: ModelRouter | None = None):
        self.router = router or ModelRouter()

    def respond(self, message: str, intent: dict, order: dict | None, policies: list[dict]) -> dict:
        if self.router.reasoning_model.api_key:
            try:
                return self._respond_with_groq(message, intent, order, policies)
            except Exception:
                pass
        return self._respond_locally(message, intent, order, policies)

    def _respond_with_groq(self, message: str, intent: dict, order: dict | None, policies: list[dict]) -> dict:
        policy_context = "\n\n".join(
            f"Source: {policy['source']}\n{policy['content']}" for policy in policies
        )
        prompt = f"""
Generate a Shopify customer support response using the order and policy context.
Return only the final customer-facing reply as normal plain text.
Do not return JSON, markdown tables, internal analysis, confidence values, or policy metadata.
Do not promise refunds, replacements, cancellations, or payment actions unless the policy clearly allows it.

Customer message:
{message}

Intent:
{intent}

Order:
{order}

Policy context:
{policy_context}
"""
        response = self.router.reasoning_model.complete(
            prompt,
            system="You are a careful ecommerce support reasoning agent.",
        ).strip()
        confidence = min(0.95, intent.get("confidence", 0.7) + (0.08 if order else -0.08) + (0.06 if policies else -0.06))
        return {
            "analysis": self._analysis_summary(intent, order, policies, "groq"),
            "response": response,
            "confidence": round(confidence, 2),
        }

    def _respond_locally(self, message: str, intent: dict, order: dict | None, policies: list[dict]) -> dict:
        intent_name = intent.get("intent", "general_support")
        policy_hint = policies[0]["content"].splitlines()[0] if policies else "Use store support policy."
        order_text = self._order_summary(order)
        response = self._compose_response(intent_name, order, policy_hint)
        confidence = min(0.95, intent.get("confidence", 0.6) + (0.08 if order else -0.08) + (0.06 if policies else -0.06))
        return {
            "analysis": self._analysis_summary(intent, order, policies, "local"),
            "response": response,
            "confidence": round(confidence, 2),
        }

    def _analysis_summary(self, intent: dict, order: dict | None, policies: list[dict], mode: str) -> str:
        intent_name = intent.get("intent", "general_support")
        order_text = self._order_summary(order)
        policy_sources = ", ".join(policy["source"] for policy in policies) if policies else "none"
        return f"mode={mode}; intent={intent_name}; {order_text}; policy_sources={policy_sources}"

    def _order_summary(self, order: dict | None) -> str:
        if not order:
            return "No matching order was found."
        return f"Order {order['order_id']} is {order['status']} with delivery estimate {order.get('expected_delivery')}."

    def _compose_response(self, intent_name: str, order: dict | None, policy_hint: str) -> str:
        greeting = "Thanks for reaching out. "
        if not order:
            return greeting + "I could not verify the order details from the message, so I am escalating this to our support team for a manual check."
        if intent_name == "refund_request":
            return (
                greeting
                + f"I checked order #{order['order_id']}. Its current status is {order['status']} and the expected delivery date is "
                + f"{order.get('expected_delivery')}. {policy_hint} Based on this, I will keep the case open and escalate it if the policy condition is met."
            )
        if intent_name == "shipping_status":
            return (
                greeting
                + f"Order #{order['order_id']} is currently {order['status']}. Tracking: {order.get('tracking_number')}. "
                + f"Expected delivery is {order.get('expected_delivery')}."
            )
        return greeting + f"I reviewed order #{order['order_id']} and the relevant policy. {policy_hint} A support agent can help with any next step that needs approval."
