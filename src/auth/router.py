from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.config import Settings as settings
from src.database import get_db

from . import service, users
from .constants import ErrorCode
from .schemas import Token, AccountLogin, AccountRegister, AccountResponse
from .models import Account
from .security import create_access_token

router = APIRouter()



@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user_in = AccountLogin(email=form_data.username, password=form_data.password)
    user = service.authenticate(db=db, user_in=user_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.JWT_EXP)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=Token)
async def register(user_in: AccountRegister, db: Session = Depends(get_db)):
    user = users.create(db=db, user_in=user_in)
    access_token_expires = timedelta(minutes=settings.JWT_EXP)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/me", response_model=AccountResponse)
def read_users_me(current_user: Account = Depends(service.get_jwt_user_active)) -> Any:
    """
    Test access token
    """
    return current_user
