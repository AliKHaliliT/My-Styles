from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.core.config.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
