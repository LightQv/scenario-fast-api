"""
Email sending module using FastAPI Mail.
"""
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr

from app.core.settings import settings

config = ConnectionConfig(
    MAIL_USERNAME=settings.smtp_user,
    MAIL_PASSWORD=settings.smtp_password,
    MAIL_FROM=settings.smtp_user,
    MAIL_PORT=settings.smtp_port,
    MAIL_SERVER=settings.smtp_host,
    MAIL_STARTTLS=settings.smtp_use_tls,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_email(
        subject: str,
        email_to: list[str] | list[EmailStr],
        body: str,
        attachments: list[dict[str, str | bytes]] | None = None,
) -> None:
    """
    Email the specified emails address.
    """
    if not email_to:
        raise ValueError("The email_to list cannot be empty.")

    mail_client = FastMail(config)

    message_args = {
        "subject": subject,
        "recipients": email_to,
        "body": body,
        "subtype": MessageType.html
    }

    if attachments:
        message_args["attachments"] = attachments

    message = MessageSchema(**message_args)

    await mail_client.send_message(message)
