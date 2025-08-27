import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from app.core.settings import settings
from app.utils.email_templates import get_password_reset_template


def send_forgotten_password_email(user_email: str, username: str, reset_token: str) -> None:
    """
    Envoie un email de réinitialisation de mot de passe.

    Args:
        user_email: Email du destinataire
        username: Nom d'utilisateur
        reset_token: Token de réinitialisation

    Raises:
        Exception: Si l'envoi échoue
    """
    try:
        # Créer le message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"{username}, have you forgot your password ?"
        message["From"] = settings.smtp_user
        message["To"] = user_email

        # Contenu HTML
        html_content = get_password_reset_template(username, reset_token)
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        # Envoyer l'email
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            if settings.smtp_use_tls:
                server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(message)

    except Exception as e:
        print(f"Error sending email: {e}")
        raise