import pytest

from app.llm.factory import LLMFactory
from app.llm.ollama import OllamaProvider
from app.llm.groq import GroqProvider
from app.llm.gemini import GeminiProvider
from app.core.errors import LLMConfigurationError


def test_llm_factory_returns_correct_providers(monkeypatch):
    monkeypatch.undo()

    ollama = LLMFactory.get_provider("ollama")
    assert isinstance(ollama, OllamaProvider)

    groq = LLMFactory.get_provider("groq")
    assert isinstance(groq, GroqProvider)

    gemini = LLMFactory.get_provider("gemini")
    assert isinstance(gemini, GeminiProvider)


def test_llm_factory_invalid_provider(monkeypatch):
    monkeypatch.undo()

    with pytest.raises(LLMConfigurationError):
        LLMFactory.get_provider("invalid_provider")