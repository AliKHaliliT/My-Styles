import re
from datetime import UTC, datetime

import pytest
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app import models
from app.api.v1.schemas.common.mixins import TimeStampMixin
from db.base import Base

MOMENT = datetime(2026, 11, 22, 1, 57, 35, tzinfo=UTC)
SENT = re.compile(r'\{"created_at":"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ","updated_at":"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ"\}')


# A stamp the database wrote crossed the wire as 2026-11-22T01:57:35, with nothing to say which
# zone it stood in, and a browser read it as its own local time. The stamp is written and read back
# through the database the settings name, with the driver the seat installs.
async def test_a_stamp_the_database_wrote_crosses_the_wire_with_its_offset() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    async with sessions() as session:
        session.add(models.User(username="stamped"))
        await session.commit()
    async with sessions() as session:
        user = (await session.execute(select(models.User))).scalar_one()
    await engine.dispose()

    sent = TimeStampMixin(created_at=user.created_at, updated_at=user.updated_at).model_dump_json()

    assert SENT.fullmatch(sent), sent


# Each field is sent without its offset in a case of its own, so a field left to take a naive stamp fails its case.
@pytest.mark.parametrize("field", ["created_at", "updated_at"])
def test_a_stamp_without_an_offset_is_refused_before_it_reaches_the_wire(field: str) -> None:
    stamps = {"created_at": MOMENT, "updated_at": MOMENT} | {field: MOMENT.replace(tzinfo=None)}

    with pytest.raises(ValidationError, match="timezone"):
        TimeStampMixin.model_validate(stamps)
