from app.core.config import Settings


def test_settings_default_values():
    settings = Settings()
    assert settings.APP_ENV == "development"
    assert settings.LLM_PROVIDER == "ollama"
    assert settings.OLLAMA_BASE_URL == "http://localhost:11434"
    assert isinstance(settings.CORS_ORIGINS, list)


def test_cors_origins_parsing():
    settings = Settings(CORS_ORIGINS="http://localhost:3000,http://localhost:8000")
    assert settings.CORS_ORIGINS == ["http://localhost:3000", "http://localhost:8000"]
