import json
import re

import httpx

from app.utils.logger import get_logger

logger = get_logger(__name__)


class GeminiClient:
    def __init__(self, api_key: str | None = None, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model

    def validate(self, response: str, context: str) -> dict:
        if not self.api_key:
            logger.info("Gemini API key not configured; using local validation.")
            has_policy_context = bool(context.strip())
            return {
                "valid": has_policy_context and len(response.strip()) > 20,
                "issues": [] if has_policy_context else ["No policy context was supplied."],
            }

        prompt = f"""
Validate this customer support response against the policy context.
Return only JSON with keys: valid (boolean), issues (array of strings).

Policy context:
{context}

Customer response:
{response}
"""
        api_response = httpx.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent",
            params={"key": self.api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=45,
        )
        api_response.raise_for_status()
        text = api_response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return self._parse_json(text)

    def _parse_json(self, text: str) -> dict:
        cleaned = text.strip()
        fenced = re.search(r"```(?:json)?\s*(.*?)```", cleaned, flags=re.DOTALL)
        if fenced:
            cleaned = fenced.group(1).strip()
        return json.loads(cleaned)
