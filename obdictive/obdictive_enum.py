import enum
from typing import Callable

from .deserialization import set_deserializer
from . import aliases, typevars
from .serialization import set_serializer


def enum_serializer(self: enum.Enum) -> aliases.Serialized:
    return self.value


def create_enum_deserializer(cls: type) -> Callable[[aliases.Serialized], enum.Enum]:
    def enum_deserializer(value: aliases.Serialized) -> enum.Enum:
        return cls(value)

    return enum_deserializer


def serializable_enum(cls: typevars.Enum) -> typevars.Enum:
    if not issubclass(cls, enum.Enum):
        raise TypeError(F"{cls} must be a subclass of enum.Enum to use `serializable_enum` on it!")

    set_serializer(cls, enum_serializer)
    set_deserializer(cls, create_enum_deserializer(cls))

    return cls
