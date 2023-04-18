import enum
from typing import TypeVar, Callable

from . import aliases

Serializable = TypeVar('Serializable', bound=aliases.Serializable)
Serialized = TypeVar('Serialized', bound=aliases.Serialized)

Class = TypeVar('Class', bound=type)

Enum = TypeVar('Enum', bound=type[enum.Enum])

Deserializer = TypeVar('Deserializer', bound=aliases.Deserializer)
DeserializerWithType = TypeVar('DeserializerWithType',
                               bound=Callable[[type, aliases.Serializable], aliases.Serialized])
Serializer = TypeVar('Serializer', bound=aliases.Serializer)

K = TypeVar('K')
V = TypeVar('V')

T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')
T6 = TypeVar('T6')
T7 = TypeVar('T7')
T8 = TypeVar('T8')
