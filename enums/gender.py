from enum import Enum

class Gender(Enum):
    male = 0, "男"
    female = 1, "女"

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: int, description: str = None):
        self._description_ = description

    # this makes sure that the description is read-only
    @property
    def description(self):
        return self._description_