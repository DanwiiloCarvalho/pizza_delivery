from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from contextvars import ContextVar, Token
from contextlib import asynccontextmanager

from core.settings import settings as stt
from core.deps import get_session
from main import app
import pytest

TEST_SQLALCHEMY_DATABASE_URL = stt.TEST_SQLALCHEMY_DATABASE_URL

test_session_context: ContextVar[AsyncSession] = ContextVar(
    'test_session_context')


@pytest.fixture(scope='session', autouse=True)
async def create_tables():
    test_async_engine = create_async_engine(url=TEST_SQLALCHEMY_DATABASE_URL)
    async with test_async_engine.begin() as conn:
        await conn.run_sync(stt.DBBaseModel.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(stt.DBBaseModel.metadata.drop_all)
    await test_async_engine.dispose()


@asynccontextmanager
async def db_session_context():
    test_async_engine = create_async_engine(url=TEST_SQLALCHEMY_DATABASE_URL)
    Session = async_sessionmaker(
        bind=test_async_engine, expire_on_commit=False)

    async with test_async_engine.connect() as conn:
        transaction = await conn.begin()

        async with Session(bind=conn) as session:
            token: Token[AsyncSession] = test_session_context.set(session)
            yield session
            test_session_context.reset(token)
        await transaction.rollback()


@pytest.fixture
async def db_session():
    async with db_session_context() as session:
        yield session


@asynccontextmanager
async def client_context(db_session):
    app.dependency_overrides[get_session] = lambda: db_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
async def client(db_session):
    async with client_context(db_session) as c:
        yield c
