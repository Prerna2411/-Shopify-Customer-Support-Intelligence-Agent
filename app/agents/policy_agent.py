from app.rag.retriever import retrieve_policies


class PolicyAgent:
    def retrieve(self, message: str, intent: str | None = None) -> list[dict]:
        query = f"{intent or ''} {message}".strip()
        return retrieve_policies(query, k=4)
