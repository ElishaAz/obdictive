# mypy: disable-error-code="override,misc"
from __future__ import annotations

import sys
from typing import Union, overload, Generic, TypeVar

from .typevars import K, V, T, T1, T2

if sys.version_info >= (3, 9):
    from builtins import tuple as Tuple, dict as Dict, list as List, type as Type
else:
    # Legacy generic type annotation classes
    # Deprecated in Python 3.9
    from typing import List, Dict, Tuple, Type

from .decorators import serializer, deserializer
from .generics import _list_deserializer_impl, _dict_deserializer_impl, _tuple_deserializer_impl, _list_serializer_impl, \
    _dict_serializer_impl, _tuple_serializer_impl
from .obdictive_class import serializable
from . import typevars


def _full_name(cls):
    if cls.__module__ == 'builtins':
        return cls.__qualname__
    else:
        return F"{cls.__module__}.{cls.__qualname__}"


class _OMeta(type):  # type: ignore[misc]
    def __repr__(self):
        return self._my_repr


class OList(list, Generic[T]):
    _cache: Dict[type, Type[list]] = {}

    @classmethod
    def __class_getitem__(cls, single_type: Union[Type[typevars.T], Tuple[Type[typevars.T]]]) -> Type[List[typevars.T]]:
        if isinstance(single_type, tuple):
            if len(single_type) != 1:
                raise TypeError(f"Too many arguments for {cls.__qualname__}: actual {len(single_type)}, expected 1")
            single_type = single_type[0]

        if single_type in cls._cache:
            return cls._cache[single_type]

        @serializable(deep_search=True)
        class OListVar(OList, metaclass=_OMeta):
            _type = single_type
            _my_repr = F"{_full_name(cls)}[{_full_name(single_type)}]"
            pass

        cls._cache[single_type] = OListVar
        return OListVar

    @serializer
    def _serializer(self: list):  # self is 'list' NOT 'OList'!
        return _list_serializer_impl(self)

    @classmethod
    @deserializer
    def _deserializer(cls, value):
        if not hasattr(cls, '_type'):
            raise TypeError(F"{cls.__qualname__} cannot be used as a type annotation directly!")
        # noinspection PyUnresolvedReferences
        # As we just verified that type exists.
        return _list_deserializer_impl(value, cls._type)


class ODict(dict, Generic[K, V]):
    _cache: Dict[Tuple[type, type], Type[dict]] = {}

    @classmethod
    def __class_getitem__(cls, type_pair: Tuple[Type[typevars.K], Type[typevars.V]]) -> Type[
        Dict[typevars.K, typevars.V]]:
        if not isinstance(type_pair, tuple) or len(type_pair) != 2:
            length = 1 if not isinstance(type_pair, tuple) else len(type_pair)
            raise TypeError(f"Wrong number of arguments for {cls.__qualname__}: actual {length}, expected 2")

        if type_pair in cls._cache:
            return cls._cache[type_pair]

        @serializable(deep_search=True)
        class ODictVar(ODict, metaclass=_OMeta):
            _t_key = type_pair[0]
            _t_value = type_pair[1]
            _my_repr = F"{_full_name(cls)}[{_full_name(type_pair[0])}, {_full_name(type_pair[1])}]"
            pass

        cls._cache[type_pair] = ODictVar
        return ODictVar

    @serializer
    def _serializer(self: dict):  # self is 'dict' NOT 'ODict'!
        return _dict_serializer_impl(self)

    @classmethod
    @deserializer
    def _deserializer(cls, value):
        if not hasattr(cls, '_t_key') or not hasattr(cls, '_t_value'):
            raise TypeError(F"{cls.__qualname__} cannot be used as a type annotation directly!")
        # noinspection PyUnresolvedReferences
        # As we just verified that _t_key and _t_value exist.
        return _dict_deserializer_impl(value, (cls._t_key, cls._t_value))


class OTuple(tuple):
    _cache: Dict[Tuple[type, ...], Type[tuple]] = {}

    @overload
    def __class_getitem__(cls, types: Tuple[
        Type[typevars.T1]]) -> \
            Type[Tuple[typevars.T1]]:
        pass

    @overload
    def __class_getitem__(cls, types: Tuple[
        Type[typevars.T1], Type[typevars.T2]]) -> \
            Type[Tuple[typevars.T1, typevars.T2]]:
        pass

    @overload
    def __class_getitem__(cls, types: Tuple[
        Type[typevars.T1], Type[typevars.T2], Type[typevars.T3]]) -> \
            Type[Tuple[typevars.T1, typevars.T2, typevars.T3]]:
        pass

    @overload
    def __class_getitem__(cls, types: Tuple[
        Type[typevars.T1], Type[typevars.T2], Type[typevars.T3], Type[typevars.T4]]) -> \
            Type[Tuple[typevars.T1, typevars.T2, typevars.T3, typevars.T4]]:
        pass

    @overload
    def __class_getitem__(cls, types: Tuple[
        Type[typevars.T1], Type[typevars.T2], Type[typevars.T3], Type[typevars.T4], Type[typevars.T5]]) -> \
            Type[Tuple[typevars.T1, typevars.T2, typevars.T3, typevars.T4, typevars.T5]]:
        pass

    @overload
    def __class_getitem__(cls, types: Tuple[
        Type[typevars.T1], Type[typevars.T2], Type[typevars.T3], Type[typevars.T4], Type[typevars.T5], Type[
            typevars.T6]]) -> \
            Type[Tuple[typevars.T1, typevars.T2, typevars.T3, typevars.T4, typevars.T5, typevars.T6]]:
        pass

    @overload
    def __class_getitem__(cls, types: Tuple[
        Type[typevars.T1], Type[typevars.T2], Type[typevars.T3], Type[typevars.T4], Type[typevars.T5], Type[
            typevars.T6], Type[typevars.T7]]) -> \
            Type[Tuple[typevars.T1, typevars.T2, typevars.T3, typevars.T4, typevars.T5, typevars.T6, typevars.T7]]:
        pass

    @overload
    def __class_getitem__(cls, types: Tuple[
        Type[typevars.T1], Type[typevars.T2], Type[typevars.T3], Type[typevars.T4], Type[typevars.T5], Type[
            typevars.T6], Type[typevars.T7], Type[typevars.T8]]) -> \
            Type[Tuple[
                typevars.T1, typevars.T2, typevars.T3, typevars.T4, typevars.T5, typevars.T6, typevars.T7, typevars.T8]]:
        pass

    @classmethod
    def __class_getitem__(cls, types: Tuple[type, ...]) -> Type[tuple]:
        if not isinstance(types, tuple):
            types = (types,)

        if types in cls._cache:
            return cls._cache[types]

        @serializable(deep_search=True)
        class OTupleVar(OTuple, metaclass=_OMeta):
            _types = types
            _my_repr = F"{_full_name(cls)}[{', '.join(_full_name(t) for t in types)}]"
            pass

        cls._cache[types] = OTupleVar
        return OTupleVar

    @serializer
    def _serializer(self: tuple):  # self is 'tuple' NOT 'OTuple'!
        return _tuple_serializer_impl(self)

    @classmethod
    @deserializer
    def _deserializer(cls, value):
        if not hasattr(cls, '_types'):
            raise TypeError(F"{cls.__qualname__} cannot be used as a type annotation directly!")
        # noinspection PyUnresolvedReferences
        # As we just verified that _types exists
        return _tuple_deserializer_impl(value, *cls._types)
