from app.core.email import send_email
from app.utils.email_templates import get_password_reset_template


async def send_forgotten_password_email(user_email: str, username: str, reset_token: str) -> None:
    """
    Envoie un email de réinitialisation de mot de passe.

    Args:
        user_email: Email du destinataire
        username: Nom d'utilisateur
        reset_token: Token de réinitialisation

    Raises:
        Exception: Si l'envoi échoue
    """
    html_content = get_password_reset_template(username, reset_token)

    await send_email(
        subject=f"{username}, have you forgot your password ?",
        email_to=[user_email],
        body=html_content,
    )