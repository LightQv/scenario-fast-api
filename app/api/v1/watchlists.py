from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from typing import List, Optional

from app.api.dependencies import get_database, get_current_user
from app.models import User, Watchlist, Media
from app.schemas import WatchlistCreate, WatchlistUpdate, WatchlistResponse, WatchlistDetail, MediaResponse

router = APIRouter()


@router.get("/{user_id}", response_model=List[WatchlistResponse])
def get_user_watchlists(
        user_id: UUID,
        database_session: Session = Depends(get_database)
) -> List[WatchlistResponse]:
    """
    Récupère toutes les watchlists d'un utilisateur.

    Args:
        user_id: ID de l'utilisateur
        database_session: Session de base de données

    Returns:
        Liste des watchlists de l'utilisateur
    """
    watchlists = database_session.query(
        Watchlist.id,
        Watchlist.title,
        Watchlist.author_id,
        func.count(Media.id).label('medias_count')
    ).outerjoin(
        Media, Watchlist.id == Media.watchlist_id
    ).filter(
        Watchlist.author_id == user_id
    ).group_by(
        Watchlist.id, Watchlist.title, Watchlist.author_id
    ).all()

    result = []
    for watchlist_data in watchlists:
        # Récupérer les médias pour chaque watchlist
        medias = database_session.query(Media.id, Media.tmdb_id).filter(
            Media.watchlist_id == watchlist_data.id
        ).all()

        watchlist_response = WatchlistResponse(
            id=watchlist_data.id,
            title=watchlist_data.title,
            author_id=watchlist_data.author_id,
            medias=[{"id": media.id, "tmdb_id": media.tmdb_id} for media in medias],
            medias_count=watchlist_data.medias_count or 0
        )
        result.append(watchlist_response)

    return result


@router.get("/detail/{watchlist_id}", response_model=WatchlistDetail)
def get_watchlist_details(
        watchlist_id: UUID,
        genre: Optional[int] = Query(None, description="Filtrer par genre"),
        database_session: Session = Depends(get_database)
) -> WatchlistDetail:
    """
    Récupère les détails d'une watchlist avec ses médias.

    Args:
        watchlist_id: ID de la watchlist
        genre: Genre pour filtrer les médias (optionnel)
        database_session: Session de base de données

    Returns:
        Détails de la watchlist

    Raises:
        HTTPException: Si la watchlist n'existe pas
    """
    watchlist = database_session.query(Watchlist).filter(Watchlist.id == watchlist_id).first()

    if not watchlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist not found"
        )

    # Construire la requête pour les médias
    media_query = database_session.query(Media).filter(Media.watchlist_id == watchlist_id)

    # Filtrer par genre si spécifié
    if genre is not None:
        media_query = media_query.filter(Media.genre_ids.any(genre))

    medias = media_query.all()

    # Compter le nombre total de médias
    total_medias_count = database_session.query(func.count(Media.id)).filter(
        Media.watchlist_id == watchlist_id
    ).scalar()

    return WatchlistDetail(
        title=watchlist.title,
        medias=[MediaResponse.model_validate(media) for media in medias],
        medias_count=total_medias_count
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_watchlist(
        watchlist_data: WatchlistCreate,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
) -> dict:
    """
    Crée une nouvelle watchlist.

    Args:
        watchlist_data: Données de la nouvelle watchlist
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Returns:
        Message de confirmation
    """
    new_watchlist = Watchlist(
        title=watchlist_data.title,
        author_id=current_user.id
    )

    database_session.add(new_watchlist)
    database_session.commit()

    return {"message": "Watchlist created successfully"}


@router.put("/{watchlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_watchlist(
        watchlist_id: UUID,
        watchlist_data: WatchlistUpdate,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
):
    """
    Met à jour une watchlist.

    Args:
        watchlist_id: ID de la watchlist à modifier
        watchlist_data: Nouvelles données de la watchlist
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Raises:
        HTTPException: Si la watchlist n'existe pas ou si l'utilisateur n'a pas les droits
    """
    watchlist = database_session.query(Watchlist).filter(Watchlist.id == watchlist_id).first()

    if not watchlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist not found"
        )

    # Vérifier que l'utilisateur est propriétaire de la watchlist
    if str(watchlist.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this watchlist"
        )

    # Mettre à jour les champs fournis
    update_data = watchlist_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(watchlist, field, value)

    database_session.commit()


@router.delete("/{watchlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_watchlist(
        watchlist_id: UUID,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
):
    """
    Supprime une watchlist et tous ses médias associés.

    Args:
        watchlist_id: ID de la watchlist à supprimer
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Raises:
        HTTPException: Si la watchlist n'existe pas ou si l'utilisateur n'a pas les droits
    """
    watchlist = database_session.query(Watchlist).filter(Watchlist.id == watchlist_id).first()

    if not watchlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist not found"
        )

    # Vérifier que l'utilisateur est propriétaire de la watchlist
    if str(watchlist.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this watchlist"
        )

    database_session.delete(watchlist)
    database_session.commit()