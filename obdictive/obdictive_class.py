"""
Obdictive class and class-oriented methods (serializable).
"""
from __future__ import annotations

import sys
from typing import Any

if sys.version_info >= (3, 9):
    from builtins import dict as Dict, list as List
else:
    # Legacy generic type annotation classes
    # Deprecated in Python 3.9
    from typing import List, Dict

from .serialization import dump
from .deserialization import load
from . import json, config
from .decorators import serializable, serializer, deserializer
from .default_serializers import get_annotations

_UNDEFINED = object()
"""An value that denotes that an attribute is not defined."""


@serializable
class Obdictive:
    """
    Derive from this class to create serializable classes easily.
    Declare the variables using annotations (type hints).

    The following methods will be implemented:

    - A constructor that takes in the variables as named arguments.
    - serializer and deserializer based on the variables in the annotations and their types.
    - __eq__ and __ne__ comparing the values of the variables in the annotations.
    - __hash__ hashing the values of the variables in the annotations. If any type errors arise, will use the standard hasher instead.
    - __str__ in the form of <class name>(<variable0>=<value0>, <variable1>=<value1>...).
    - __repr__ using `json_dumps`.

    Example:

    >>> from obdictive import *
    >>> class Pet(Obdictive):
    ...     name: str
    ...     age: int
    ...
    >>> class Child(Obdictive):
    ...     name: str
    ...     pet: Pet
    ...
    >>> sarah = Child(name="Sarah", pet=Pet(name="Whiskers", age=2))
    >>> dump(sarah)
    {'name': 'Sarah', 'pet': {'name': 'Whiskers', 'age': 2}}
    >>> john = load(Child, {'name': 'John', 'pet': {'name': 'Tiger', 'age': 4}})
    >>> john == Child(name="John", pet=Pet(name="Tiger", age=4))
    True
    >>> john == sarah
    False
    >>> hash(sarah)
    8753099804541
    >>> sarah.pet.age = 3
    >>> hash(sarah)
    8753099804583
    >>> str(sarah)
    'Child(name=Sarah, pet=Pet(age=3, name=Whiskers))'
    >>> repr(sarah)
    '{"name": "Sarah", "pet": {"name": "Whiskers", "age": 3}}'

    """

    def __init__(self, **kwargs):
        annotations = get_annotations(self.__class__)
        self.__class__._sorted_annotations = sorted(annotations.keys())

        for name, cls in annotations.items():
            if name in kwargs:  # argument is in keyword arguments
                value = kwargs[name]
                loaded_value = load(cls, value)
                setattr(self, name, loaded_value)
            elif hasattr(self.__class__, name):
                setattr(self, name, getattr(self.__class__, name))

    @serializer
    def _serializer(self) -> dict:
        d: Dict[str, Any] = dict()
        for name, cls in get_annotations(self.__class__).items():
            if hasattr(self, name):
                val = getattr(self, name)
                d[name] = dump(val)
        return d

    @classmethod
    @deserializer
    def _deserializer(cls, val):
        return cls(**val)

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """
        Applies the `@serializable` decorator to all subclasses
        :param kwargs:
        :return:
        """
        super().__init_subclass__(**kwargs)
        serializable(cls)

    def __eq__(self, o: object) -> bool:
        if o is None:
            return False
        if not isinstance(o, self.__class__):
            return False

        for name in get_annotations(self.__class__):
            if not (getattr(self, name, _UNDEFINED) == getattr(o, name, _UNDEFINED)):
                return False
        return True

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        if not config.hash_dict_class:
            return hash(self)
        try:
            return hash(getattr(self, x, _UNDEFINED) for x in _get_sorted_annotations(self.__class__))
        except TypeError:
            return hash(self)

    def __str__(self) -> str:
        attrs = []
        for name in _get_sorted_annotations(self.__class__):
            if hasattr(self, name):
                value = getattr(self, name)
                if isinstance(value, list) and config.use_custom_list_str:
                    value = _list_str(value)
                else:
                    value = str(value)
                attrs.append(F"{name}={value}")
        return F"{self.__class__.__name__}({', '.join(attrs)})"

    def __repr__(self) -> str:
        return json.json_dumps(self)


def _list_str(lst: list):
    str_list = []
    for item in lst:
        if isinstance(item, list):
            str_list.append(_list_str(item))
        else:
            str_list.append(str(item))
    return F"[{', '.join(str_list)}]"


_sorted_annotations_cache: Dict[type, List[str]] = {}


def _get_sorted_annotations(cls: type):
    global _sorted_annotations_cache
    if cls in _sorted_annotations_cache:
        return _sorted_annotations_cache[cls]
    sorted_annotations = sorted(get_annotations(cls).keys())
    _sorted_annotations_cache[cls] = sorted_annotations
    return sorted_annotations
