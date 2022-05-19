from enum import Enum

class UserRole(Enum):
    normal = "N"
    "一般使用者"
    doctor = "D"
    "物理治療師"