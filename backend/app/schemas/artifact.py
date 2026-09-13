from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field


class ArtifactCreate(BaseModel):
    title: str = "Untitled Artifact"
    type: str  # markdown, html
    content: str
    message_id: Optional[str] = None


class ArtifactResponse(BaseModel):
    id: str
    session_id: str
    message_id: Optional[str] = None
    title: str
    type: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="artifact_metadata")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ArtifactListResponse(BaseModel):
    artifacts: List[ArtifactResponse]

