import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import UserModel
    from app.models.message import MessageModel
    from app.models.artifact import ArtifactModel


class SessionModel(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[Optional["UserModel"]] = relationship("UserModel", back_populates="sessions")
    messages: Mapped[List["MessageModel"]] = relationship("MessageModel", back_populates="session", cascade="all, delete-orphan", order_by="MessageModel.created_at")
    artifacts: Mapped[List["ArtifactModel"]] = relationship("ArtifactModel", back_populates="session", cascade="all, delete-orphan")
