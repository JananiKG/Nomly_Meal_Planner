import httpx
from .base import AIProvider
from backend.config import settings

class GeminiProvider(AIProvider):
    def generate(self, prompt: str) -> str:
        resp = httpx.post(
            settings.GEMINI_URL,
            headers={"Authorization": f"Bearer {settings.GEMINI_KEY}"},
            json={"prompt": prompt}
        )
        resp.raise_for_status()
        return resp.json().get("output", "")
