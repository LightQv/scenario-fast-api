from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from app.api.dependencies import get_database, get_current_user
from app.models import User, View
from app.schemas import ViewCreate, ViewResponse

router = APIRouter()


@router.get("/{user_id}", response_model=List[ViewResponse])
def get_user_views(
        user_id: UUID,
        database_session: Session = Depends(get_database)
) -> List[ViewResponse]:
    """
    Récupère toutes les vues d'un utilisateur.

    Args:
        user_id: ID de l'utilisateur
        database_session: Session de base de données

    Returns:
        Liste des vues de l'utilisateur
    """
    views = database_session.query(View).filter(View.viewer_id == user_id).all()
    return [ViewResponse.model_validate(view) for view in views]


@router.get("/{media_type}/{user_id}", response_model=List[ViewResponse])
def get_user_views_by_type(
        media_type: str,
        user_id: UUID,
        genre: Optional[int] = Query(None, description="Filtrer par genre"),
        database_session: Session = Depends(get_database)
) -> List[ViewResponse]:
    """
    Récupère les vues d'un utilisateur filtrées par type de média et optionnellement par genre.

    Args:
        media_type: Type de média (movie, tv)
        user_id: ID de l'utilisateur
        genre: ID du genre pour filtrer (optionnel)
        database_session: Session de base de données

    Returns:
        Liste des vues filtrées
    """
    query = database_session.query(View).filter(
        View.viewer_id == user_id,
        View.media_type == media_type
    )

    if genre is not None:
        query = query.filter(View.genre_ids.any(genre))

    views = query.all()
    return [ViewResponse.model_validate(view) for view in views]


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_view(
        view_data: ViewCreate,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
) -> dict:
    """
    Ajoute une nouvelle vue (média regardé).

    Args:
        view_data: Données de la vue à ajouter
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Returns:
        Message de confirmation

    Raises:
        HTTPException: Si l'utilisateur n'a pas les droits
    """
    # Vérifier que l'utilisateur ajoute une vue pour lui-même
    if str(view_data.viewer_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add view for this user"
        )

    new_view = View(
        tmdb_id=view_data.tmdb_id,
        genre_ids=view_data.genre_ids,
        poster_path=view_data.poster_path,
        backdrop_path=view_data.backdrop_path,
        release_date=view_data.release_date,
        release_year=view_data.release_year,
        runtime=view_data.runtime,
        title=view_data.title,
        media_type=view_data.media_type,
        viewer_id=view_data.viewer_id
    )

    database_session.add(new_view)
    database_session.commit()

    return {"message": "View added successfully"}


@router.delete("/{view_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_view(
        view_id: UUID,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
):
    """
    Supprime une vue.

    Args:
        view_id: ID de la vue à supprimer
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Raises:
        HTTPException: Si la vue n'existe pas ou si l'utilisateur n'a pas les droits
    """
    view = database_session.query(View).filter(View.id == view_id).first()

    if not view:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="View not found"
        )

    # Vérifier que l'utilisateur possède cette vue
    if str(view.viewer_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this view"
        )

    database_session.delete(view)
    database_session.commit()
