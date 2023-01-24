from datetime import timedelta
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.config import Settings as settings
from src.database import get_db

from . import service, users
from .constants import ErrorCode
from .models import Account
from .schemas import AccountLogin, AccountRegister, AccountResponse, Token
from .security import create_access_token, hash_password

router = APIRouter()
router.mount("/static", StaticFiles(directory="/home/tungnt/Documents/hide-my-email/src/auth/static"), name="static")

templates = Jinja2Templates(directory="/home/tungnt/Documents/hide-my-email/src/auth/templates")

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
async def register(background_tasks: BackgroundTasks, user_in: AccountRegister, db: Session = Depends(get_db)):
    user = users.get_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
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
    background_tasks.add_task(service.send_email, recipient=user_in.email, token=access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify", response_class=HTMLResponse)
async def verify(request: Request, token: str, db: Session = Depends(get_db)):
    try:
        email, password = await service.get_signup_user(token)
        user = users.get_by_email(db, email)
        if user:
            raise Exception
        password = password.replace(settings.SECRET_KEY_SIGNUP, "")
        users.create(db=db, email=email, password=password)
        return templates.TemplateResponse("signup-success.html", context={"request": request, "email": email})
    except Exception:
        return templates.TemplateResponse("index.html", context={"request": request})