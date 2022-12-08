from typing import Union, Callable, overload

from .default_serializers import _default_serializer, _default_deserializer
from .deserialization import set_deserializer
from .serialization import set_serializer
from .type_vars import Class_TypeVar, Serializer_TypeVar, Deserializer_TypeVar


@overload
def serializable(*, serializer: Serializer_TypeVar = None, deserializer: Deserializer_TypeVar = None,
                 deep_search=False) -> Callable[[Class_TypeVar], Class_TypeVar]:
    pass


@overload
def serializable(cls: Class_TypeVar, *, serializer: Serializer_TypeVar = None,
                 deserializer: Deserializer_TypeVar = None,
                 deep_search=False) -> Class_TypeVar:
    pass


def serializable(cls: Class_TypeVar = None, *,
                 serializer: Serializer_TypeVar = None, deserializer: Deserializer_TypeVar = None,
                 deep_search=False) -> Union[Class_TypeVar, Callable[[Class_TypeVar], Class_TypeVar]]:
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

    def decorator(cls: Class_TypeVar) -> Class_TypeVar:
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

        set_serializer(cls, serializer)
        set_deserializer(cls, deserializer)

        return cls

    if cls is not None:
        return decorator(cls)
    return decorator


# ------------------------ Serializer ----------------------------------

SERIALIZER_MARK = "is_obdictive_serializer"


def serializer(method: Serializer_TypeVar) -> Serializer_TypeVar:
    """
    A method decorator that marks it as the serializer for that class. The class must be decorated with `serializable`.
    """
    setattr(method, SERIALIZER_MARK, True)
    return method


def serializer_for(cls: type) -> Callable[[Serializer_TypeVar], Serializer_TypeVar]:
    """
    A function decorator that sets it as the serializer for type `cls`.
    """

    def my_serializer(method: Serializer_TypeVar) -> Serializer_TypeVar:
        set_serializer(cls, method)
        return method

    return my_serializer


# ------------------------- Deserializer -----------------------


DESERIALIZER_MARK = "is_obdictive_deserializer"


def deserializer(method: Deserializer_TypeVar) -> Deserializer_TypeVar:
    """
    A method decorator that marks it as the deserializer for that class. The class must be decorated with `serializable`.
    """
    setattr(method, DESERIALIZER_MARK, True)
    return method


def deserializer_for(cls: type) -> Callable[[Deserializer_TypeVar], Deserializer_TypeVar]:
    """
    A function decorator that sets it as the serializer for type `cls`.
    """

    def my_deserializer(method: Deserializer_TypeVar) -> Deserializer_TypeVar:
        set_deserializer(cls, method)
        return method

    return my_deserializer
