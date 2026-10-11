from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from production_agent_runtime_api.core.config import settings


engine = create_async_engine(
    url=settings.DATABASE_URL
)



session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass



async def get_db():
    async with session_factory() as session:
        yield session