"""
Serialization of python objects to dictionaries and JSON using annotations.
"""

__version__ = "0.1.0"
__author__ = 'Elisha Azaria'
__credits__ = 'Elisha Azaria'

from .obdictive_class import Obdictive, serializable
from .obdictive_enum import serializable_enum
from .dict_to_obj import load, deserializer, deserializer_for, set_deserializer
from .obj_to_dict import dump, serializer, serializer_for, set_serializer
from .special_types import OList, ODict, OTuple
from .json import json_dumps, json_loads
from . import config

del obdictive_class
del obdictive_enum
del dict_to_obj
del obj_to_dict
del special_types
del json
