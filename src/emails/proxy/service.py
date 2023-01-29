import random
import string
from random import choice
from typing import List, Optional

from pydantic import EmailStr

from src.config import Settings as settings
from src.emails.models import VirtualDomain
from src.emails.proxy.models import VirtualUser
from src.emails.proxy.schemas import ProxiesGenerated, ProxyCreate, ProxyGet, PasswordGenerated


def choice_random_email(db, account_id) -> Optional[ProxiesGenerated]:
    proxies = db.query(VirtualUser).filter(VirtualUser.account_id==account_id, VirtualUser.used==False).all()
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

n = -1
def round_rob_seq(seq):
  global n
  n = n + 1
  return seq[n % len(seq)]
        
    
def random_proxy(proxies, domain, account_id, db):
    random_list = []
    if len(proxies) < settings.LIMIT_PROXIES:
        new_proxy = generate_email(db, domain, account_id)
        random_list.append(new_proxy)
    for proxy in proxies:
        random_list.append(proxy.email)
    proxy = round_rob_seq(random_list)
    return proxy


def generate_email(db, domain, account_id):
    username = "_".join(choice(settings.RANDOM_WORDS) for _ in range(2)).lower()
    email_address = f"{username}@{domain.name}"
    proxy = VirtualUser(
        domain_id=domain.id,
        email=email_address,
        account_id=account_id,
        password=settings.DEFAULT_RANDOM_EMAIL_PASS
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


def generate_password():
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=14))
    return PasswordGenerated(password=password)
