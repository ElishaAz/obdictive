from typing import Union, Callable, overload, Optional

from .default_serializers import _default_serializer, _default_deserializer
from .deserialization import set_deserializer
from .serialization import set_serializer
from . import typevars, aliases


@overload
def serializable(*, serializer: Optional[typevars.Serializer] = None,
                 deserializer: Optional[typevars.Deserializer] = None,
                 deep_search: bool = False) -> Callable[[typevars.Class], typevars.Class]:
    pass


@overload
def serializable(cls: typevars.Class, *, serializer: Optional[typevars.Serializer] = None,
                 deserializer: Optional[typevars.Deserializer] = None,
                 deep_search: bool = False) -> typevars.Class:
    pass


def serializable(cls: Optional[typevars.Class] = None, *,
                 serializer: Optional[aliases.Serializer] = None, deserializer: Optional[aliases.Deserializer] = None,
                 deep_search: bool = False) -> Union[typevars.Class, Callable[[typevars.Class], typevars.Class]]:
    """
    A class decorator that marks it as serializable.

    The serializer and deserializer can be either:
        1. Supplied in the decorator.
        2. Methods in the class marked with @serializer and @deserializer.

    If none of these are defined, they will be created based on the class's annotations, as follows:
        A. If `_annotations: Dict[str, type]` is specified, it will be used in place of the class's annotations.
        B. Any variables specified in `_ignore_annot: Set[str]` will not be included.
        C. Any annotation specified in `_add_annot: Dict[str, type]` will be added to the annotations.
        D. Any annotation specified in `_edit_annot: Dict[str, type]` will replace any existing annotation.

    """

    def decorator(cls: typevars.Class) -> typevars.Class:
        nonlocal serializer, deserializer

        found_serializer = serializer is not None
        found_deserializer = deserializer is not None

        # search for methods marked as serializer or deserializer
        for superclass in (cls.mro() if deep_search else (cls,)):
            for name in superclass.__dict__:  # go over all the methods
                method = getattr(cls, name)
                if hasattr(method, SERIALIZER_MARK) and not found_serializer:  # if it is marked as the serializer
                    serializer = method
                    found_serializer = True
                elif hasattr(method,
                             DESERIALIZER_MARK) and not found_deserializer:  # if it is marked as the deserializer
                    deserializer = method
                    found_deserializer = True
                if found_serializer and found_deserializer:
                    break

        if not found_serializer:
            serializer = _default_serializer

        if not found_deserializer:
            def deserializer(val: dict): _default_deserializer(cls, val)

        assert serializer is not None
        assert deserializer is not None
        set_serializer(cls, serializer)
        set_deserializer(cls, deserializer)

        return cls

    if cls is not None:
        return decorator(cls)
    return decorator


# ------------------------ Serializer ----------------------------------

SERIALIZER_MARK = "is_obdictive_serializer"


def serializer(method: typevars.Serializer) -> typevars.Serializer:
    """
    A method decorator that marks it as the serializer for that class. The class must be decorated with `serializable`.
    """
    setattr(method, SERIALIZER_MARK, True)
    return method


def serializer_for(cls: type) -> Callable[[typevars.Serializer], typevars.Serializer]:
    """
    A function decorator that sets it as the serializer for type `cls`.
    """

    def my_serializer(method: typevars.Serializer) -> typevars.Serializer:
        set_serializer(cls, method)
        return method

    return my_serializer


# ------------------------- Deserializer -----------------------


DESERIALIZER_MARK = "is_obdictive_deserializer"


def deserializer(method: typevars.DeserializerWithType) -> typevars.DeserializerWithType:
    """
    A method decorator that marks it as the deserializer for that class. The class must be decorated with `serializable`.
    """
    setattr(method, DESERIALIZER_MARK, True)
    return method


def deserializer_for(cls: type) -> Callable[[typevars.Deserializer], typevars.Deserializer]:
    """
    A function decorator that sets it as the serializer for type `cls`.
    """

    def my_deserializer(method: typevars.Deserializer) -> typevars.Deserializer:
        set_deserializer(cls, method)
        return method

    return my_deserializer
