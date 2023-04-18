from typing import Dict

from . import typevars, aliases
from .generics import generic_serializers_map


def echo(x: typevars.T) -> typevars.T: return x


serializers_map: Dict[type, aliases.Serializer] = {
    int: echo,
    str: echo,
    float: echo,
    bool: echo,
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

    elif type(obj) in generic_serializers_map:
        return generic_serializers_map[type(obj)](obj)
    return None


def set_serializer(cls: type, method: aliases.Serializer) -> None:
    """
    Set `method` as the serializer for type `cls`.
    """
    serializers_map[cls] = method
