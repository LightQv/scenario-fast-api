from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.dependencies import get_database, get_current_user
from app.models import User, Media, Watchlist
from app.schemas import MediaCreate, MediaUpdate, MediaResponse

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_media_to_watchlist(
        media_data: MediaCreate,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
) -> dict:
    """
    Ajoute un média à une watchlist.

    Args:
        media_data: Données du média à ajouter
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Returns:
        Message de confirmation

    Raises:
        HTTPException: Si la watchlist n'existe pas ou si l'utilisateur n'a pas les droits
    """
    # Vérifier que la watchlist existe et appartient à l'utilisateur
    watchlist = database_session.query(Watchlist).filter(
        Watchlist.id == media_data.watchlist_id
    ).first()

    if not watchlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist not found"
        )

    if str(watchlist.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add media to this watchlist"
        )

    new_media = Media(
        tmdb_id=media_data.tmdb_id,
        genre_ids=media_data.genre_ids,
        poster_path=media_data.poster_path,
        backdrop_path=media_data.backdrop_path,
        release_date=media_data.release_date,
        runtime=media_data.runtime,
        title=media_data.title,
        media_type=media_data.media_type,
        watchlist_id=media_data.watchlist_id
    )

    database_session.add(new_media)
    database_session.commit()

    return {"message": "Media added successfully"}


@router.put("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_media(
        media_id: UUID,
        media_data: MediaUpdate,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
):
    """
    Met à jour un média (par exemple changer de watchlist).

    Args:
        media_id: ID du média à modifier
        media_data: Nouvelles données du média
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Raises:
        HTTPException: Si le média n'existe pas ou si l'utilisateur n'a pas les droits
    """
    media = database_session.query(Media).filter(Media.id == media_id).first()

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )

    # Vérifier que l'utilisateur possède la watchlist actuelle
    current_watchlist = database_session.query(Watchlist).filter(
        Watchlist.id == media.watchlist_id
    ).first()

    if str(current_watchlist.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this media"
        )

    # Si on change de watchlist, vérifier les droits sur la nouvelle
    if media_data.watchlist_id:
        new_watchlist = database_session.query(Watchlist).filter(
            Watchlist.id == media_data.watchlist_id
        ).first()

        if not new_watchlist or str(new_watchlist.author_id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to move media to this watchlist"
            )

        media.watchlist_id = media_data.watchlist_id

    database_session.commit()


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_media(
        media_id: UUID,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
):
    """
    Supprime un média d'une watchlist.

    Args:
        media_id: ID du média à supprimer
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Raises:
        HTTPException: Si le média n'existe pas ou si l'utilisateur n'a pas les droits
    """
    media = database_session.query(Media).filter(Media.id == media_id).first()

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )

    # Vérifier que l'utilisateur possède la watchlist
    watchlist = database_session.query(Watchlist).filter(
        Watchlist.id == media.watchlist_id
    ).first()

    if str(watchlist.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this media"
        )

    database_session.delete(media)
    database_session.commit()