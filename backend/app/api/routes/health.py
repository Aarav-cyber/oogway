from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db
from app.llm.factory import LLMFactory
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    db_status = "ok"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "unavailable"

    llm_status = "ok"
    try:
        provider = LLMFactory.get_provider()
        is_available = await provider.check_availability()
        if not is_available:
            llm_status = "unavailable"
    except Exception:
        llm_status = "unavailable"

    overall = "ok" if db_status == "ok" and llm_status == "ok" else "degraded"

    return {
        "status": overall,
        "database": db_status,
        "llm": llm_status,
        "provider": settings.LLM_PROVIDER,
    }
