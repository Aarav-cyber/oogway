from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db
from app.llm.factory import LLMFactory
from app.llm.runtime import get_current_provider, get_current_model

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

    current_p = get_current_provider()
    current_m = get_current_model(current_p)

    llm_status = "ok"
    try:
        provider = LLMFactory.get_provider(current_p)
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
        "provider": current_p,
        "model": current_m,
    }
