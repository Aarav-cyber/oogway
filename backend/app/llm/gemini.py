from typing import List, Dict, Optional

from app.llm.base import BaseLLMProvider
from app.core.config import settings
from app.core.errors import LLMUnavailableError, LLMConfigurationError


class GeminiProvider(BaseLLMProvider):
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = model or settings.GEMINI_MODEL

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
                "Gemini API key is not configured."
            )

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)

            contents = []

            for message in messages:
                role = message["role"]

                if role == "assistant":
                    role = "model"

                contents.append(
                    types.Content(
                        role=role,
                        parts=[
                            types.Part.from_text(
                                text=message["content"]
                            )
                        ],
                    )
                )

            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                system_instruction=system_prompt,
            )

            response = await client.aio.models.generate_content(
                model=self.model,
                contents=contents,
                config=config,
            )

            return response.text or ""

        except Exception as e:
            raise LLMUnavailableError("gemini", str(e))