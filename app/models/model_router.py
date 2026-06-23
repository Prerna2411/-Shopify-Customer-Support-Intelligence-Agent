from app.models.gemini_client import GeminiClient
from app.models.groq_client import GroqClient
from app.utils.config import get_settings


class ModelRouter:
    def __init__(self):
        settings = get_settings()
        self.intent_model = GroqClient(settings.groq_api_key, "llama-3.1-8b-instant")
        self.reasoning_model = GroqClient(settings.groq_api_key, "llama-3.3-70b-versatile")
        self.validation_model = GeminiClient(settings.gemini_api_key or settings.google_api_key, "gemini-1.5-flash")
