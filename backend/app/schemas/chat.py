from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field
from app.rag.sources import SourceMetadata


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, description="Message text content cannot be empty")


class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="message_metadata")
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ChatResponse(BaseModel):
    message: MessageResponse
    sources: List[SourceMetadata] = Field(default_factory=list)
    provider: str
    model: str
    skill: str
    artifact_id: Optional[str] = None
