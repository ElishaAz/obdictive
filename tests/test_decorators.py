import obdictive.deserialization as dto
import obdictive.serialization as otd
from obdictive import *


def test_serializable_marks():
    @serializable
    class ExampleClass0:
        def __init__(self, i: int, s: str):
            self.i = i
            self.s = s

        @serializer
        def _serializer(self):
            return {'i': dump(self.i), 's': dump(self.s)}

        @classmethod
        @deserializer
        def _deserializer(cls, value):
            return ExampleClass0(load(int, value['i']), load(str, value['s']))

    assert ExampleClass0 in otd.serializers_map
    assert ExampleClass0 in dto.deserializers_map


def test_serializable_variables():
    def _serializer(self):
        return {'i': dump(self.i), 's': dump(self.s)}

    def _deserializer(value):
        return ExampleClass1(load(int, value['i']), load(str, value['s']))

    @serializable(serializer=_serializer, deserializer=_deserializer)
    class ExampleClass1:
        def __init__(self, i: int, s: str):
            self.i = i
            self.s = s

    assert ExampleClass1 in otd.serializers_map
    assert ExampleClass1 in dto.deserializers_map

    assert otd.serializers_map[ExampleClass1] == _serializer
    assert dto.deserializers_map[ExampleClass1] == _deserializer

