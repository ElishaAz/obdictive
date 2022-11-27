from typing import Tuple

import obdictive.dict_to_obj as dto


class ExampleClass:
    def __init__(self, i: int, s: str):
        self.i = i
        self.s = s

    def __eq__(self, other):
        return self.i == other.i and self.s == other.s

    def __repr__(self):
        return F"ExampleClass[i={self.i}, s={self.s}]"


@dto.deserializer_for(ExampleClass)
def ec_deserializer(val: dict):
    return ExampleClass(dto.load(int, val['i']), dto.load(str, val['s']))


def test__list_deserializer_impl():
    assert dto._list_deserializer_impl([1, 2, 3], int) == [1, 2, 3]
    assert dto._list_deserializer_impl([{'i': 1, 's': 'a'}, {'i': 2, 's': 'b'}, {'i': 3, 's': 'c'}], ExampleClass) == \
           [ExampleClass(1, 'a'), ExampleClass(2, 'b'), ExampleClass(3, 'c')]


def test__dict_deserializer_impl():
    assert dto._dict_deserializer_impl({'a': 1, 'b': 2, 'c': 3}, str, int) == {'a': 1, 'b': 2, 'c': 3}
    assert dto._dict_deserializer_impl({'a': {'i': 1, 's': 'a'}, 'b': {'i': 2, 's': 'b'}, 'c': {'i': 3, 's': 'c'}},
                                       str, ExampleClass) == \
           {'a': ExampleClass(1, 'a'), 'b': ExampleClass(2, 'b'), 'c': ExampleClass(3, 'c')}


def test__tuple_deserializer_impl():
    assert dto._tuple_deserializer_impl((1, 2, 3), int, int, int) == (1, 2, 3)
    assert dto._tuple_deserializer_impl(({'i': 1, 's': 'a'}, {'i': 2, 's': 'b'}, {'i': 3, 's': 'c'}),
                                        ExampleClass, ExampleClass, ExampleClass) == \
           (ExampleClass(1, 'a'), ExampleClass(2, 'b'), ExampleClass(3, 'c'))
    assert dto._tuple_deserializer_impl((1, 'a', {'i': 2, 's': 'b'}), int, str, ExampleClass) == \
           (1, 'a', ExampleClass(2, 'b'))


class ComplexExampleClass:
    def __init__(self, t: Tuple[int, str, ExampleClass], ec: ExampleClass):
        self.t = t
        self.ec = ec

    def __eq__(self, other):
        return self.t == other.t and self.ec == other.ec

    def __repr__(self):
        return F"ComplexExampleClass[t={self.t}, ec={self.ec}]"


dto.set_deserializer(Tuple[int, str, ExampleClass], lambda v: dto._tuple_deserializer_impl(v, int, str, ExampleClass))


@dto.deserializer_for(ComplexExampleClass)
def cec_deserializer(val: dict):
    return ComplexExampleClass(dto.load(Tuple[int, str, ExampleClass], val['t']),
                               dto.load(ExampleClass, val['ec']))


def test_load():
    assert dto.load(int, 1) == 1
    assert dto.load(str, 'a') == 'a'

    assert dto.load(ComplexExampleClass, {'t': (1, 'a', {'i': 2, 's': 'b'}), 'ec': {'i': 3, 's': 'c'}}) == \
           ComplexExampleClass((1, 'a', ExampleClass(2, 'b')), ExampleClass(3, 'c'))
