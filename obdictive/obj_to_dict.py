from typing import Any, Dict, Callable, Union

from obdictive.type_vars import Serializer_TypeVar, Serializable_TypeVar, Serialized_TypeVar


def echo(x): return x


def _list_serializer_impl(l: list):
    """
    List serializer implementation.
    """
    return [dump(i) for i in l]


def _dict_serializer_impl(d: dict):
    """
    Dictionary serializer implementation.
    """
    return {k: dump(v) for k, v in d.items()}


def _tuple_serializer_impl(t: tuple):
    """
    Tuple serializer implementation.
    """
    return tuple(dump(i) for i in t)


serializers_map: Dict[type, Serializer_TypeVar] = {
    int: echo,
    str: echo,
    float: echo,
    bool: echo,
    list: _list_serializer_impl,
    dict: _dict_serializer_impl,
    tuple: _tuple_serializer_impl,
}
"""
A dictionary that defines how an object can be serialized into a dict.
The `@serializer` decorator adds to this dictionary.
"""


def dump(obj: Serializable_TypeVar) -> Serialized_TypeVar:
    """
    Convert an object to a dictionary.
    """
    if type(obj) in serializers_map:
        return serializers_map[type(obj)](obj)


SERIALIZER_MARK = "is_obdictive_serializer"


def serializer(method: Serializer_TypeVar) -> Serializer_TypeVar:
    """
    A method decorator that marks it as the serializer for that class. The class must be decorated with `serializable`.
    """
    setattr(method, SERIALIZER_MARK, True)
    return method


def set_serializer(cls: type, method: Serializer_TypeVar) -> None:
    """
    Set `method` as the serializer for type `cls`.
    """
    serializers_map[cls] = method


def serializer_for(cls: type) -> Callable[[Serializer_TypeVar], Serializer_TypeVar]:
    """
    A function decorator that sets it as the serializer for type `cls`.
    """

    def my_serializer(method: Serializer_TypeVar) -> Serializer_TypeVar:
        set_serializer(cls, method)
        return method

    return my_serializer
