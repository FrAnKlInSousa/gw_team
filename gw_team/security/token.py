from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi.security import OAuth2PasswordBearer
from jwt import encode
from pwdlib import PasswordHash

from gw_team.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
settings = Settings()


def hash_password(password: str):
    return pwd_context.hash(password)


def is_valid_password(password: str, hashed_password: str):
    return pwd_context.verify(password=password, hash=hashed_password)


def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt
