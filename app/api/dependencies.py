from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session

from app.core.database import get_database_session
from app.core.security import verify_token
from app.models import User


def get_database() -> Generator[Session, None, None]:
    """
    Dépendance pour obtenir une session de base de données.
    """
    yield from get_database_session()


def get_current_user(
        access_token: Optional[str] = Cookie(None, alias="access_token"),
        database_session: Session = Depends(get_database)
) -> User:
    """
    Dépendance pour obtenir l'utilisateur actuellement connecté depuis le cookie.

    Args:
        access_token: Token JWT depuis le cookie
        database_session: Session de base de données

    Returns:
        L'utilisateur connecté

    Raises:
        HTTPException: Si le token est invalide ou l'utilisateur n'existe pas
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials"
    )

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access token not found"
        )

    user_id = verify_token(access_token)
    if user_id is None:
        raise credentials_exception

    user = database_session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


def get_current_user_id(
        current_user: User = Depends(get_current_user)
) -> str:
    """
    Dépendance pour obtenir uniquement l'ID de l'utilisateur connecté.

    Args:
        current_user: L'utilisateur connecté

    Returns:
        L'ID de l'utilisateur sous forme de string
    """
    return str(current_user.id)
