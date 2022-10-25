from src.models import OrmBaseModel
from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional


class AccountBase(OrmBaseModel):
    email: Optional[EmailStr] = None


class AccountRegister(AccountBase):
    email: EmailStr
    password: SecretStr


class AccountLogin(AccountBase):
    email: EmailStr
    password: str


class AccountUpdate(AccountBase):
    password: Optional[SecretStr] = None


# Base Properties for models stored in DB
class AccountInDBBase(AccountBase):
    id: str
    email: EmailStr


# Returned to Client
class AccountResponse(AccountInDBBase):
    pass


# Stored in DB
class AccountInDB(AccountInDBBase):
    password: SecretStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr
