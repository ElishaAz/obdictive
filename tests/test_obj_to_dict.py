import obdictive.generics as og
import obdictive.serialization as otd
from obdictive.decorators import serializer_for


class ExampleClass:
    def __init__(self, i: int, f: float, s: str):
        self.i = i
        self.f = f
        self.s = s


def ec_serializer(ec: ExampleClass):
    return {'i': otd.dump(ec.i), 'f': otd.dump(ec.f), 's': otd.dump(ec.s)}


otd.set_serializer(ExampleClass, ec_serializer)


def test__list_serializer_impl():
    assert og._list_serializer_impl([1, 2, 3]) == [1, 2, 3]
    assert og._list_serializer_impl([ExampleClass(1, 2.2, '3'), ExampleClass(4, 5.5, '6')]) == \
           [{'i': 1, 'f': 2.2, 's': '3'}, {'i': 4, 'f': 5.5, 's': '6'}]


def test__dict_serializer_impl():
    assert og._dict_serializer_impl({'a': 1, 'b': 2}) == {'a': 1, 'b': 2}
    assert og._dict_serializer_impl({'a': ExampleClass(1, 2.2, '3')}) == {'a': {'i': 1, 'f': 2.2, 's': '3'}}


def test__tuple_serializer_impl():
    assert og._tuple_serializer_impl(('1', 2, 3.3)) == ('1', 2, 3.3)
    assert og._tuple_serializer_impl((1, '2', ExampleClass(3, 4.4, '5'))) == (1, '2', {'i': 3, 'f': 4.4, 's': '5'})


def test_dump():
    assert otd.dump(1) == 1
    assert otd.dump(2.2) == 2.2
    assert otd.dump('a') == 'a'

    assert otd.dump([1, 2, 3]) == [1, 2, 3]
    assert otd.dump({'a': 1, 'b': 2, 'c': 3}) == {'a': 1, 'b': 2, 'c': 3}
    assert otd.dump((1, 2.2, 'a')) == (1, 2.2, 'a')

    assert otd.dump(ExampleClass(1, 2.2, 'a')) == {'i': 1, 'f': 2.2, 's': 'a'}
    assert otd.dump(ExampleClass(3, 12345.6789, 'b')) == {'i': 3, 'f': 12345.6789, 's': 'b'}

    assert otd.dump(('a', 1, ['a', 'b', 'c', 'd', 'e'], {'a': 'A', 'b': 'B'})) == \
           ('a', 1, ['a', 'b', 'c', 'd', 'e'], {'a': 'A', 'b': 'B'})
    assert otd.dump([ExampleClass(1, 2.2, 'a'), ExampleClass(2, 3.3, 'b')]) == \
           [{'i': 1, 'f': 2.2, 's': 'a'}, {'i': 2, 'f': 3.3, 's': 'b'}]


class ComplexExampleClass:
    def __init__(self, t: tuple, l: list, ec: ExampleClass):
        self.t = t
        self.l = l
        self.ec = ec


def cec_serializer(cec: ComplexExampleClass):
    return {'t': otd.dump(cec.t), 'l': otd.dump(cec.l), 'ec': otd.dump(cec.ec)}


otd.set_serializer(ComplexExampleClass, cec_serializer)


def test_dump_complex():
    assert otd.dump(ComplexExampleClass((1, 2.2, 'a'), ['a', 'b', 'c'], ExampleClass(1, 2.2, ';'))) == \
           {'t': (1, 2.2, 'a'), 'l': ['a', 'b', 'c'], 'ec': {'i': 1, 'f': 2.2, 's': ';'}}


def test_serializer_for():
    orig = otd.serializers_map[int]

    @serializer_for(int)
    def serializer(i: int):
        return str(i)

    assert otd.serializers_map[int] is serializer
    assert otd.dump((1, 2, 3)) == ('1', '2', '3')

    otd.serializers_map[int] = orig
