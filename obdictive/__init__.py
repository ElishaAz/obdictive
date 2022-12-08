"""
Serialization of python objects to dictionaries and JSON using annotations.
"""

__version__ = "0.1.0"
__author__ = 'Elisha Azaria'
__credits__ = 'Elisha Azaria'

from .obdictive_class import Obdictive
from .obdictive_enum import serializable_enum
from .deserialization import load, set_deserializer
from .serialization import dump, set_serializer
from .decorators import serializable, serializer, deserializer, serializer_for, deserializer_for, \
    SERIALIZER_MARK, DESERIALIZER_MARK
from .special_types import OList, ODict, OTuple
from .json import json_dumps, json_loads
from . import config

del obdictive_class
del obdictive_enum
del dict_to_obj
del obj_to_dict
del decorators
del special_types
del json
