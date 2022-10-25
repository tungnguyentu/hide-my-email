from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session

from .constants import ErrorCode
from .schemas import AccountRegister
from .models import Account
from .security import hash_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get(db: Session, user_id: UUID4):
    return db.query(Account).filter(Account.id == user_id).first()


def get_by_email(db: Session, email: EmailStr):
    return db.query(Account).filter(Account.email == email).first()


def create(*, db: Session, user_in: AccountRegister) -> Account:
    user = get_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    plain_password = user_in.password.get_secret_value()
    hashed_password = hash_password(plain_password)
    user = Account(**user_in.dict(exclude={"password"}), password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
