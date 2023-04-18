from types import TracebackType


class ObdictiveException(Exception):
    """An exception in the obdictive module or any related code"""


class ObdictiveSerializationException(Exception):
    """An exception in obdictive serialization code"""


class ObdictiveDeserializationException(Exception):
    """An exception in obdictive deserialization code"""


class GenericSerializationException(ObdictiveSerializationException):
    """An exception in obdictive generic serialization code"""
