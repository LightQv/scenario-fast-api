from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import get_database
from app.core.security import hash_password, verify_password, create_access_token, generate_password_reset_token
from app.models import User
from app.schemas import UserRegister, UserLogin, ForgottenPassword, PasswordReset, Token, UserResponse
from app.services.email_service import send_forgotten_password_email
from app.core.settings import settings

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
        user_data: UserRegister,
        database_session: Session = Depends(get_database)
) -> dict:
    """
    Crée un nouveau compte utilisateur.

    Args:
        user_data: Données d'inscription de l'utilisateur
        database_session: Session de base de données

    Returns:
        Message de confirmation

    Raises:
        HTTPException: Si l'email ou le nom d'utilisateur existe déjà
    """
    # Hasher le mot de passe
    hashed_password = hash_password(user_data.password)

    # Créer l'utilisateur
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )

    try:
        database_session.add(new_user)
        database_session.commit()
        return {"message": "User created successfully"}
    except IntegrityError:
        database_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )


@router.post("/login", response_model=UserResponse)
def login_user(
        user_credentials: UserLogin,
        response: Response,
        database_session: Session = Depends(get_database)
) -> UserResponse:
    """
    Connecte un utilisateur et définit le cookie d'authentification.

    Args:
        user_credentials: Identifiants de connexion
        response: Objet response FastAPI pour définir le cookie
        database_session: Session de base de données

    Returns:
        Données publiques de l'utilisateur

    Raises:
        HTTPException: Si les identifiants sont invalides
    """
    # Chercher l'utilisateur par email
    user = database_session.query(User).filter(User.email == user_credentials.email).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Créer le token JWT
    access_token = create_access_token(subject=user.id)

    # Définir le cookie d'authentification
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=not settings.DEBUG,  # HTTPS en production
        max_age=settings.JWT_ACCESS_TOKEN_EXPIRES_IN * 60,
        samesite="lax"
    )

    return UserResponse.model_validate(user)


@router.post("/forgotten-password", status_code=status.HTTP_200_OK)
async def request_password_reset(
        email_data: ForgottenPassword,
        database_session: Session = Depends(get_database)
) -> dict:
    """
    Envoie un email de réinitialisation de mot de passe.

    Args:
        email_data: Email de l'utilisateur
        database_session: Session de base de données

    Returns:
        Message de confirmation

    Raises:
        HTTPException: Si l'utilisateur n'existe pas
    """
    # Chercher l'utilisateur par email
    user = database_session.query(User).filter(User.email == email_data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Générer un token de réinitialisation
    reset_token = generate_password_reset_token()

    # Sauvegarder le token en base
    user.password_token = reset_token
    database_session.commit()

    # Envoyer l'email
    try:
        await send_forgotten_password_email(user.email, user.username, reset_token)
        return {"message": "Password reset email sent"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email"
        )


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(
        reset_data: PasswordReset,
        database_session: Session = Depends(get_database)
) -> dict:
    """
    Réinitialise le mot de passe avec le token reçu par email.

    Args:
        reset_data: Données de réinitialisation
        database_session: Session de base de données

    Returns:
        Message de confirmation

    Raises:
        HTTPException: Si le token est invalide
    """
    # Chercher l'utilisateur par token
    user = database_session.query(User).filter(User.password_token == reset_data.password_token).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )

    # Mettre à jour le mot de passe
    user.hashed_password = hash_password(reset_data.password)
    user.password_token = None  # Invalider le token
    database_session.commit()

    return {"message": "Password reset successfully"}


@router.get("/logout", status_code=status.HTTP_200_OK)
def logout_user(response: Response) -> dict:
    """
    Déconnecte l'utilisateur en supprimant le cookie d'authentification.

    Args:
        response: Objet response FastAPI pour supprimer le cookie

    Returns:
        Message de confirmation
    """
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax"
    )

    return {"message": "Logged out successfully"}