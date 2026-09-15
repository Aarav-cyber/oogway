from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.llm.factory import LLMFactory
from app.llm.runtime import get_current_provider, set_current_provider, get_current_model, PROVIDER_MODELS
from app.core.errors import AppError, LLMUnavailableError

router = APIRouter(prefix="/config", tags=["config"])


class LLMConfigPayload(BaseModel):
    provider: str = Field(..., description="Target LLM provider: ollama, groq, or gemini")


class LLMConfigResponse(BaseModel):
    provider: str
    model: str


@router.get("/llm", response_model=LLMConfigResponse)
async def get_llm_config():
    current_p = get_current_provider()
    current_m = get_current_model(current_p)
    return LLMConfigResponse(provider=current_p, model=current_m)


@router.post("/llm", response_model=LLMConfigResponse)
async def switch_llm_provider(payload: LLMConfigPayload):
    requested_p = payload.provider.lower().strip()

    if requested_p not in PROVIDER_MODELS:
        raise AppError(
            code="INVALID_PROVIDER",
            message=f"Invalid provider '{payload.provider}'. Supported providers: ollama, groq, gemini.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Instantiate provider and check availability BEFORE switching
    try:
        provider_obj = LLMFactory.get_provider(requested_p)
        is_available = await provider_obj.check_availability()
    except Exception as e:
        raise LLMUnavailableError(requested_p, str(e))

    if not is_available:
        raise LLMUnavailableError(requested_p, f"{requested_p.capitalize()} is currently unavailable or API key is invalid.")

    # Apply switch to runtime state
    set_current_provider(requested_p)
    model_name = get_current_model(requested_p)

    return LLMConfigResponse(provider=requested_p, model=model_name)
