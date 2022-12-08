from typing import Union, Any, Dict, Callable

Serializable = Union[int, float, str, dict, list, tuple, Any]
Serialized = Union[Dict[str, Any], Any]
Deserializer = Union[Callable[[Serializable], Serialized], Callable[[Any], Any]]
Serializer = Union[Callable[[Serializable], Serialized], Callable[[Any], Any]]
