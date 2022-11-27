"""
Configuration for the obdictive package
"""

use_special_types_black_magic: bool = True
"""Use black magic to serialize special types (Dict[str,T] and List[T])."""

hash_dict_class: bool = True
"""implement `__hash__` for `DictClass` based on the annotations."""
use_custom_list_str: bool = True
"""use a custom `str()` implementation for `list` (as the default calls `repr()` on the items instead of `str()`)."""

use_instance_annotations: bool = False
"""
Use the annotations of the instance, so that types can be set at runtime
(in a subclass's `__init__` before it calls `super().__init__()`).
E.g. storing the type of a list as a separate variable in the dictionary.
"""
