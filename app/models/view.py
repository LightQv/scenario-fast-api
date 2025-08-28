from sqlalchemy import Column, String, Integer, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.base import Base


class View(Base):
    __tablename__ = "view_model"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tmdb_id = Column(Integer, nullable=False)
    genre_ids = Column(ARRAY(Integer), default=[0])
    poster_path = Column(String, nullable=False)
    backdrop_path = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    release_year = Column(String, nullable=False)
    runtime = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    media_type = Column(String, nullable=False)
    viewer_id = Column(UUID(as_uuid=True), ForeignKey("user_model.id", ondelete="CASCADE"), nullable=False)

    viewer = relationship("User", back_populates="views")