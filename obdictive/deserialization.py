"""
Converting a dict to an object (deserialization).
"""

from typing import Any, Dict, List, Union, Callable, TypeVar, Tuple

from . import config
from .type_vars import Deserializer_TypeVar, Serialized_TypeVar, Serializable_TypeVar


def _list_deserializer_impl(value: list, t_item: type):
    return [load(t_item, x) for x in value]


def _dict_deserializer_impl(value: dict, t_key: type, t_value: type):
    return {load(t_key, k): load(t_value, v) for k, v in value.items()}


def _tuple_deserializer_impl(value: tuple, *types: type):
    return tuple(load(t, v) for t, v in zip(types, value))


# Deserializer = Callable[[Union[Dict[str, Any], Any]], Any]

deserializers_map: Dict[type, Deserializer_TypeVar] = {
    int: int,
    str: str,
    float: float,
    bool: bool,
}
"""
A dictionary that defines how a value can be deserialized to a specific type.
The `@deserializer` decorator adds to this dictionary.
"""


def load(cls: type, value: Serialized_TypeVar) -> Serializable_TypeVar:
    """
    Convert a dictionary back to a python object.

    :param cls: The type of the object.
    :param value: The dictionary.
    :return: An instance of type `cls` equivalent to `value`.
    """
    #                                          Special types in Python 3.7+                 Python 3.5-3.6
    if config.use_special_types_black_magic and not isinstance(cls, type) or \
            isinstance(cls, List) or isinstance(cls, Dict) or isinstance(cls, Tuple):
        if hasattr(cls, '__origin__'):
            cls: List.__class__
            ty = cls.__extra__ if hasattr(cls, '__extra__') else cls.__origin__
            if ty == list:
                t_item = cls.__args__[0]
                value: list
                return _list_deserializer_impl(value, t_item)
            if ty == dict:
                t_key, t_value = cls.__args__[0:2]
                value: dict
                return _dict_deserializer_impl(value, t_key, t_value)
            if ty == tuple:
                types = cls.__args__
                value: tuple
                return _tuple_deserializer_impl(value, *types)
        return value
    else:
        if cls in deserializers_map:
            return deserializers_map[cls](value)
        else:
            # for map_type, map_method in load_map.items():
            #     if issubclass(t, map_type):
            #         return map_method(value)
            raise TypeError(F"{value} is not of type {cls.__name__}, and cannot be converted")


def set_deserializer(cls: type, method: Deserializer_TypeVar) -> None:
    """
    Set `method` as the deserializer for type `cls`.
    """
    deserializers_map[cls] = method
