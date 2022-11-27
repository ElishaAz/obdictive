"""
Obdictive class and class-oriented methods (serializable).
"""

from typing import Any, Dict, TypeVar

from . import dict_to_obj, obj_to_dict, json, config
from .dict_to_obj import DESERIALIZER_MARK
from .obj_to_dict import SERIALIZER_MARK
from .type_vars import Class_TypeVar

_UNDEFINED = object()
"""An value that denotes that an attribute is not defined."""


def serializable(cls: Class_TypeVar) -> Class_TypeVar:
    """
    A class decorator that sets the method marked with `@serializer` as the serializer and
    `@deserializer` as the deserializer for that class.
    """
    found_serializer = False
    found_deserializer = False
    for superclass in cls.mro():
        for name in superclass.__dict__:  # go over all the methods
            method = getattr(cls, name)
            if hasattr(method, SERIALIZER_MARK) and not found_serializer:  # if it is marked as the serializer
                obj_to_dict.set_serializer(cls, method)
                found_serializer = True
            elif hasattr(method, DESERIALIZER_MARK) and not found_deserializer:  # if it is marked as the deserializer
                dict_to_obj.set_deserializer(cls, method)
                found_deserializer = True
            if found_serializer and found_deserializer:
                return cls
    return cls


@serializable
class Obdictive:
    """
    Derive from this class to create serializable classes easily.
    Declare the variables using annotations (type hints).

    The following methods will be implemented:

    - A constructor that takes in the variables as named arguments.
    - serializer and deserializer based on the variables in the annotations and their types.
    - __eq__ and __ne__ comparing the values of the variables in the annotations.
    - __hash__ hashing the values of the variables in the annotations. If any errors arise, will use the standard hasher instead.
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
        annotations = _get_annotations(self)
        if config.use_instance_annotations:
            self.__annotations = annotations
            self.__sorted_annotations = sorted(annotations.keys())
        elif not hasattr(self.__class__, "__sorted_annotations"):
            self.__class__._sorted_annotations = sorted(annotations.keys())

        for name, cls in annotations.items():
            if name in kwargs:  # argument is in keyword arguments
                value = kwargs[name]
                value = dict_to_obj.load(cls, value)
                setattr(self, name, value)
            elif hasattr(self.__class__, name):
                setattr(self, name, getattr(self.__class__, name))

    @obj_to_dict.serializer
    def _serializer(self):
        d: Dict[str, Any] = dict()
        for name, cls in _get_annotations(self).items():
            if hasattr(self, name):
                val = getattr(self, name)
                d[name] = obj_to_dict.dump(val)
        return d

    @classmethod
    @dict_to_obj.deserializer
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

        for name in _get_annotations(self):
            if not (getattr(self, name, _UNDEFINED) == getattr(o, name, _UNDEFINED)):
                return False
        return True

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        if not config.hash_dict_class:
            return hash(self)
        try:
            return hash(getattr(self, x, _UNDEFINED) for x in _get_sorted_annotations(self))
        except:
            return hash(self)

    def __str__(self) -> str:
        attrs = []
        for name in _get_sorted_annotations(self):
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


def _list_str(l: list):
    str_list = []
    for item in l:
        if isinstance(item, list):
            str_list.append(_list_str(item))
        else:
            str_list.append(str(item))
    return F"[{', '.join(str_list)}]"


def _get_annotations(self):
    return self.__annotations if config.use_instance_annotations else self.__class__.__annotations__


def _get_sorted_annotations(self):
    return self.__sorted_annotations if config.use_instance_annotations else self.__class__._sorted_annotations
