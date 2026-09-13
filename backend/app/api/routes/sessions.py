from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.session_service import SessionService
from app.schemas.session import SessionCreate, SessionResponse, SessionListResponse
from app.schemas.chat import MessageResponse

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    payload: Optional[SessionCreate] = None,
    db: AsyncSession = Depends(get_db),
):
    title = payload.title if payload else None
    user_id = payload.user_id if payload else None
    session = await SessionService.create_session(db, title=title, user_id=user_id)
    return session


@router.get("", response_model=SessionListResponse)
async def list_sessions(
    user_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    sessions = await SessionService.list_sessions(db, user_id=user_id)
    return SessionListResponse(sessions=[SessionResponse.model_validate(s) for s in sessions])


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    session = await SessionService.get_session(db, session_id)
    return session


@router.get("/{session_id}/messages", response_model=List[MessageResponse])
async def get_session_messages(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    messages = await SessionService.get_session_messages(db, session_id)
    return [MessageResponse.model_validate(m) for m in messages]
