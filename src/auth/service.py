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
