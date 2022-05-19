from enum import Enum

class RecordType(Enum):
    training = 0, "訓練模式"
    examination = 1, "檢測模式"

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
