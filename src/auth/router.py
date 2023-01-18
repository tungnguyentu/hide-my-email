from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.config import Settings as settings
from src.database import get_db

from . import service, users
from .constants import ErrorCode
from .models import Account
from .schemas import AccountLogin, AccountRegister, AccountResponse, Token
from .security import create_access_token, hash_password

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


@router.post('/verify')
async def verify(token: str, db: Session = Depends(get_db)):
    email, password = service.get_signup_user(token)
    password = password.replace(settings.SECRET_KEY_SIGNUP, "")
    user = users.create(db=db, email=email, password=password)
    access_token_expires = timedelta(minutes=settings.JWT_EXP)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=Token)
async def register(user_in: AccountRegister):
    access_token_expires = timedelta(minutes=settings.JWT_EXP)
    plain_password = user_in.password.get_secret_value()
    hashed_password = hash_password(plain_password)
    access_token = create_access_token(
        data={
            "sub": user_in.email,
            "action": "signup",
            "pa": f"{hashed_password}{settings.SECRET_KEY_SIGNUP}"
        }, expires_delta=access_token_expires
    )
    service.send_email(user_in.email, access_token)
    return {"access_token": access_token, "token_type": "bearer"}
