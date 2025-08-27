from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from uuid import UUID


class WatchlistBase(BaseModel):
    title: str = Field(..., max_length=255)


class WatchlistCreate(WatchlistBase):
    pass


class WatchlistUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)


class MediaInWatchlist(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tmdb_id: int


class WatchlistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    author_id: UUID
    medias: List[MediaInWatchlist] = []
    medias_count: int = 0


class WatchlistDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    medias: List["MediaResponse"] = []
    medias_count: int = 0
