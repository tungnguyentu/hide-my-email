import string
from random import choice
from typing import List, Optional
from pydantic import EmailStr
from src.emails.proxy.models import VirtualUser
from src.emails.models import VirtualDomain
from src.emails.proxy.schemas import ProxiesGenerated, ProxyGet, ProxyCreate
from src.config import Settings as settings


def choice_random_email(db, account_id) -> Optional[ProxiesGenerated]:
    proxies = db.query(VirtualUser).filter(VirtualUser.account_id==account_id).all()
    domain = db.query(VirtualDomain).first()
    if proxies:
        proxy = random_proxy(proxies, domain, account_id, db)
        return ProxiesGenerated(email=proxy)
    else:
        for _ in range(settings.LIMIT_PROXIES):
            generate_email(db, domain, account_id)
        proxies = db.query(VirtualUser).filter(VirtualUser.account_id==account_id).all()
        proxy = random_proxy(proxies, domain, account_id, db)
        return ProxiesGenerated(email=proxy)
        
    
def random_proxy(proxies, domain, account_id, db):
    random_list = []
    for proxy in proxies:
        if proxy.used:
            new_proxy = generate_email(db, domain, account_id)
            random_list.append(new_proxy)
        random_list.append(proxy.email)
    proxy = choice(random_list)
    return proxy


def generate_email(db, domain, account_id):
    username = "-".join(choice(settings.RANDOM_WORDS) for _ in range(2)).lower()
    email_address = f"{username}@{domain.name}"
    proxy = VirtualUser(
        domain_id=domain.id,
        email=email_address,
        account_id=account_id,
        password="HaNoi2018"
    )
    db.add(proxy)
    db.commit()
    return email_address


def get_users(db, account_id: str) -> Optional[List[VirtualUser]]:
    users = db.query(VirtualUser).filter(
        VirtualUser.account_id==account_id
    ).all()
    return users


def get_proxy(db, account_id: str, email: EmailStr) -> VirtualUser:
    proxy = db.query(VirtualUser).filter(
        VirtualUser.account_id == account_id,
        VirtualUser.email == email
    ).first()
    return proxy