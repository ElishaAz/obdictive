from typing import List, Tuple

from obdictive import *


class TestInner(Obdictive):
    f: float
    name: str


class Test(Obdictive):
    i: int
    s: str
    ti: List[TestInner]


if __name__ == '__main__':
    assert load(int, "5") == 5

    test_str = '{ "i": 1, "s": "abc", "ti": [{"f": 1.5, "name": "Inner"}]}'

    t1 = json_loads(Test, test_str)
    t2 = Test(i=1, s="abc", ti=[TestInner(f=1.5, name="Inner")])

    assert t1 == t2
    assert str(t1) == "Test(i=1, s=abc, ti=[TestInner(f=1.5, name=Inner)])"
    assert str(t1) == str(t2)

    assert json_dumps(t2) == json_dumps(t2)
    assert json_loads(Test, json_dumps(t2)) == t2

    t = Tuple[int, str, float]

    i = t[0]

