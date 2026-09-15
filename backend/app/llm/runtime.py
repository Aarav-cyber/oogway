from app.core.config import settings

# Global runtime provider state initialized from settings.LLM_PROVIDER
_CURRENT_PROVIDER = settings.LLM_PROVIDER.lower()

PROVIDER_MODELS = {
    "ollama": settings.OLLAMA_MODEL,
    "groq": settings.GROQ_MODEL,
    "gemini": settings.GEMINI_MODEL,
}


def get_current_provider() -> str:
    return _CURRENT_PROVIDER


def set_current_provider(provider: str) -> None:
    global _CURRENT_PROVIDER
    p = provider.lower()
    if p not in PROVIDER_MODELS:
        raise ValueError(f"Unsupported provider: {provider}")
    _CURRENT_PROVIDER = p


def get_current_model(provider: str = None) -> str:
    p = (provider or _CURRENT_PROVIDER).lower()
    if p == "ollama":
        return settings.OLLAMA_MODEL
    elif p == "groq":
        return settings.GROQ_MODEL
    elif p == "gemini":
        return settings.GEMINI_MODEL
    return "unknown"
