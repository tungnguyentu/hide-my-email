import uuid
from sqlalchemy import Column, String
from src.database import Base
from src.models import ActivatedMixin, TimeStampMixin


class Account(Base, TimeStampMixin, ActivatedMixin):
    __tablename__ = 'accounts'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(120), nullable=False)
    password = Column(String(106), nullable=False)


