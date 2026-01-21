import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from contextvars import ContextVar, Token

from main import app
from core.settings import settings as stt
from core.deps import get_session


TEST_SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'

test_session_context: ContextVar[AsyncSession] = ContextVar(
    'test_session_context')


@pytest.fixture
async def db_session():
    test_async_engine = create_async_engine(url=TEST_SQLALCHEMY_DATABASE_URL)
    Session = async_sessionmaker(
        bind=test_async_engine, expire_on_commit=False)

    async with test_async_engine.begin() as conn:
        await conn.run_sync(stt.DBBaseModel.metadata.create_all)

    async with Session() as session:
        token: Token[AsyncSession] = test_session_context.set(session)
        yield session
        test_session_context.reset(token)

    await test_async_engine.dispose()


@pytest.fixture
async def client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
