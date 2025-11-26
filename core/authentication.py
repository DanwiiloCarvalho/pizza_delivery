from datetime import timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from zoneinfo import ZoneInfo
from core.settings import settings as stt
from core.security import verify_password
from fastapi import status
from fastapi.exceptions import HTTPException
import jwt


def create_access_token(data: dict[str, any], expires_delta: timedelta | None = None) -> str:
    data_to_encode = data.copy()
    now: datetime = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=15)

    data_to_encode.update({"exp": expire})
    enconded_jwt: str = jwt.encode(payload=data_to_encode,
                                   key=stt.SECRET_KEY, algorithm=stt.ALGORITHM)

    return enconded_jwt


async def authenticate_user(db: AsyncSession, username: str, password: str) -> User:
    query = select(User).filter(User.email == username)
    user_found = (await db.execute(query)).unique().scalar_one_or_none()

    if not user_found or not verify_password(password, user_found.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='E-mail ou senha inválidos.')
    return user_found
