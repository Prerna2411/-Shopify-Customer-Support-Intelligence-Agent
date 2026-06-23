from typing import Any

from pydantic import BaseModel, Field


class TicketRequest(BaseModel):
    customer_id: str = Field(..., examples=["cust_001"])
    message: str = Field(..., examples=["My order #1234 has not arrived. Can I get a refund?"])
    order_id: str | None = Field(default=None, examples=["1234"])


class AgentTrace(BaseModel):
    supervisor: dict[str, Any]
    intent: dict[str, Any]
    order: dict[str, Any] | None
    policies: list[dict[str, Any]]
    reasoning: dict[str, Any]
    validation: dict[str, Any]


class TicketResponse(BaseModel):
    ticket_id: str
    response: str
    confidence: float
    escalated: bool
    escalation_reason: str | None = None
    trace: AgentTrace
