from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from src.config import Config

engine = create_async_engine(
    Config.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_async_session() :
    async with AsyncSessionLocal() as session:
        yield session


async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
)