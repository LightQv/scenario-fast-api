from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class Watchlist(Base):
    __tablename__ = "watchlist_model"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    author = relationship("User", back_populates="watchlist")
    medias = relationship("Media", back_populates="watchlist", cascade="all, delete-orphan")
