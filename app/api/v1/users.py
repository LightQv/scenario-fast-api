from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from app.api.dependencies import get_database, get_current_user
from app.core.security import hash_password
from app.models import User
from app.schemas import (
    UserResponse, UserPublic, UserBanner, UserUpdate, UserUpdateEmail,
    UserUpdatePassword, UserUpdateBanner
)

router = APIRouter()


@router.get("/{user_id}", response_model=UserPublic)
def get_user(
        user_id: UUID,
        database_session: Session = Depends(get_database)
) -> UserPublic:
    """
    Récupère les informations publiques d'un utilisateur.

    Args:
        user_id: ID de l'utilisateur
        database_session: Session de base de données

    Returns:
        Informations publiques de l'utilisateur

    Raises:
        HTTPException: Si l'utilisateur n'existe pas
    """
    user = database_session.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserPublic.model_validate(user)


@router.get("/banner/{user_id}", response_model=UserBanner)
def get_user_banner(
        user_id: UUID,
        database_session: Session = Depends(get_database)
) -> UserBanner:
    """
    Récupère la bannière de profil d'un utilisateur.

    Args:
        user_id: ID de l'utilisateur
        database_session: Session de base de données

    Returns:
        Bannière de profil de l'utilisateur

    Raises:
        HTTPException: Si l'utilisateur n'existe pas
    """
    user = database_session.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserBanner.model_validate(user)


@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user(
        user_id: UUID,
        user_data: UserUpdate,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
):
    """
    Met à jour les informations complètes d'un utilisateur.

    Args:
        user_id: ID de l'utilisateur à modifier
        user_data: Nouvelles données utilisateur
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Raises:
        HTTPException: Si l'utilisateur n'a pas les droits ou si l'utilisateur n'existe pas
    """
    # Vérifier que l'utilisateur modifie ses propres données
    if str(current_user.id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this user"
        )

    user = database_session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Mettre à jour les champs fournis
    update_data = user_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    try:
        for field, value in update_data.items():
            setattr(user, field, value)
        database_session.commit()
    except IntegrityError:
        database_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )


@router.put("/email/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user_email(
        user_id: UUID,
        email_data: UserUpdateEmail,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
):
    """
    Met à jour uniquement l'email d'un utilisateur.

    Args:
        user_id: ID de l'utilisateur à modifier
        email_data: Nouvel email
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Raises:
        HTTPException: Si l'utilisateur n'a pas les droits ou si l'utilisateur n'existe pas
    """
    if str(current_user.id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this user"
        )

    user = database_session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        user.email = email_data.email
        database_session.commit()
    except IntegrityError:
        database_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )


@router.put("/password/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user_password(
        user_id: UUID,
        password_data: UserUpdatePassword,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
):
    """
    Met à jour uniquement le mot de passe d'un utilisateur.

    Args:
        user_id: ID de l'utilisateur à modifier
        password_data: Nouveau mot de passe
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Raises:
        HTTPException: Si l'utilisateur n'a pas les droits ou si l'utilisateur n'existe pas
    """
    if str(current_user.id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this user"
        )

    user = database_session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.hashed_password = hash_password(password_data.password)
    user.password_token = None  # Invalider tout token de réinitialisation
    database_session.commit()


@router.put("/banner/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user_banner(
        user_id: UUID,
        banner_data: UserUpdateBanner,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
):
    """
    Met à jour la bannière de profil d'un utilisateur.

    Args:
        user_id: ID de l'utilisateur à modifier
        banner_data: Nouvelle URL de bannière
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Raises:
        HTTPException: Si l'utilisateur n'a pas les droits ou si l'utilisateur n'existe pas
    """
    if str(current_user.id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this user"
        )

    user = database_session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.profile_banner = banner_data.banner_link
    database_session.commit()


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_id: UUID,
        current_user: User = Depends(get_current_user),
        database_session: Session = Depends(get_database)
):
    """
    Supprime un utilisateur et toutes ses données associées.

    Args:
        user_id: ID de l'utilisateur à supprimer
        current_user: Utilisateur connecté
        database_session: Session de base de données

    Raises:
        HTTPException: Si l'utilisateur n'a pas les droits ou si l'utilisateur n'existe pas
    """
    if str(current_user.id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )

    user = database_session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    database_session.delete(user)
    database_session.commit()