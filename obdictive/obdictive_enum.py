import enum

from .deserialization import set_deserializer
from .serialization import set_serializer


def enum_serializer(self):
    return self.value


def create_enum_deserializer(cls):
    def enum_deserializer(value):
        return cls(value)

    return enum_deserializer


def serializable_enum(cls):
    if not issubclass(cls, (enum.Enum, enum.IntEnum, enum.StrEnum)):
        raise TypeError(F"{cls} must be a subclass of enum.Enum to use `serializable_enum` on it!")

    set_serializer(cls, enum_serializer)
    set_deserializer(cls, create_enum_deserializer(cls))
