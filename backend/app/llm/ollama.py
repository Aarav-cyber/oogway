import httpx
from typing import List, Dict, Any, Optional
from app.llm.base import BaseLLMProvider
from app.core.config import settings
from app.core.errors import LLMUnavailableError


class OllamaProvider(BaseLLMProvider):
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.OLLAMA_MODEL

    async def check_availability(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                return res.status_code == 200
        except Exception:
            return False

    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        for m in messages:
            formatted_messages.append({"role": m["role"], "content": m["content"]})

        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(f"{self.base_url}/api/chat", json=payload)
                if res.status_code != 200:
                    raise LLMUnavailableError("ollama", f"Ollama returned HTTP {res.status_code}: {res.text}")
                data = res.json()
                return data.get("message", {}).get("content", "")
        except httpx.TimeoutException:
            raise LLMUnavailableError("ollama", "Connection to Ollama timed out.")
        except httpx.RequestError as e:
            raise LLMUnavailableError("ollama", f"Failed to connect to Ollama: {str(e)}")
