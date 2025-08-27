from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from typing import List

from app.api.dependencies import get_database
from app.models import View
from app.schemas import ViewCountByType, ViewCountByYear, ViewRuntime

router = APIRouter()


@router.get("/count/{media_type}/{user_id}", response_model=List[ViewCountByType])
def get_view_count_by_type(
        media_type: str,
        user_id: UUID,
        database_session: Session = Depends(get_database)
) -> List[ViewCountByType]:
    """
    Récupère le nombre de vues par type de média pour un utilisateur.

    Args:
        media_type: Type de média (movie, tv)
        user_id: ID de l'utilisateur
        database_session: Session de base de données

    Returns:
        Statistiques de vues par type
    """
    results = database_session.query(
        View.media_type,
        func.count(View.id).label('count')
    ).filter(
        View.viewer_id == user_id,
        View.media_type == media_type
    ).group_by(View.media_type).all()

    return [
        ViewCountByType(media_type=result.media_type, count=result.count)
        for result in results
    ]


@router.get("/year/{media_type}/{user_id}", response_model=List[ViewCountByYear])
def get_view_count_by_year(
        media_type: str,
        user_id: UUID,
        database_session: Session = Depends(get_database)
) -> List[ViewCountByYear]:
    """
    Récupère le nombre de vues par année de sortie pour un utilisateur.

    Args:
        media_type: Type de média (movie, tv)
        user_id: ID de l'utilisateur
        database_session: Session de base de données

    Returns:
        Statistiques de vues par année
    """
    results = database_session.query(
        View.release_year,
        func.count(View.id).label('count')
    ).filter(
        View.viewer_id == user_id,
        View.media_type == media_type
    ).group_by(View.release_year).order_by(View.release_year.asc()).all()

    return [
        ViewCountByYear(release_year=result.release_year, count=result.count)
        for result in results
    ]


@router.get("/runtime/{media_type}/{user_id}", response_model=List[ViewRuntime])
def get_runtime_by_user(
        media_type: str,
        user_id: UUID,
        database_session: Session = Depends(get_database)
) -> List[ViewRuntime]:
    """
    Récupère les durées de tous les médias vus par un utilisateur.

    Args:
        media_type: Type de média (movie, tv)
        user_id: ID de l'utilisateur
        database_session: Session de base de données

    Returns:
        Liste des durées des médias vus
    """
    results = database_session.query(View.runtime).filter(
        View.viewer_id == user_id,
        View.media_type == media_type
    ).all()

    return [ViewRuntime(runtime=result.runtime) for result in results]