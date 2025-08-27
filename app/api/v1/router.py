from fastapi import APIRouter

from app.api.v1 import auth, users, watchlists, medias, views, statistics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(watchlists.router, prefix="/watchlists", tags=["watchlists"])
api_router.include_router(medias.router, prefix="/medias", tags=["medias"])
api_router.include_router(views.router, prefix="/views", tags=["views"])
api_router.include_router(statistics.router, prefix="/stats", tags=["statistics"])