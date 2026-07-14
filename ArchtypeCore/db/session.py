from typing import AsyncGenerator

from app.core.config.settings import settings
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
