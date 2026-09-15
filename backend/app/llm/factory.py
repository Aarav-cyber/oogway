from typing import Optional
from app.llm.base import BaseLLMProvider
from app.llm.ollama import OllamaProvider
from app.llm.groq import GroqProvider
from app.llm.gemini import GeminiProvider
from app.llm.runtime import get_current_provider
from app.core.errors import LLMConfigurationError


class LLMFactory:
    @staticmethod
    def get_provider(provider_name: Optional[str] = None) -> BaseLLMProvider:
        provider = (provider_name or get_current_provider()).lower()

        if provider == "ollama":
            return OllamaProvider()

        elif provider == "groq":
            return GroqProvider()

        elif provider == "gemini":
            return GeminiProvider()

        else:
            raise LLMConfigurationError(
                f"Unsupported LLM provider: '{provider}'. "
                "Supported options: ollama, groq, gemini."
            )
