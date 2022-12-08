from typing import Dict, Any

from . import aliases
from .serialization import dump
from .deserialization import load

IGNORE_ANNOTATIONS = "_ignore_annot"
EDIT_ANNOTATIONS = "_edit_annot"
ADD_ANNOTATIONS = "_add_annot"
SET_ANNOTATIONS = "_annotations"


def _default_serializer(self: aliases.Serializable) -> dict:
    """
    Serializes an object to a dict based on its annotations.
    """
    d: Dict[str, Any] = dict()
    for name, cls in get_annotations(self.__class__).items():
        if hasattr(self, name):
            val = getattr(self, name)
            d[name] = dump(val)
    return d


def _default_deserializer(cls: type, value: dict) -> aliases.Serializable:
    """
    Deserializes a dict to the given class based on its annotations.
    The constructor must allow passing no arguments.
    """
    self = cls()

    annotations = get_annotations(cls)

    for name, cls in annotations.items():
        if name in value:
            value = value[name]
            loaded_value = load(cls, value)
            setattr(self, name, loaded_value)
        elif hasattr(self.__class__, name):
            setattr(self, name, getattr(self.__class__, name))

    return self


annotations_cache: Dict[type, dict] = {}


def get_annotations(cls: type, reload_cache=False) -> dict:
    global annotations_cache
    if cls in annotations_cache and not reload_cache:
        return annotations_cache[cls]

    annotations = {}
    for c in reversed(cls.mro()):
        annot = c.__dict__.get(SET_ANNOTATIONS, None) or c.__dict__.get(SET_ANNOTATIONS, {})
        ignore = c.__dict__.get(IGNORE_ANNOTATIONS, set())
        add = c.__dict__.get(ADD_ANNOTATIONS, {})
        edit = c.__dict__.get(EDIT_ANNOTATIONS, {})
        for k, v in annot.items():
            if k not in ignore:
                annotations[k] = v
        for k, v in add.items():
            if k not in annot:
                annotations[k] = v
        for k, v in edit.items():
            if k in annot:
                annotations[k] = v

    annotations_cache[cls] = annotations
    return annotations
