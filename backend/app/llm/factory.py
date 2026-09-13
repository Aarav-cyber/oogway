from typing import Optional
from app.llm.base import BaseLLMProvider
from app.llm.ollama import OllamaProvider
from app.llm.anthropic import AnthropicProvider
from app.llm.openai import OpenAIProvider
from app.core.config import settings
from app.core.errors import LLMConfigurationError


class LLMFactory:
    @staticmethod
    def get_provider(provider_name: Optional[str] = None) -> BaseLLMProvider:
        provider = (provider_name or settings.LLM_PROVIDER).lower()

        if provider == "ollama":
            return OllamaProvider()
        elif provider == "anthropic":
            return AnthropicProvider()
        elif provider == "openai":
            return OpenAIProvider()
        else:
            raise LLMConfigurationError(f"Unsupported LLM provider: '{provider}'. Supported options: ollama, anthropic, openai.")
