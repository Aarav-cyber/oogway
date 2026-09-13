from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.session import SessionModel
from app.models.message import MessageModel
from app.core.errors import SessionNotFoundError


class SessionService:
    @staticmethod
    async def create_session(db: AsyncSession, title: Optional[str] = None, user_id: Optional[str] = None) -> SessionModel:
        session = SessionModel(
            id=str(uuid.uuid4()),
            title=title or "New Chat",
            user_id=user_id,
        )
        db.add(session)
        await db.flush()
        return session

    @staticmethod
    async def get_session(db: AsyncSession, session_id: str) -> SessionModel:
        result = await db.execute(select(SessionModel).where(SessionModel.id == session_id))
        session = result.scalar_one_or_none()
        if not session:
            raise SessionNotFoundError(session_id)
        return session

    @staticmethod
    async def list_sessions(db: AsyncSession, user_id: Optional[str] = None) -> List[SessionModel]:
        query = select(SessionModel)
        if user_id:
            query = query.where(SessionModel.user_id == user_id)
        query = query.order_by(SessionModel.updated_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_session_messages(db: AsyncSession, session_id: str) -> List[MessageModel]:
        await SessionService.get_session(db, session_id)  # verify session exists
        result = await db.execute(
            select(MessageModel)
            .where(MessageModel.session_id == session_id)
            .order_by(MessageModel.created_at.asc())
        )
        return list(result.scalars().all())
