"""
Converting a dict to an object (deserialization).
"""
from __future__ import annotations

import sys
from typing import cast

if sys.version_info >= (3, 9):
    from builtins import tuple as Tuple, dict as Dict, list as List
else:
    # Legacy generic type annotation classes
    # Deprecated in Python 3.9
    # Remove once we no longer support Python 3.8 or lower
    from typing import List, Dict, Tuple

from . import config, aliases


def _list_deserializer_impl(value: list, t_item: type):
    return [load(t_item, x) for x in value]


def _dict_deserializer_impl(value: dict, t_key: type, t_value: type):
    return {load(t_key, k): load(t_value, v) for k, v in value.items()}


def _tuple_deserializer_impl(value: tuple, *types: type):
    return tuple(load(t, v) for t, v in zip(types, value))


# Deserializer = Callable[[Union[Dict[str, Any], Any]], Any]

deserializers_map: Dict[type, aliases.Deserializer] = {
    int: int,
    str: str,
    float: float,
    bool: bool,
}
"""
A dictionary that defines how a value can be deserialized to a specific type.
The `@deserializer` decorator adds to this dictionary.
"""


def load(cls: type, value: aliases.Serialized) -> aliases.Serializable:
    """
    Convert a dictionary back to a python object.

    :param cls: The type of the object.
    :param value: The dictionary.
    :return: An instance of type `cls` equivalent to `value`.
    """
    #                                          Special types in Python 3.7+                 Python 3.5-3.6
    if config.use_special_types_black_magic and not isinstance(cls, type) or \
            isinstance(cls, List) or isinstance(cls, Dict) or isinstance(cls, Tuple):  # type: ignore
        if hasattr(cls, '__origin__'):
            cls_cast = cast(List.__class__, cls)  # type: ignore[valid-type]
            if hasattr(cls_cast, '__extra__'):
                ty = cls_cast.__extra__  # type: ignore[attr-defined]
            else:
                ty = cls_cast.__origin__  # type: ignore[attr-defined]
            if ty == list:
                t_item = cls_cast.__args__[0]  # type: ignore[attr-defined]
                value_list = cast(list, value)
                return _list_deserializer_impl(value_list, t_item)
            if ty == dict:
                t_key, t_value = cls_cast.__args__[0:2]  # type: ignore[attr-defined]
                value_dict = cast(dict, value)
                return _dict_deserializer_impl(value_dict, t_key, t_value)
            if ty == tuple:
                types = cls_cast.__args__  # type: ignore[attr-defined]
                value_tuple = cast(tuple, value)
                return _tuple_deserializer_impl(value_tuple, *types)
        return value
    else:
        if cls in deserializers_map:
            return deserializers_map[cls](value)
        else:
            # for map_type, map_method in load_map.items():
            #     if issubclass(t, map_type):
            #         return map_method(value)
            raise TypeError(F"{value} is not of type {cls.__name__}, and cannot be converted")


def set_deserializer(cls: type, method: aliases.Deserializer) -> None:
    """
    Set `method` as the deserializer for type `cls`.
    """
    deserializers_map[cls] = method
