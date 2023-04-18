import sys

if sys.version_info >= (3, 9):
    # noinspection PyPep8Naming
    from builtins import tuple as Tuple, dict as Dict, list as List, type as Type
    from collections.abc import Sequence
else:
    # Legacy generic type annotation classes
    # Deprecated in Python 3.9
    from typing import List, Dict, Tuple, Type, Sequence

from typing import Union, Any, Callable

Serializable = Union[int, float, str, dict, list, tuple, Any]
Serialized = Union[Dict[str, Any], Any]
Deserializer = Union[Callable[[Serializable], Serialized], Callable[[Any], Any]]
Serializer = Union[Callable[[Serializable], Serialized], Callable[[Any], Any]]

GenericType = Type[Any]
GenericInstanceTypes = Sequence[Type[Any]]
GenericInstance = Union[type, Any]
GenericDeserializer = Union[
    Callable[[Serializable, GenericInstanceTypes], Serialized], Callable[[Any, GenericInstanceTypes], Any]]
GenericSerializer = Union[
    Callable[[Serialized], Serializable], Callable[[Any], Any]]
