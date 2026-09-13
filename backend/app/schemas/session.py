from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class SessionCreate(BaseModel):
    title: Optional[str] = None
    user_id: Optional[str] = None


class SessionResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SessionListResponse(BaseModel):
    sessions: List[SessionResponse]
