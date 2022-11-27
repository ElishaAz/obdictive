from typing import TypeVar, Callable, Union, Dict, Any

Serializable_TypeVar = TypeVar('Serializable', bound=Union[int, float, str, dict, list, tuple, Any])
Serialized_TypeVar = TypeVar('Serialized', bound=Union[Dict[str, Any], Any])

Class_TypeVar = TypeVar('Class', bound=type)
Deserializer_TypeVar = TypeVar('Deserializer', bound=Callable[[Union[Dict[str, Any], Any]], Any])
Serializer_TypeVar = TypeVar('Serializer', bound=Callable[[Any], Union[Dict[str, Any], Any]])
