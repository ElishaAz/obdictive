"""
Converting a dict to an object (deserialization).
"""
from __future__ import annotations

import sys

from .generics import _list_deserializer_impl, _dict_deserializer_impl, _tuple_deserializer_impl, generics_map, \
    generic_deserializers_map
from .obdictive_exceptions import ObdictiveDeserializationException

if sys.version_info >= (3, 9):
    # noinspection PyPep8Naming
    from builtins import tuple as Tuple, dict as Dict, list as List, type as Type
else:
    # Legacy generic type annotation classes
    # Deprecated in Python 3.9
    from typing import List, Dict, Tuple, Type
from typing import Any, cast

from . import config, aliases

deserializers_map: Dict[Type[Any], aliases.Deserializer] = {
    int: int,
    str: str,
    float: float,
    bool: bool,
}
"""
A dictionary that defines how a value can be deserialized to a specific type.
The `@deserializer` decorator adds to this dictionary.
"""


def load(cls: Type[Any], value: aliases.Serialized) -> aliases.Serializable:
    """
    Convert a dictionary back to a python object.

    :param cls: The type of the object.
    :param value: The dictionary.
    :return: An instance of type `cls` equivalent to `value`.
    """
    #                                          Special types in Python 3.7+                 Python 3.5-3.6
    if config.use_special_types_black_magic and not isinstance(cls, Type) or \
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
                return _dict_deserializer_impl(value_dict, (t_key, t_value))
            if ty == tuple:
                types = cls_cast.__args__  # type: ignore[attr-defined]
                value_tuple = cast(tuple, value)
                return _tuple_deserializer_impl(value_tuple, types)
        return value
    else:
        if cls in generics_map:
            base_cls, types = generics_map[cls]
            return generic_deserializers_map[base_cls](value, types)
        elif cls in deserializers_map:
            return deserializers_map[cls](value)
        else:
            # for map_type, map_method in load_map.items():
            #     if issubclass(t, map_type):
            #         return map_method(value)
            raise ObdictiveDeserializationException(F"{value} is not of type {cls.__name__}, and cannot be converted")


def set_deserializer(cls: type, method: aliases.Deserializer) -> None:
    """
    Set `method` as the deserializer for type `cls`.
    """
    deserializers_map[cls] = method
