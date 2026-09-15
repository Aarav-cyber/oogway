from typing import List, Dict, Optional

from app.llm.base import BaseLLMProvider
from app.core.config import settings
from app.core.errors import LLMUnavailableError, LLMConfigurationError


class GroqProvider(BaseLLMProvider):
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_MODEL

    async def check_availability(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if not await self.check_availability():
            raise LLMConfigurationError(
                "Groq API key is not configured."
            )

        try:
            from groq import AsyncGroq

            client = AsyncGroq(api_key=self.api_key)

            formatted_messages = []

            if system_prompt:
                formatted_messages.append(
                    {
                        "role": "system",
                        "content": system_prompt,
                    }
                )

            for message in messages:
                formatted_messages.append(
                    {
                        "role": message["role"],
                        "content": message["content"],
                    }
                )

            response = await client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return response.choices[0].message.content or ""

        except Exception as e:
            raise LLMUnavailableError("groq", str(e))