import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.database import Base
from src.models import TimeStampMixin, ActivatedMixin


class VirtualAliases(Base, TimeStampMixin, ActivatedMixin):
    __tablename__ = 'virtual_aliases'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    domain_id = Column(ForeignKey('virtual_domains.id', ondelete='CASCADE'), nullable=False, index=True)
    source = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    account_id = Column(ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False, index=True)
    label = Column(String(200), nullable=False)
    note = Column(String(1000), nullable=False)
    domain = relationship('VirtualDomain')
    account = relationship('Account')
