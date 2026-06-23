from app.agents.intent_agent import IntentAgent
from app.agents.order_agent import OrderAgent
from app.agents.policy_agent import PolicyAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.validation_agent import ValidationAgent
from app.services.escalation_service import EscalationService
from app.services.ticket_service import TicketService


class CustomerSupportWorkflow:
    def __init__(self):
        self.supervisor = SupervisorAgent()
        self.intent_agent = IntentAgent()
        self.order_agent = OrderAgent()
        self.policy_agent = PolicyAgent()
        self.reasoning_agent = ReasoningAgent()
        self.validation_agent = ValidationAgent()
        self.escalation_service = EscalationService()
        self.ticket_service = TicketService()

    def run(self, customer_id: str, message: str, order_id: str | None = None) -> dict:
        supervisor = self.supervisor.plan(message, order_id)
        intent = self.intent_agent.classify(message)
        order = self.order_agent.fetch(message, order_id) if supervisor["run_order_agent"] else None
        policies = self.policy_agent.retrieve(message, intent["intent"]) if supervisor["run_policy_agent"] else []
        reasoning = self.reasoning_agent.respond(message, intent, order, policies)
        validation = self.validation_agent.validate(reasoning["response"], policies)
        escalated, escalation_reason = self.escalation_service.should_escalate(
            reasoning["confidence"], validation, order
        )
        ticket_id = self.ticket_service.save(
            {
                "customer_id": customer_id,
                "message": message,
                "order_id": order_id,
                "response": reasoning["response"],
                "escalated": escalated,
                "trace": {
                    "supervisor": supervisor,
                    "intent": intent,
                    "order": order,
                    "policies": policies,
                    "reasoning": reasoning,
                    "validation": validation,
                },
            }
        )
        return {
            "ticket_id": ticket_id,
            "response": reasoning["response"],
            "confidence": reasoning["confidence"],
            "escalated": escalated,
            "escalation_reason": escalation_reason,
            "trace": {
                "supervisor": supervisor,
                "intent": intent,
                "order": order,
                "policies": policies,
                "reasoning": reasoning,
                "validation": validation,
            },
        }
