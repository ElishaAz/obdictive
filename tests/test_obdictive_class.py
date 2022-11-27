import obdictive.dict_to_obj
import obdictive.obdictive_class as oc
import obdictive.obj_to_dict as otd
import obdictive.dict_to_obj as dto
from obdictive import *


@oc.serializable
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


def test_serializable():
    assert ExampleClass0 in otd.serializers_map
    assert ExampleClass0 in dto.deserializers_map

    # assert dump(ExampleClass0())
