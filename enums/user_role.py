from enum import Enum

class UserRole(Enum):
    normal = "N", "一般使用者"
    doctor = "D", "物理治療師"

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: str, description: str = None):
        self._description_ = description

    # this makes sure that the description is read-only
    @property
    def description(self):
        return self._description_