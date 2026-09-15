import httpx
from typing import List, Dict, Any, Optional
from app.llm.base import BaseLLMProvider
from app.core.config import settings
from app.core.errors import LLMUnavailableError, LLMConfigurationError


class GroqProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_MODEL

    async def check_availability(self) -> bool:
        if not self.api_key or not self.api_key.strip():
            return False
        # Optional lightweight HTTP check to Groq API models endpoint
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(
                    "https://api.groq.com/openai/v1/models",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                return res.status_code == 200
        except Exception:
            # If network error or invalid key
            return False

    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if not self.api_key or not self.api_key.strip():
            raise LLMConfigurationError("GROQ_API_KEY is not configured.")

        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        for m in messages:
            formatted_messages.append({"role": m["role"], "content": m["content"]})

        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
                if res.status_code != 200:
                    raise LLMUnavailableError("groq", f"Groq returned HTTP {res.status_code}: {res.text}")
                data = res.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except httpx.TimeoutException:
            raise LLMUnavailableError("groq", "Connection to Groq API timed out.")
        except httpx.RequestError as e:
            raise LLMUnavailableError("groq", f"Failed to connect to Groq API: {str(e)}")
