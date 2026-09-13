import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.artifact import ArtifactModel
from app.core.errors import AppError, SessionNotFoundError
from app.services.session_service import SessionService
from fastapi import status


class ArtifactService:
    @staticmethod
    async def create_artifact(
        db: AsyncSession,
        session_id: str,
        title: str,
        type: str,
        content: str,
        message_id: Optional[str] = None,
    ) -> ArtifactModel:
        await SessionService.get_session(db, session_id)
        artifact = ArtifactModel(
            id=str(uuid.uuid4()),
            session_id=session_id,
            message_id=message_id,
            title=title,
            type=type.lower(),
            content=content,
        )
        db.add(artifact)
        await db.flush()
        return artifact

    @staticmethod
    async def get_artifact(db: AsyncSession, artifact_id: str) -> ArtifactModel:
        result = await db.execute(select(ArtifactModel).where(ArtifactModel.id == artifact_id))
        artifact = result.scalar_one_or_none()
        if not artifact:
            raise AppError("ARTIFACT_NOT_FOUND", f"Artifact '{artifact_id}' not found.", status.HTTP_404_NOT_FOUND)
        return artifact

    @staticmethod
    async def list_session_artifacts(db: AsyncSession, session_id: str) -> List[ArtifactModel]:
        await SessionService.get_session(db, session_id)
        result = await db.execute(
            select(ArtifactModel)
            .where(ArtifactModel.session_id == session_id)
            .order_by(ArtifactModel.created_at.desc())
        )
        return list(result.scalars().all())
