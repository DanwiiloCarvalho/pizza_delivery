from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from core.settings import settings
from contextvars import ContextVar

async_engine: AsyncEngine = create_async_engine(settings.DATABASE_URL)

Session = async_sessionmaker[AsyncSession](
    bind=async_engine, expire_on_commit=False)

session_context: ContextVar[AsyncSession] = ContextVar('session_context')
