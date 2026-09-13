import pytest
from app.llm.factory import LLMFactory
from app.llm.ollama import OllamaProvider
from app.llm.anthropic import AnthropicProvider
from app.llm.openai import OpenAIProvider
from app.core.errors import LLMConfigurationError


def test_llm_factory_returns_correct_providers(monkeypatch):
    monkeypatch.undo()  # un-mock factory for unit test
    ollama = LLMFactory.get_provider("ollama")
    assert isinstance(ollama, OllamaProvider)

    anthropic = LLMFactory.get_provider("anthropic")
    assert isinstance(anthropic, AnthropicProvider)

    openai = LLMFactory.get_provider("openai")
    assert isinstance(openai, OpenAIProvider)


def test_llm_factory_invalid_provider(monkeypatch):
    monkeypatch.undo()
    with pytest.raises(LLMConfigurationError):
        LLMFactory.get_provider("invalid_provider")
