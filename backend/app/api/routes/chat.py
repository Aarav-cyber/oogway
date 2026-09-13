from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.chat_service import ChatService
from app.schemas.chat import MessageCreate, ChatResponse

router = APIRouter(prefix="/sessions", tags=["chat"])


@router.post("/{session_id}/messages", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def post_chat_message(
    session_id: str,
    payload: MessageCreate,
    provider: Optional[str] = Query(None, description="Override LLM provider (ollama, anthropic, openai)"),
    db: AsyncSession = Depends(get_db),
):
    response = await ChatService.process_chat_message(
        db=db,
        session_id=session_id,
        user_content=payload.content,
        provider_name=provider,
    )
    return response
