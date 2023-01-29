from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.config import Settings as settings
from src.database import get_db

from . import users
from .constants import ErrorCode
from .schemas import TokenData, AccountLogin
from .models import Account
from .security import verify_password
import smtplib
from email.mime.text import MIMEText
from src import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_jwt_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorCode.COULD_NOT_VALIDATE_CREDENTIALS,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except Exception:
        raise credentials_exception

    email: str = payload.get("sub")
    if not email:
        raise credentials_exception

    token_data = TokenData(email=email)
    user = users.get_by_email(db, email=token_data.email)
    if not user:
        raise credentials_exception

    return user

async def get_signup_user(
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorCode.COULD_NOT_VALIDATE_CREDENTIALS,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except Exception:
        raise credentials_exception

    email: str = payload.get("sub")
    action: str = payload.get("action")
    pa: str = payload.get("pa")
    if not email or action != "signup" or settings.SECRET_KEY_SIGNUP not in pa:
        raise credentials_exception

    return email, pa

def get_jwt_user_active(current_user: Account = Depends(get_jwt_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.USER_IS_NOT_ACTIVE
        )
    return current_user


def authenticate(*, db: Session, user_in: AccountLogin):
    user_db = users.get_by_email(db, user_in.email)
    if not user_db:
        return

    if not verify_password(user_in.password, user_db.password):
        return

    return user_db


def send_email(token: str, recipient: str):
    sender_email = settings.NO_REPLY_SENDER
    sender_password = settings.NO_REPLY_PASSWORD

    # the subject and body of the email
    subject = "Xác minh email đăng ký Hide My Email"

    # create the HTML template for the body of the email
    verify_url = f"{settings.HOST}/auth/verify?token={token}"
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Montserrat', sans-serif;
            }
            h1 {
                font-weight: 600;
                margin-bottom: 20px;
            }
            .jumbotron {
                background-color: #f5f5f5;
                padding: 30px;
                border-radius: 10px;
            }
            .btn-success {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin-top: 20px;
            }
            a:link {
         color: white;
         background-color: transparent;
         text-decoration: none;
      }
        </style>
        <title>Verification Email</title>
    </head>
    <body>
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <div class="jumbotron text-center">
                        <h1>Chào mừng đến với Hide My Email!</h1>
                        <p>Cảm ơn bạn đã đăng ký dịch vụ.</p>
                        <p>Để hoàn tất quá trình đăng ký, vui lòng nhấn vào link xác minh bên dưới:</p>
                        <a href='"""+f"{verify_url}"+"""' class="btn btn-success" style="color: white" >Xác minh địa chỉ email</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # create a MIMEText object with the HTML template
    msg = MIMEText(template, 'html')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient
    server = smtplib.SMTP(settings.SMTP_HOST, 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()

    logger.info("The email was sent successfully.")