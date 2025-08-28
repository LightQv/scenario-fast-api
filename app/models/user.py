from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.base import Base


class User(Base):
    __tablename__ = "user_model"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    password_token = Column(String, nullable=True)
    profile_banner = Column(String, nullable=True)

    watchlists = relationship("Watchlist", back_populates="author", cascade="all, delete-orphan")
    views = relationship("View", back_populates="viewer", cascade="all, delete-orphan")

