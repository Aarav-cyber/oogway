from typing import Dict, Any, Optional
from pydantic import BaseModel


class SourceMetadata(BaseModel):
    document_id: str
    chunk_id: str
    title: str
    source_url: Optional[str] = None
    episode_date: Optional[str] = None
    snippet: Optional[str] = None


class RetrievedChunk(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    text: str
    source_url: Optional[str] = None
    score: float
    metadata: Dict[str, Any] = {}
