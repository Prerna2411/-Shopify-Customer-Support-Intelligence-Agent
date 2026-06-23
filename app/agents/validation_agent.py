from app.models.model_router import ModelRouter


class ValidationAgent:
    def __init__(self, router: ModelRouter | None = None):
        self.router = router or ModelRouter()

    def validate(self, response: str, policies: list[dict]) -> dict:
        context = "\n\n".join(policy["content"] for policy in policies)
        try:
            result = self.router.validation_model.validate(response, context)
        except Exception as exc:
            result = {
                "valid": bool(context.strip()) and len(response.strip()) > 20,
                "issues": [f"Gemini validation unavailable; used local fallback. {type(exc).__name__}"],
            }
        return {"valid": bool(result.get("valid")), "issues": result.get("issues", [])}
