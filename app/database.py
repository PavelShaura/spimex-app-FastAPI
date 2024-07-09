from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base

from app.config import settings

database_url = settings.database_url
database_params = {}

metadata = MetaData()

engine = create_async_engine(database_url, **database_params, pool_pre_ping=True)

async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


Base = declarative_base(metadata=metadata)
