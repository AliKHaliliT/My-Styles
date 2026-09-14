import warnings

import pytest
from pydantic import BaseModel

from app.utils.reorder_fields import reorder_fields

# The decorator rebuilds a model, so every case reads the rebuilt model's field order and
# defaults rather than the class it was handed.


class StampMixin(BaseModel):
    created_at: int
    updated_at: int


class Identified(BaseModel):
    id: int


def field_names(model: type[BaseModel]) -> list[str]:
    return list(model.model_fields)


def test_inherited_fields_lead_own_fields_follow_and_the_last_classes_close_the_order() -> None:
    @reorder_fields(StampMixin)
    class Thing(Identified, StampMixin):
        name: str = "unnamed"

    names = field_names(Thing)

    assert names[:2] == ["id", "name"]
    assert set(names[2:]) == {"created_at", "updated_at"}
    assert Thing.__name__ == "Thing"


def test_interleave_last_fixes_the_order_of_the_moved_fields() -> None:
    @reorder_fields(StampMixin, interleave_last=["updated_at", "created_at"])
    class Thing(Identified, StampMixin):
        name: str

    assert field_names(Thing) == ["id", "name", "updated_at", "created_at"]


def test_include_and_exclude_sets_filter_every_source_of_fields() -> None:
    @reorder_fields(StampMixin, include_fields={"id", "name", "created_at"}, exclude_fields={"name"})
    class Thing(Identified, StampMixin):
        name: str

    assert field_names(Thing) == ["id", "created_at"]


def test_fields_to_move_last_moves_only_the_named_fields_and_warns_about_unknown_ones() -> None:
    with pytest.warns(UserWarning, match="invalid fields"):
        @reorder_fields(StampMixin, fields_to_move_last={StampMixin: {"created_at", "deleted_at"}})
        class Thing(Identified, StampMixin):
            name: str

    assert field_names(Thing) == ["id", "name", "created_at"]


def test_the_last_classes_may_be_named_as_strings() -> None:
    @reorder_fields("StampMixin", interleave_last=["created_at", "updated_at"])
    class Thing(Identified, StampMixin):
        name: str

    assert field_names(Thing) == ["id", "name", "created_at", "updated_at"]


def test_a_last_class_missing_from_the_bases_is_refused() -> None:
    with pytest.raises(TypeError, match="not in the MRO"):
        @reorder_fields(StampMixin)
        class Thing(Identified):
            name: str


def test_an_option_of_the_wrong_shape_is_refused_before_any_class_is_touched() -> None:
    with pytest.raises(TypeError, match="include_fields must be an instance of set"):
        reorder_fields(StampMixin, include_fields=["id"])  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="interleave_last must be an instance of list"):
        reorder_fields(StampMixin, interleave_last={"id"})  # type: ignore[arg-type]


def test_a_clean_call_raises_no_warning() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")

        @reorder_fields(StampMixin, fields_to_move_last={StampMixin: {"created_at"}})
        class Thing(Identified, StampMixin):
            name: str

    assert field_names(Thing) == ["id", "name", "created_at"]
