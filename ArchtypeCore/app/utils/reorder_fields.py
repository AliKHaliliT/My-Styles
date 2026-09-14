from collections.abc import Callable
from functools import cache
import warnings

from pydantic import BaseModel, create_model


def reorder_fields(
    *last_classes: type | str,
    include_fields: set[str] | None = None,
    exclude_fields: set[str] | None = None,
    fields_to_move_last: dict[type | str, set[str]] | None = None,
    interleave_last: list[str] | None = None,
    debug: bool = False,
    verbose: bool = False
) -> Callable[[type], type]:
    
    """

    A decorator to reorder Pydantic model fields with advanced control.

    This decorator reconstructs a Pydantic model to enforce a specific field
    ordering. It is useful for ensuring a consistent layout, especially in
    complex inheritance scenarios.

    Field ordering logic
    --------------------
    1.  Inherited fields (from bases not specified in `last_classes`).
    2.  The decorated model's own explicitly defined fields.
    3.  Fields from `last_classes`, which are moved to the end. These can
        be further filtered and interleaved.


    Parameters
    ----------
    *last_classes : type | str
        Variable-length argument of class types or their names to be
        moved to the end of the field order.

    include_fields : set[str] | None, optional
        A set of field names to explicitly include. If provided, any
        field not in this set will be dropped. Defaults to `None`.

    exclude_fields : set[str] | None, optional
        A set of field names to explicitly exclude from the final model.
        Defaults to None.

    fields_to_move_last : dict[type | str, set[str]] | None, optional
        A dictionary mapping a class (or its name) from `last_classes`
        to a set of its fields that should be moved. If a class from
        `last_classes` is not in this dict, all its fields are moved.
        Defaults to `None`.

    interleave_last : list[str] | None, optional
        An ordered list of field names from `last_classes` to specify
        their exact order at the end. Any fields from `last_classes` not
        in this list will be appended alphabetically after the interleaved
        ones. Defaults to `None`.

    debug : bool, optional
        If True, prints detailed step-by-step information about the
        reordering process. Defaults to `False`.

    verbose : bool, optional
        If True, prints information about why individual fields are
        skipped. Requires `debug=True` to be effective. Defaults to `False`.


    Returns
    -------
    Callable[[type], type]
        A decorator that returns a new Pydantic model class with
        reordered fields.


    Raises
    ------
    TypeError
        If `include_fields` is not an instance of set, or `exclude_fields` is not an instance of set, or `fields_to_move_last` is not an instance of dict, or `interleave_last` is not an instance of list.

    """
    
    _check_options(include_fields, exclude_fields, fields_to_move_last, interleave_last)


    last_class_names_ordered = [
        cls.__name__ if isinstance(cls, type) else cls for cls in last_classes
    ]
    last_class_names_set = set(last_class_names_ordered)

    fields_to_move_last_norm = {}
    if fields_to_move_last:
        for k, v in fields_to_move_last.items():
            key_name = k.__name__ if isinstance(k, type) else k
            fields_to_move_last_norm[key_name] = v


    def _decorator(cls: type) -> type:

        """
        
        Applies the field reordering logic to the decorated class.
        
        """

        _check_mro(cls, last_class_names_set)
        order = _FieldOrder(include_fields, exclude_fields, verbose)
        _add_inherited_fields(cls, last_class_names_set, order, debug)
        _add_own_fields(cls, order, debug)
        last_fields_collected = _collect_last_fields(cls, last_class_names_ordered, fields_to_move_last_norm, order, debug)
        _add_last_fields(last_fields_collected, interleave_last, order, debug)


        return _build_model(cls, order.fields, debug)
    

    return _decorator


def _check_options(
    include_fields: set[str] | None,
    exclude_fields: set[str] | None,
    fields_to_move_last: dict[type | str, set[str]] | None,
    interleave_last: list[str] | None,
) -> None:

    """
    
    Refuse an option whose shape is not the one the decorator reads.
    
    """

    if include_fields and not isinstance(include_fields, set):
        raise TypeError(f"include_fields must be an instance of set. Received: {include_fields} with type {type(include_fields)}")
    if exclude_fields and not isinstance(exclude_fields, set):
        raise TypeError(f"exclude_fields must be an instance of set. Received: {exclude_fields} with type {type(exclude_fields)}")
    if fields_to_move_last and not isinstance(fields_to_move_last, dict):
        raise TypeError(f"fields_to_move_last must be an instance of dict. Received: {fields_to_move_last} with type {type(fields_to_move_last)}")
    if interleave_last and not isinstance(interleave_last, list):
        raise TypeError(f"interleave_last must be an instance of list. Received: {interleave_last} with type {type(interleave_last)}")


def _check_mro(cls: type, last_class_names_set: set[str]) -> None:

    """
    
    Ensure every class named in last_classes is a base of the decorated class.
    
    """

    mro_names = {base.__name__ for base in cls.__mro__}
    missing = last_class_names_set - mro_names
    if missing:
        raise TypeError(
            f"The following classes specified in @reorder_fields are not in the MRO of {cls.__name__}: {missing}"
        )


@cache
def _collect_fields_recursively(base_cls: type) -> dict[str, tuple[type, object]]:

    """
    
    Collect all fields from a class and its bases.
    
    """

    collected = {}
    for base in reversed(base_cls.__mro__):
        if base in (BaseModel, object):
            continue
        if hasattr(base, "model_fields"):
            for fname, field in base.model_fields.items():
                collected[fname] = (field.annotation, getattr(field, "default", ...))


    return collected


class _FieldOrder:

    """
    
    The fields gathered so far, in order, behind the include and exclude filter.
    
    """

    def __init__(self, include_fields: set[str] | None, exclude_fields: set[str] | None, verbose: bool) -> None:
        self.include_fields_set = include_fields.copy() if include_fields else None
        self.exclude_fields_set = exclude_fields.copy() if exclude_fields else None
        self.verbose = verbose
        self.seen: set[str] = set()
        self.fields: list[tuple[str, tuple[object, object]]] = []

    def allowed(self, fname: str) -> bool:

        """
        
        Check if a field should be included based on include/exclude sets.
        
        """

        if self.include_fields_set and fname not in self.include_fields_set:
            if self.verbose: print(f"Skipping field '{fname}' (not in include_fields)")
            return False
        if self.exclude_fields_set and fname in self.exclude_fields_set:
            if self.verbose: print(f"Skipping field '{fname}' (in exclude_fields)")
            return False
        return True

    def add(self, fname: str, annotation: object, default: object) -> None:

        """
        
        Add a field to the ordered list if not already seen.
        
        """

        if fname not in self.seen:
            self.fields.append((fname, (annotation, default)))
            self.seen.add(fname)


def _add_inherited_fields(cls: type, last_class_names_set: set[str], order: _FieldOrder, debug: bool) -> None:

    """
    
    Add the fields of every base that is not one of the last classes.
    
    """

    if debug: print(f"\n[{cls.__name__}] Adding inherited fields (excluding last_classes)...")
    for base in cls.__mro__[1:]:
        if base in (BaseModel, object) or base.__name__ in last_class_names_set:
            continue
        if hasattr(base, "model_fields"):
            for fname, field in base.model_fields.items():
                if order.allowed(fname):
                    order.add(fname, field.annotation, getattr(field, "default", ...))
                elif order.verbose:
                    print(f"Skipping field '{fname}' (not allowed)")


def _add_own_fields(cls: type, order: _FieldOrder, debug: bool) -> None:

    """
    
    Add the fields the decorated class declares itself.
    
    """

    if debug: print(f"\n[{cls.__name__}] Adding own fields...")
    for fname, annotation in getattr(cls, "__annotations__", {}).items():
        if order.allowed(fname):
            order.add(fname, annotation, getattr(cls, fname, ...))
        elif order.verbose:
            print(f"Skipping field '{fname}' (not allowed)")


def _collect_last_fields(
    cls: type,
    last_class_names_ordered: list[str],
    fields_to_move_last_norm: dict[str, set[str]],
    order: _FieldOrder,
    debug: bool,
) -> dict[str, tuple[type, object]]:

    """
    
    Gather the fields of the last classes that are to move to the end.
    
    """

    if debug: print(f"\n[{cls.__name__}] Adding last-class fields...")
    last_fields_collected: dict[str, tuple[type, object]] = {}
    for class_name in last_class_names_ordered:
        base = next(b for b in cls.__mro__ if b.__name__ == class_name)
        all_fields = _collect_fields_recursively(base)
        move_fields: set[str] = fields_to_move_last_norm.get(class_name, set(all_fields.keys()))

        invalid_fields = move_fields - set(all_fields.keys())
        if invalid_fields:
            warnings.warn(f"fields_to_move_last for class {class_name} contains invalid fields: {invalid_fields}", stacklevel=3)

        for fname in move_fields & set(all_fields.keys()):
            if order.allowed(fname):
                last_fields_collected[fname] = all_fields[fname]


    return last_fields_collected


def _add_last_fields(
    last_fields_collected: dict[str, tuple[type, object]],
    interleave_last: list[str] | None,
    order: _FieldOrder,
    debug: bool,
) -> None:

    """
    
    Append the moved fields, the interleaved ones first in their given order.
    
    """

    if interleave_last:
        if debug: print(f"  Interleaving last fields in order: {interleave_last}")
        for fname in interleave_last:
            if fname in last_fields_collected and fname not in order.seen:
                order.add(fname, *last_fields_collected.pop(fname))
    for fname, val in last_fields_collected.items():
        if fname not in order.seen:
            order.add(fname, *val)


def _build_model(cls: type, ordered_fields: list[tuple[str, tuple[object, object]]], debug: bool) -> type:

    """
    
    Build the new model from the ordered fields, preserving config and validators.
    
    """

    new_model_name = cls.__name__
    new_model_bases = (BaseModel,)
    new_model_dict = dict(ordered_fields)
    new_model = create_model(  # type: ignore[call-overload]  # create_model takes fields as keywords, not a mapping
        new_model_name,
        **new_model_dict,
        __base__=new_model_bases[0]
    )

    for attr in ("model_config",):
        if hasattr(cls, attr):
            setattr(new_model, attr, getattr(cls, attr))

    if hasattr(cls, "__dict__"):
        for name, value in cls.__dict__.items():
            if hasattr(value, "_attributes") and "validator" in value._attributes:
                setattr(new_model, name, value)


    if debug:
        print(f"\n[{cls.__name__}] Final field order: {[f[0] for f in ordered_fields]}")


    return new_model
