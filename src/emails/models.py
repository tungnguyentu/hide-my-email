import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from src.database import Base
from src.models import TimeStampMixin


class VirtualDomain(Base, TimeStampMixin):
    __tablename__ = 'virtual_domains'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
