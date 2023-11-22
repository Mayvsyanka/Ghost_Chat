"""The service of sending an e-mail to the user"""

from pathlib import Path
from email.message import EmailMessage
#from fastapi_mail.errors import ConnectionErrors
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException

from src.services.auth import auth_service
from src.conf.config import settings


class ConnectionConfig(BaseModel):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool
    TEMPLATE_FOLDER: Path


class MessageType:
    html = "html"
    plain = "plain"


class MessageSchema(BaseModel):
    subject: str
    recipients: list
    template_body: dict
    subtype: str


class FastMail:
    def __init__(self, conf):
        self.conf = conf

    async def send_message(self, message, template_name):
        # Implement your send_message logic here
        pass


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    The send_email function sends an email to the user with a link to confirm their email address.

    :param email: Specify the email address of the recipient
    :type email: str
    :param username: Pass the username to the email template
    :type username: str
    :param host: Pass the host name of the server to be used in the email template
    :type host: str
    :return: The token_verification
    :rtype: str
    """
    token_verification = auth_service.create_email_token({"sub": email})
    message = MessageSchema(
        subject="Confirm your email ",
        recipients=[email],
        template_body={"host": host, "username": username,
                       "token": token_verification},
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email_template.html")
    #except ConnectionErrors as err:
        # Log the error for better visibility
   #     print(f"Error sending email: {err}")


async def send_email_forgot(email: str, link: str):
    """
    The send_email_forgot function sends an email to the user with a link for password reset.

    :param email: Specify the email address of the recipient
    :type email: str
    :param link: Pass the link to the email template
    :type link: str
    :return: The token_verification
    :rtype: str
    """
    token_verification = auth_service.create_email_token({"sub": email})
    message = MessageSchema(
        subject="Forgot your password?",
        recipients=[email],
        template_body={"link": link},
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="forget_email.html")

