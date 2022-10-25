from typing import Optional, List
from fastapi.encoders import jsonable_encoder
from src.auth.models import Account
from src.emails.forwards.models import VirtualAliases
from src.emails.models import VirtualDomain
from src.emails.forwards.schemas import ForwardCreate, ForwardGet, ForwardUpdate
from src.emails.proxy.models import VirtualUser


def create(db, forward_in: ForwardCreate, account_id: str) -> Optional[VirtualAliases]:
    domain = db.query(VirtualDomain).first()
    proxy = db.query(VirtualUser).filter(
        VirtualUser.account_id==account_id,
        VirtualUser.email==forward_in.source
    ).first()
    setattr(proxy, "used", True)
    forward = VirtualAliases(
        domain_id=domain.id,
        account_id=account_id,
        source=forward_in.source,
        destination=forward_in.destination,
        label=forward_in.label,
        note=forward_in.note
    )
    db.add(proxy)
    db.add(forward)
    db.commit()
    return forward


def get_forwards(db, account_id: str) -> Optional[List[VirtualAliases]]:
    forwards = db.query(VirtualAliases).filter(
        VirtualAliases.account_id==account_id
    ).all()
    return forwards


def get_by_id(db, forward_id: str, account: Account) -> Optional[VirtualAliases]:
    forward = db.query(VirtualAliases).filter(
        VirtualAliases.id==forward_id,
        VirtualAliases.account_id==account.id
    ).first()
    return forward

def get_by_source_n_destination(db, forward_in, account_id):
    forward = db.query(VirtualAliases).filter(
        VirtualAliases.account_id == account_id,
        VirtualAliases.source == forward_in.source,
        VirtualAliases.destination == forward_in.destination
    ).first()
    return forward

def update(db, alias: VirtualAliases, alias_in: ForwardUpdate) -> Optional[VirtualAliases]:
    forward_data = jsonable_encoder(alias)
    update_data = alias_in.dict(exclude_unset=True)
    for field in forward_data:
        if field in update_data:
            setattr(alias, field, update_data[field])

    db.add(alias)
    db.commit()
    return alias


def deactivate(db, forward: VirtualAliases) -> Optional[VirtualAliases]:
    forward.is_active = False
    db.add(forward)
    db.commit()
    return forward


def activate(db, forward: VirtualAliases) -> Optional[VirtualAliases]:
    forward.is_active = True
    db.add(forward)
    db.commit()
    return forward

def delete(db, forward: VirtualAliases):
    db.delete(forward)
    db.commit()