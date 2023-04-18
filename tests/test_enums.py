import enum

from obdictive import serializable_enum, dump, load


@serializable_enum
class MyEnum(enum.Enum):
    ONE = 1
    TWO = "2"
    THREE = "Three"


def test_reserialize():
    for value in MyEnum:
        assert load(MyEnum, dump(value)) == value


def test_deserialize():
    assert load(MyEnum, 1) == MyEnum.ONE
    assert load(MyEnum, "2") == MyEnum.TWO
    assert load(MyEnum, "Three") == MyEnum.THREE
