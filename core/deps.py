from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from core.database import Session
from core.database import session_context
from contextvars import Token

async def get_session() -> AsyncGenerator:
    async with Session() as session:
        token: Token[AsyncSession] = session_context.set(session)
        try:
            yield session
        finally:
            session_context.reset(token)