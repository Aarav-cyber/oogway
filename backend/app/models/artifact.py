import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.session import SessionModel


class ArtifactModel(Base):
    __tablename__ = "artifacts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(String, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    message_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False, default="Untitled Artifact")
    type: Mapped[str] = mapped_column(String, nullable=False)  # markdown, html
    content: Mapped[str] = mapped_column(Text, nullable=False)
    artifact_metadata: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    session: Mapped["SessionModel"] = relationship("SessionModel", back_populates="artifacts")
