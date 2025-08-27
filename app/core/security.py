from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.hash import argon2
import uuid

from app.core.settings import settings

# Configuration Argon2 (même config que ton Express)
password_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,  # 2^16
    argon2__time_cost=5,
    argon2__parallelism=1,
)


def create_access_token(
        subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crée un token JWT pour l'authentification.

    Args:
        subject: L'identifiant du sujet (user_id généralement)
        expires_delta: Durée de vie du token (optionnel)

    Returns:
        Token JWT encodé
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """
    Vérifie et décode un token JWT.

    Args:
        token: Le token JWT à vérifier

    Returns:
        L'ID utilisateur si le token est valide, None sinon
    """
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None


def hash_password(password: str) -> str:
    """
    Hashe un mot de passe avec Argon2.

    Args:
        password: Le mot de passe en clair

    Returns:
        Le mot de passe hashé
    """
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie un mot de passe contre son hash.

    Args:
        plain_password: Le mot de passe en clair
        hashed_password: Le hash à vérifier

    Returns:
        True si le mot de passe correspond
    """
    return password_context.verify(plain_password, hashed_password)


def generate_password_reset_token() -> str:
    """
    Génère un token unique pour la réinitialisation de mot de passe.

    Returns:
        Un UUID4 sous forme de string
    """
    return str(uuid.uuid4())