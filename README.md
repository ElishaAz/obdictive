# Obdictive

A python package for serializing objects to and from dictionaries and JSON strings using annotations.

This project uses class-level annotations (type hints) to define the variables a class has, and their type.

## Basic usage:

Create a class that derives from `Obdictive`:

```python
from obdictive import Obdictive


class Pet(Obdictive):
    name: str
    age: int


class Child(Obdictive):
    name: str
    pet: Pet
```

This creates two Obdictive subclasses.

1. Pet, with the following variables:
    - `name` with the type of `str` (string).
    - `age` with the type of `int`.
2. Child, with the following variables:
    - `name` with the type of `str` (string).
    - `pet` with the type of `Pet`.

To create an instance of these classes, pass in the values as named arguments:

```python
jimmy = Child(name="Jimmy", pet=Pet(name="Tiger", age=4))
```

### Serialization

Say we have the following dictionary: `{'name': 'Sarah', 'pet': {'name': 'Whiskers','age': 2}}`,
we can convert it to a `Child` object by calling:

```python
from obdictive import load

sarah = load(Child, {'name': 'Sarah', 'pet': {'name': 'Whiskers', 'age': 2}})
```

This will give us an instance of `Child` that is equivalent to:

```python
Child(name="Sarah", pet=Pet(name="Whiskers", age=2))
```

To convert a `Child` object to a dictionary, use `dump`:

```python
from obdictive import dump

jimmy = Child(name="Jimmy", pet=Pet(name="Tiger", age=4))
print(dump(jimmy))
# output:
# {'name': 'Jimmy', 'pet' :{'name': 'Tiger', 'age': 4}}
```

### JSON serialization

Similarly, `json_dumps` and `json_loads` can be used to serialize to and from JSON:

```python
from obdictive import json_dumps, json_loads

jimmy = Child(name="Jimmy", pet=Pet(name="Tiger", age=4))
print(json_dumps(jimmy))
# output:
# {"name": "Jimmy", "pet": {"name": "Tiger", "age": 4}}

sarah = json_loads(Child, '{"name": "Sarah", "pet": {"name": "Whiskers", "age": 2}}')
print(sarah == Child(name="Sarah", pet=Pet(name="Whiskers", age=2)))
# output:
# True
```

## Supported type annotations

`obdictive` supports the following types:

1. `bool, int, float, str`
2. `List[T]`, `Dict[T(key),T(value)]` and `Tuple[<list of Ts>]` where `T` is a supported type (including other lists,
   dicts or tuples).
    - Note: for `List[T]`, `Dict[K,V]` and `Tuple[...]`, I had to use implementation specific code (which means that it
      might not work on newer
      versions of python).
    - For compatibility, one can use `OList`, `ODict` and `OTuple` instead of `List`, `Dict` or `Tuple`.
3. Any subclass of `Obdictive`.
4. Classes with the `@serializable` decorator, with `@serializer` and `@deserializer` decorated functions.
5. Any type that is added manually using `obdictive.config.set_serializer` and `obdictive.config.set_deserializer`.

## Complex examples

### Custom serializer

Create a custom serializer for a `Point` class that stores its value as a `(x,y)` string:

```python
from obdictive import *


@serializable
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @serializer
    def _serializer(self):
        return F"({self.x},{self.y})"

    @classmethod
    @deserializer
    def _deserializer(cls, value: str):
        comma = value.index(',')
        x = float(value[1:comma])
        y = float(value[comma + 1:-1])
        return Point(x, y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# usage:
print(dump(Point(2, 6)))  # output: (2,6)
print(load(Point, "(7,3)") == Point(7, 3))  # output: True
```