from typing import TypeVar, Callable, Union, Dict, Any, Tuple

Serializable_TypeVar = TypeVar('Serializable', bound=Union[int, float, str, dict, list, tuple, Any])
Serialized_TypeVar = TypeVar('Serialized', bound=Union[Dict[str, Any], Any])

Class_TypeVar = TypeVar('Class', bound=type)

Deserializer_TypeVar = TypeVar('Deserializer', bound=Callable[[Union[Dict[str, Any], Any]], Any])
Serializer_TypeVar = TypeVar('Serializer', bound=Callable[[Any], Union[Dict[str, Any], Any]])

K = TypeVar('K', bound=type)
V = TypeVar('V', bound=type)

T = TypeVar('T', bound=type)
T1 = TypeVar('T1', bound=type)
T2 = TypeVar('T2', bound=type)
T3 = TypeVar('T3', bound=type)
T4 = TypeVar('T4', bound=type)
T5 = TypeVar('T5', bound=type)
T6 = TypeVar('T6', bound=type)
T7 = TypeVar('T7', bound=type)
T8 = TypeVar('T8', bound=type)

TupleOfTypes_TypeVar = TypeVar('Tuple of Types', bound=Tuple[type, ...])