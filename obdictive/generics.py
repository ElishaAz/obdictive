from __future__ import annotations

import sys

from . import aliases
from .obdictive_exceptions import GenericSerializationException

if sys.version_info >= (3, 9):
    # noinspection PyPep8Naming
    from builtins import tuple as Tuple, dict as Dict, list as List, type as Type
else:
    # Legacy generic type annotation classes
    # Deprecated in Python 3.9
    from typing import List, Dict, Tuple, Type


def _list_serializer_impl(value: aliases.Serialized) -> list:
    from .serialization import dump
    try:
        return [dump(x) for x in value]
    except TypeError as e:
        raise GenericSerializationException(F"Unsupported type for list: {type(value)}") from e


def _list_deserializer_impl(value: list, types: aliases.GenericInstanceTypes) -> aliases.Serialized:
    from .deserialization import load
    if len(types) != 1:
        raise GenericSerializationException(F"List expected one type, but got {types}")
    return [load(types[0], x) for x in value]


def _dict_serializer_impl(value: aliases.Serialized) -> dict:
    from .serialization import dump
    try:
        return {dump(k): dump(v) for k, v in value.items()}
    except TypeError as e:
        raise GenericSerializationException(F"Unsupported type for dict: {type(value)}") from e


def _dict_deserializer_impl(value: dict, types: aliases.GenericInstanceTypes) -> aliases.Serialized:
    from .deserialization import load
    if len(types) != 2:
        raise GenericSerializationException(F"Dictionary expected two types (key, value), but got {types}")
    return {load(types[0], k): load(types[1], v) for k, v in value.items()}


def _tuple_serializer_impl(value: aliases.Serialized):
    from .serialization import dump
    try:
        return tuple(dump(v) for v in value)
    except TypeError as e:
        raise GenericSerializationException(F"Unsupported type for tuple: {type(value)}") from e


def _tuple_deserializer_impl(value: tuple, types: aliases.GenericInstanceTypes):
    from .deserialization import load
    return tuple(load(t, v) for t, v in zip(types, value))


generics_map: Dict[aliases.GenericInstance, Tuple[aliases.GenericType, aliases.GenericInstanceTypes]] = {
    # List[int]: (list, (int,))  # example
}

generic_serializers_map: Dict[aliases.GenericType, aliases.GenericSerializer] = {
    list: _list_serializer_impl,
    dict: _dict_serializer_impl,
    tuple: _tuple_serializer_impl,
}

generic_deserializers_map: Dict[aliases.GenericType, aliases.GenericDeserializer] = {
    list: _list_deserializer_impl,
    dict: _dict_deserializer_impl,
    tuple: _tuple_deserializer_impl,
}


def define_generic(instance: aliases.GenericInstance,
                   generic_class: aliases.GenericType,
                   types: aliases.GenericInstanceTypes):
    if instance not in generics_map:
        generics_map[instance] = (generic_class, types)
