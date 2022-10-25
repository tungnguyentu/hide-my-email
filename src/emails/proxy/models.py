import uuid
from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from src.database import Base
from src.models import TimeStampMixin


class VirtualUser(Base, TimeStampMixin):
    __tablename__ = 'virtual_users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    domain_id = Column(ForeignKey('virtual_domains.id', ondelete='CASCADE'), nullable=False, index=True)
    account_id = Column(ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False, index=True)
    email = Column(String(120), nullable=False)
    password = Column(String(106), nullable=False)
    used = Column(Boolean, default=False)

    domain = relationship('VirtualDomain')
    account = relationship('Account')