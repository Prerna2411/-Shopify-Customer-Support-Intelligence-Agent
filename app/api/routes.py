from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.api.schemas import TicketRequest, TicketResponse
from app.rag.ingest import ingest_policies
from app.rag.vector_store import collection_count
from app.workflows.langgraph_workflow import CustomerSupportWorkflow

router = APIRouter(prefix="/api", tags=["support"])
workflow = CustomerSupportWorkflow()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/rag/status")
def rag_status() -> dict:
    return {"collection_count": collection_count()}


@router.post("/rag/ingest")
def ingest_rag() -> dict:
    return ingest_policies(reset=True)


@router.post("/tickets", response_model=TicketResponse)
def submit_ticket(request: TicketRequest) -> dict:
    return workflow.run(
        customer_id=request.customer_id,
        message=request.message,
        order_id=request.order_id,
    )


@router.post("/tickets/text", response_class=PlainTextResponse)
def submit_ticket_text(request: TicketRequest) -> str:
    result = workflow.run(
        customer_id=request.customer_id,
        message=request.message,
        order_id=request.order_id,
    )
    return result["response"]
