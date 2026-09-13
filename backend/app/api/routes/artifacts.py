from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.artifact_service import ArtifactService
from app.schemas.artifact import ArtifactCreate, ArtifactResponse, ArtifactListResponse

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.post("", response_model=ArtifactResponse, status_code=status.HTTP_201_CREATED)
async def create_artifact(
    session_id: str,
    payload: ArtifactCreate,
    db: AsyncSession = Depends(get_db),
):
    artifact = await ArtifactService.create_artifact(
        db=db,
        session_id=session_id,
        title=payload.title,
        type=payload.type,
        content=payload.content,
        message_id=payload.message_id,
    )
    return artifact


@router.get("/{artifact_id}", response_model=ArtifactResponse)
async def get_artifact(
    artifact_id: str,
    db: AsyncSession = Depends(get_db),
):
    artifact = await ArtifactService.get_artifact(db, artifact_id)
    return artifact


@router.get("/session/{session_id}", response_model=ArtifactListResponse)
async def list_session_artifacts(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    artifacts = await ArtifactService.list_session_artifacts(db, session_id)
    return ArtifactListResponse(artifacts=[ArtifactResponse.model_validate(a) for a in artifacts])
