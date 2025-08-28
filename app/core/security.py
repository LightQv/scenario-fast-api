from datetime import datetime, timedelta
from typing import Any, Union, Optional
import jwt
import bcrypt
import uuid

from app.core.exceptions.custom_exception import CustomExceptionError
from app.core.settings import settings
from app.services.constant.response_constant import EXPIRED_TOKEN_ERROR, INVALID_TOKEN_ERROR


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
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_IN
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
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
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except jwt.ExpiredSignatureError as error:
        raise CustomExceptionError(EXPIRED_TOKEN_ERROR) from error
    except jwt.InvalidTokenError as error:
        raise CustomExceptionError(INVALID_TOKEN_ERROR) from error
    except Exception as error:
        raise error

def hash_password(password: str) -> str:
    """
    Hashe un mot de passe avec bcrypt.

    Args:
        password: Le mot de passe en clair

    Returns:
        Le mot de passe hashé
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie un mot de passe contre son hash.

    Args:
        plain_password: Le mot de passe en clair
        hashed_password: Le hash à vérifier

    Returns:
        True si le mot de passe correspond
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def generate_password_reset_token() -> str:
    """
    Génère un token unique pour la réinitialisation de mot de passe.

    Returns:
        Un UUID4 sous forme de string
    """
    return str(uuid.uuid4())