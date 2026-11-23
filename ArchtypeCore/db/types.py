from datetime import UTC, datetime
from typing import TYPE_CHECKING, Literal

from sqlalchemy import DateTime
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator

if TYPE_CHECKING:
    from alembic.autogenerate.api import AutogenContext


class UTCDateTime(TypeDecorator[datetime]):

    """

    A timestamp column that hands a moment back aware and in UTC.

    The column stores a timezone-aware DateTime. SQLite keeps no offset and writes its clock in UTC,
    so a moment it hands back without one is read as UTC, and a database that keeps the offset hands
    back an aware moment, which is turned to UTC. A database that keeps no offset and writes its own
    local time is not one this type can read. A moment bound from Python must carry its offset, and
    is stored in UTC.


    Usage
    -----
    Declare a timestamp column with this type in place of a bare DateTime.
    ```python
    from datetime import datetime

    from sqlalchemy import func
    from sqlalchemy.orm import Mapped, mapped_column

    from db.types import UTCDateTime

    created_at: Mapped[datetime] = mapped_column(UTCDateTime, nullable=False, server_default=func.now())
    ```

    """

    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(self, value: datetime | None, dialect: Dialect) -> datetime | None:

        """

        Turns a moment bound from Python into the UTC the column stores.


        Parameters
        ----------
        value : datetime | None
            The moment to store, or None.

        dialect : Dialect
            The dialect of the database in use.


        Returns
        -------
        datetime | None
            The same moment in UTC, or None.


        Raises
        ------
        ValueError
            If `value` carries no offset.

        """

        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError(f"value must carry an offset. Received: {value} with type {type(value)}")


        return value.astimezone(UTC)


    def process_result_value(self, value: datetime | None, dialect: Dialect) -> datetime | None:

        """

        Turns a moment read from the database into an aware one in UTC.


        Parameters
        ----------
        value : datetime | None
            The moment the database handed back, or None.

        dialect : Dialect
            The dialect of the database in use.


        Returns
        -------
        datetime | None
            The same moment in UTC, with UTC attached where the database kept no offset, or None.


        Raises
        ------
        None.

        """

        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)


        return value.astimezone(UTC)


def render_stored_type(type_: str, obj: object, autogen_context: AutogenContext) -> str | Literal[False]:

    """

    Renders a column type by what the database stores, so a generated revision never imports the application.

    A UTCDateTime column stores a timezone-aware DateTime, and the offset it attaches is the
    application's work on the way out. Left to Alembic, a revision named the application's type
    without importing it and failed when applied. Every other item is rendered as Alembic would.
    The migration environment passes it to Alembic as the item renderer in both of its modes.


    Parameters
    ----------
    type_ : str
        The kind of item being rendered.

    obj : object
        The item itself.

    autogen_context : AutogenContext
        The context Alembic renders in.


    Returns
    -------
    str | Literal[False]
        The stored type's source for a UTCDateTime column, or False to leave the item to Alembic.


    Raises
    ------
    None.

    """

    if type_ == "type" and isinstance(obj, UTCDateTime):
        return "sa.DateTime(timezone=True)"


    return False
