import warnings
from types import SimpleNamespace
from typing import ClassVar

import pytest
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from app.utils.reorder_fields import reorder_fields

# The decorator reorders the class it is handed and rebuilds that class's schema, so every case
# reads the field order, the defaults and the behavior of the very class its statement made.


class StampMixin(BaseModel):
    updated_at: int
    created_at: int


class Identified(BaseModel):
    id: int
    labels: list[str] = Field(default_factory=list, description="free-form labels")


class Named(BaseModel):
    name: str

    def label(self) -> str:
        return f"named {self.name}"

    @field_validator("name")
    @classmethod
    def refuse_a_blank_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("a blank name is refused")
        return value


@reorder_fields(StampMixin)
class Sized(Named, StampMixin):
    size: int
    kind: ClassVar[str] = "sized"
    model_config = ConfigDict(from_attributes=True)

    @field_validator("size")
    @classmethod
    def refuse_a_negative_size(cls, value: int) -> int:
        if value < 0:
            raise ValueError("a negative size is refused")
        return value


@reorder_fields(StampMixin)
class Early(Identified, StampMixin):
    later: Later | None = None


class Later(BaseModel):
    note: str


def field_names(model: type[BaseModel]) -> list[str]:
    return list(model.model_fields)


def sized(**overrides: object) -> dict[str, object]:
    return {"name": "a", "size": 1, "created_at": 2, "updated_at": 3} | overrides


def test_inherited_fields_lead_own_fields_follow_and_the_last_classes_close_the_order() -> None:
    @reorder_fields(StampMixin)
    class Thing(Identified, StampMixin):
        name: str = "unnamed"

    assert field_names(Thing) == ["id", "labels", "name", "created_at", "updated_at"]
    assert Thing.__name__ == "Thing"


def test_defaults_and_factories_survive_the_rebuild_wherever_the_field_came_from() -> None:
    @reorder_fields(StampMixin)
    class Thing(Identified, StampMixin):
        name: str = "unnamed"
        count: int

    thing = Thing(id=1, count=2, created_at=3, updated_at=4)

    assert thing.name == "unnamed"
    assert thing.labels == []
    assert Thing.model_fields["labels"].description == "free-form labels"
    assert Thing.model_fields["count"].is_required()


def test_moved_fields_without_an_interleave_order_fall_alphabetically() -> None:
    @reorder_fields(StampMixin)
    class Thing(Identified, StampMixin):
        name: str

    assert field_names(Thing)[-2:] == ["created_at", "updated_at"]


def test_interleave_last_fixes_the_order_of_the_moved_fields() -> None:
    @reorder_fields(StampMixin, interleave_last=["updated_at", "created_at"])
    class Thing(Identified, StampMixin):
        name: str

    assert field_names(Thing) == ["id", "labels", "name", "updated_at", "created_at"]


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

    assert field_names(Thing) == ["id", "labels", "name", "created_at"]


def test_the_last_classes_may_be_named_as_strings() -> None:
    @reorder_fields("StampMixin", interleave_last=["created_at", "updated_at"])
    class Thing(Identified, StampMixin):
        name: str

    assert field_names(Thing) == ["id", "labels", "name", "created_at", "updated_at"]


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

    assert field_names(Thing) == ["id", "labels", "name", "created_at"]


def test_the_class_keeps_every_base_its_statement_names() -> None:
    model = Sized.model_validate(sized())

    assert isinstance(model, Named)
    assert isinstance(model, StampMixin)


def test_the_class_keeps_the_methods_it_inherits() -> None:
    assert Sized.model_validate(sized()).label() == "named a"


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [("name", " ", "a blank name is refused"), ("size", -1, "a negative size is refused")],
)
def test_the_validators_it_inherits_and_declares_still_refuse(field: str, value: object, reason: str) -> None:
    with pytest.raises(ValidationError, match=reason):
        Sized.model_validate(sized(**{field: value}))


def test_the_configuration_built_into_its_schema_applies() -> None:
    row = SimpleNamespace(**sized())

    assert Sized.model_validate(row).size == 1


def test_the_order_holds_where_the_model_is_written_and_described() -> None:
    expected = ["name", "size", "created_at", "updated_at"]

    assert list(Sized.model_validate(sized()).model_dump()) == expected
    assert list(Sized.model_json_schema()["properties"]) == expected


def test_a_class_variable_stays_a_class_variable() -> None:
    assert Sized.kind == "sized"
    assert "kind" not in Sized.model_fields


def test_a_forward_reference_resolves_once_its_class_exists() -> None:
    early = Early.model_validate({"id": 1, "later": {"note": "n"}, "created_at": 2, "updated_at": 3})

    assert early.later is not None
    assert early.later.note == "n"
    assert field_names(Early) == ["id", "labels", "later", "created_at", "updated_at"]


def test_a_class_that_is_no_pydantic_model_is_refused() -> None:
    with pytest.raises(TypeError, match="decorates a pydantic model"):
        @reorder_fields(StampMixin)
        class Plain:
            name: str
