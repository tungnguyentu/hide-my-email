from datetime import datetime
from typing import Optional
from pydantic import EmailStr
from src.models import OrmBaseModel


class ForwardCreate(OrmBaseModel):
    source: EmailStr
    destination: EmailStr
    password: Optional[str] = None
    label: str
    note: Optional[str] = None


class ForwardGet(OrmBaseModel):
    account_id: str


class ForwardUpdate(OrmBaseModel):
    password: Optional[str]
    label: Optional[str]
    note: Optional[str]


class ForwardsResponse(OrmBaseModel):
    id: str
    source: EmailStr
    label: str
    is_active: bool
    destination: str
    password: str


class ForwardResponse(OrmBaseModel):
    id: str
    source: EmailStr
    password: str
    destination: EmailStr
    label: str
    note: str
    created_at: datetime
    is_active: bool