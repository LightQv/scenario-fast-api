from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID


class MediaBase(BaseModel):
    tmdb_id: int
    genre_ids: List[int] = [0]
    poster_path: str
    backdrop_path: str
    release_date: str
    runtime: int
    title: str
    media_type: str


class MediaCreate(MediaBase):
    watchlist_id: UUID


class MediaUpdate(BaseModel):
    watchlist_id: Optional[UUID] = None


class MediaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tmdb_id: int
    genre_ids: List[int]
    poster_path: str
    backdrop_path: str
    release_date: str
    runtime: int
    title: str
    media_type: str
    watchlist_id: UUID
