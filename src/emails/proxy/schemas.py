from datetime import datetime
from pydantic import EmailStr
from src.models import OrmBaseModel


class ProxyBase(OrmBaseModel):
    domain_id: str


class ProxyCreate(OrmBaseModel):
    account_id: str


class ProxyGet(OrmBaseModel):
    account_id: str
    email: EmailStr


class ProxiesGenerated(OrmBaseModel):
    email: EmailStr

class PasswordGenerated(OrmBaseModel):
    password: str


class ProxyInDBBase(ProxyBase):
    id: str
    email: EmailStr
    password: str
    domain_id: str


class ProxyResponse(OrmBaseModel):
    email: EmailStr
    created_at: datetime
