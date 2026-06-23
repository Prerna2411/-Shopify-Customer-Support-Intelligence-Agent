from app.agents.intent_agent import IntentAgent
from app.agents.order_agent import OrderAgent


def test_intent_agent_detects_refund():
    result = IntentAgent().classify("My order #1234 is late and I want a refund")
    assert result["intent"] == "refund_request"
    assert result["priority"] == "high"


def test_order_agent_loads_sample_order():
    order = OrderAgent().fetch("Where is order #1234?")
    assert order["order_id"] == "1234"
    assert order["status"] == "delayed"
