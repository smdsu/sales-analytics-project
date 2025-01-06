from fastapi import Request, Depends

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from pydantic import EmailStr

from app.config import get_auth_data
from app.exceptions import (
    TokenExpiredException,
    TokenNotFoundException,
    NoUserIdException,
    NoUserException,
    NoJwtException,
)

from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(
        to_encode,
        auth_data['secret_key'],
        algorithm=auth_data['algorithm']
    )
    return encode_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none_by_filter(email=email)
    if not user or verify_password(
        plain_password=password,
        hashed_password=user.password
    ) is False:
        return None
    return user


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNotFoundException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            token,
            auth_data['secret_key'],
            algorithms=auth_data['algorithm']
        )
    except JWTError:
        raise NoJwtException

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id = payload.get("sub")
    if not user_id:
        raise NoUserIdException

    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise NoUserException

    return user
