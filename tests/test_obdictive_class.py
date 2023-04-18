from obdictive import Obdictive, json_loads


class ExampleClass(Obdictive):
    i: int
    s: str


def test_deserialize():
    assert json_loads(ExampleClass, '{"i": 1, "s": "123"}') == ExampleClass(i=1, s="123")


if __name__ == '__main__':
    test_deserialize()
