from typing import Any, Dict, Callable, Union

from . import typevars, aliases


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


serializers_map: Dict[type, aliases.Serializer] = {
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


def dump(obj: aliases.Serializable) -> aliases.Serialized:
    """
    Convert an object to a dictionary.
    """
    if type(obj) in serializers_map:
        return serializers_map[type(obj)](obj)
    return None


def set_serializer(cls: type, method: aliases.Serializer) -> None:
    """
    Set `method` as the serializer for type `cls`.
    """
    serializers_map[cls] = method
