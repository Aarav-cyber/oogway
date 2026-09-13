from typing import List, Dict, Any, Optional
from app.llm.base import BaseLLMProvider
from app.core.config import settings
from app.core.errors import LLMUnavailableError, LLMConfigurationError


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL

    async def check_availability(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 0)

    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if not await self.check_availability():
            raise LLMConfigurationError("OpenAI API key is not configured.")

        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.api_key)

            formatted_messages = []
            if system_prompt:
                formatted_messages.append({"role": "system", "content": system_prompt})
            for m in messages:
                formatted_messages.append({"role": m["role"], "content": m["content"]})

            res = await client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return res.choices[0].message.content or ""
        except Exception as e:
            raise LLMUnavailableError("openai", str(e))
