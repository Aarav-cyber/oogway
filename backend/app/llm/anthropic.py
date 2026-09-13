from typing import List, Dict, Any, Optional
from app.llm.base import BaseLLMProvider
from app.core.config import settings
from app.core.errors import LLMUnavailableError, LLMConfigurationError


class AnthropicProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.model = model or settings.ANTHROPIC_MODEL

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
            raise LLMConfigurationError("Anthropic API key is not configured.")

        try:
            from anthropic import AsyncAnthropic
            client = AsyncAnthropic(api_key=self.api_key)

            formatted_messages = []
            for m in messages:
                if m["role"] in ["user", "assistant"]:
                    formatted_messages.append({"role": m["role"], "content": m["content"]})

            kwargs: Dict[str, Any] = {
                "model": self.model,
                "messages": formatted_messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            if system_prompt:
                kwargs["system"] = system_prompt

            res = await client.messages.create(**kwargs)
            return res.content[0].text
        except Exception as e:
            raise LLMUnavailableError("anthropic", str(e))
