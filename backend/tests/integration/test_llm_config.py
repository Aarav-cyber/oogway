import pytest
from app.llm.runtime import get_current_provider, set_current_provider
from app.llm.factory import LLMFactory
from app.llm.base import BaseLLMProvider


class MockAvailableProvider(BaseLLMProvider):
    async def check_availability(self) -> bool:
        return True

    async def generate(self, messages, system_prompt=None, temperature=0.7, max_tokens=2048) -> str:
        return "Mock response"


class MockUnavailableProvider(BaseLLMProvider):
    async def check_availability(self) -> bool:
        return False

    async def generate(self, messages, system_prompt=None, temperature=0.7, max_tokens=2048) -> str:
        return "Mock response"


@pytest.mark.asyncio
async def test_get_current_llm(client):
    res = await client.get("/config/llm")
    assert res.status_code == 200
    data = res.json()
    assert "provider" in data
    assert "model" in data


@pytest.mark.asyncio
async def test_switch_to_groq(client, monkeypatch):
    monkeypatch.setattr(LLMFactory, "get_provider", lambda p=None: MockAvailableProvider())

    res = await client.post("/config/llm", json={"provider": "groq"})
    assert res.status_code == 200
    data = res.json()
    assert data["provider"] == "groq"
    assert "model" in data
    assert get_current_provider() == "groq"


@pytest.mark.asyncio
async def test_switch_to_gemini(client, monkeypatch):
    monkeypatch.setattr(LLMFactory, "get_provider", lambda p=None: MockAvailableProvider())

    res = await client.post("/config/llm", json={"provider": "gemini"})
    assert res.status_code == 200
    data = res.json()
    assert data["provider"] == "gemini"
    assert get_current_provider() == "gemini"


@pytest.mark.asyncio
async def test_switch_to_ollama(client, monkeypatch):
    monkeypatch.setattr(LLMFactory, "get_provider", lambda p=None: MockAvailableProvider())

    res = await client.post("/config/llm", json={"provider": "ollama"})
    assert res.status_code == 200
    data = res.json()
    assert data["provider"] == "ollama"
    assert get_current_provider() == "ollama"


@pytest.mark.asyncio
async def test_reject_invalid_provider(client):
    initial_provider = get_current_provider()
    res = await client.post("/config/llm", json={"provider": "unknown_provider"})
    assert res.status_code == 400
    assert get_current_provider() == initial_provider


@pytest.mark.asyncio
async def test_reject_unavailable_provider(client, monkeypatch):
    set_current_provider("groq")
    monkeypatch.setattr(LLMFactory, "get_provider", lambda p=None: MockUnavailableProvider())

    res = await client.post("/config/llm", json={"provider": "ollama"})
    assert res.status_code == 503
    # Verify provider remains unchanged!
    assert get_current_provider() == "groq"
