from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
from typing import AsyncGenerator
from core.database import Session
from core.database import session_context
from core.authentication import verify_token
from core.settings import settings as stt
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from contextvars import Token
from fastapi.exceptions import HTTPException
from schemas.token_schema import TokenDataSchema
from models.user import User


async def get_session() -> AsyncGenerator:
    async with Session() as session:
        token: Token[AsyncSession] = session_context.set(session)
        try:
            yield session
        finally:
            session_context.reset(token)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{stt.API_PREFIX}/auth/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_session)) -> User | None:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não é possível validar as crendenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload: dict[str, any] = verify_token(token=token)

    user_id = payload.get('sub')

    if not user_id:
        raise credentials_exception

    token_data = TokenDataSchema(user_id=user_id)

    query = select(User).filter(User.id == token_data.user_id)
    user = (await db.execute(query)).unique().scalar_one_or_none()
    if not user:
        raise credentials_exception
    return user
