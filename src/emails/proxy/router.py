from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.models import Account

from src.database import get_db
from src.emails.proxy.schemas import ProxiesGenerated, ProxyResponse, ProxyCreate, PasswordGenerated
from src.emails.proxy import service
from src.auth.service import get_jwt_user_active


router = APIRouter()


@router.post("", response_model=ProxiesGenerated, status_code=status.HTTP_200_OK, dependencies=[Depends(get_jwt_user_active)])
def create(db: Session = Depends(get_db), account: Account = Depends(get_jwt_user_active)):
    return service.choice_random_email(db, account.id)


@router.get("", response_model=List[ProxyResponse], status_code=status.HTTP_200_OK, dependencies=[Depends(get_jwt_user_active)])
def get_all(db: Session = Depends(get_db), account: Account = Depends(get_jwt_user_active)):
    return service.get_users(db, account.id)


@router.post("/password", response_model=PasswordGenerated, status_code=status.HTTP_200_OK, dependencies=[Depends(get_jwt_user_active)])
def generate_password():
    return service.generate_password()
