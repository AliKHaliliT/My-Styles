from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.domain.schemas.common.mixins import TimeStampMixin

MOMENT = datetime(2026, 11, 22, 1, 57, 35, tzinfo=UTC)


# A naive moment in the domain is compared and formatted as if it stood in the machine's own zone,
# so the domain refuses one as it is built, each field in a case of its own.
@pytest.mark.parametrize("field", ["created_at", "updated_at"])
def test_a_stamp_without_an_offset_is_refused_as_the_domain_builds_it(field: str) -> None:
    stamps = {"created_at": MOMENT, "updated_at": MOMENT} | {field: MOMENT.replace(tzinfo=None)}

    with pytest.raises(ValidationError, match="timezone"):
        TimeStampMixin.model_validate(stamps)
