import json

import httpx

from app.utils.logger import get_logger

logger = get_logger(__name__)


class GroqClient:
    def __init__(
        self,
        api_key: str | None = None,
        model: str = "llama-3.3-70b-versatile",
        base_url: str = "https://api.groq.com/openai/v1",
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    def complete(self, prompt: str, system: str | None = None) -> str:
        if not self.api_key:
            logger.info("Groq API key not configured; using deterministic local response.")
            return prompt

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }
        if "json" in prompt.lower():
            payload["response_format"] = {"type": "json_object"}

        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=45,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def complete_json(self, prompt: str, system: str | None = None) -> dict:
        return json.loads(self.complete(prompt, system))
