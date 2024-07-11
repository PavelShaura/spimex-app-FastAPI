from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.database import get_async_session
from app.config import settings
from app.database import metadata
from app.tests.fixtures import *


DATABASE_URL_TEST = settings.test_database_url

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool, future=True)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)
