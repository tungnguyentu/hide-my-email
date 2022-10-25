from datetime import datetime, timedelta
from fastapi.security import HTTPBearer
from jose import jwt
from passlib.context import CryptContext

from src.config import Settings as settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

def create_access_token(data: dict, expires_delta: timedelta = None):
    expires_delta = expires_delta or timedelta(minutes=settings.JWT_EXP)
    expire = datetime.utcnow() + expires_delta

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password):
    return pwd_context.hash(plain_password)
