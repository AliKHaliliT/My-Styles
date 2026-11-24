from datetime import UTC, datetime, timedelta, timezone
from typing import cast

import pytest
from alembic.autogenerate.api import AutogenContext
from sqlalchemy import DateTime
from sqlalchemy.dialects import sqlite
from sqlalchemy.engine import make_url

from db.types import UTCDateTime, render_stored_type

DIALECT = sqlite.dialect()
# A database that keeps the offset, which SQLite does not, so the column's asking for the time zone shows in its type.
KEEPS_OFFSETS = make_url("postgresql://").get_dialect()()
# One moment in UTC, and the same moment as a clock seven hours behind it reads it.
MOMENT = datetime(2026, 11, 22, 1, 57, 35, tzinfo=UTC)
BEHIND = MOMENT.astimezone(timezone(timedelta(hours=-7)))


# SQLite keeps no offset, so a moment it wrote in UTC came back naive, and a reader that took it for
# its own local time was off by its whole offset.
def test_a_moment_read_without_an_offset_is_handed_back_in_utc() -> None:
    read = UTCDateTime().process_result_value(MOMENT.replace(tzinfo=None), DIALECT)

    assert read == MOMENT
    assert read is not None and read.utcoffset() == timedelta(0)


def test_a_moment_read_with_an_offset_is_handed_back_in_utc_at_the_same_instant() -> None:
    read = UTCDateTime().process_result_value(BEHIND, DIALECT)

    assert read == MOMENT
    assert read is not None and read.utcoffset() == timedelta(0)


def test_a_moment_bound_without_an_offset_is_refused() -> None:
    with pytest.raises(ValueError, match="must carry an offset"):
        UTCDateTime().process_bind_param(MOMENT.replace(tzinfo=None), DIALECT)


def test_a_moment_bound_with_an_offset_is_stored_in_utc_at_the_same_instant() -> None:
    bound = UTCDateTime().process_bind_param(BEHIND, DIALECT)

    assert bound == MOMENT
    assert bound is not None and bound.utcoffset() == timedelta(0)


# SQLite stores the same text whether the column asks for the time zone or not, while a database that keeps the offset
# drops it from a column that does not ask, so the moment would come back from it without one.
def test_the_column_asks_a_database_that_keeps_offsets_for_one() -> None:
    assert UTCDateTime().compile(dialect=KEEPS_OFFSETS) == "TIMESTAMP WITH TIME ZONE"


def test_no_moment_stays_none_both_ways() -> None:
    assert UTCDateTime().process_bind_param(None, DIALECT) is None
    assert UTCDateTime().process_result_value(None, DIALECT) is None


# A revision generated from the models named db.types.UTCDateTime without importing it, so it failed
# when applied; it names the type the database stores instead, and leaves every other item to Alembic.
def test_a_generated_revision_names_the_stored_type_and_never_the_application_s() -> None:
    context = cast(AutogenContext, None)

    assert render_stored_type("type", UTCDateTime(), context) == "sa.DateTime(timezone=True)"
    assert render_stored_type("type", DateTime(timezone=True), context) is False
    assert render_stored_type("column", UTCDateTime(), context) is False
