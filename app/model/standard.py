from mongoengine import Document, ListField, EnumField, IntField

from app.enums.training_part import TrainingPart
from app.enums.gender import Gender


class Standard(Document):
    """
    standard-肌力百分比常模資料

    | 欄位名稱 |   意義   | 資料型態 |
    |:--------:|:--------:|:--------:|
    |   part   |   肌力部位   |   int    |
    |   age    | 年齡範圍 |  array   |
    |  gender  |   性別   |   int    |
    |  times   | 次數範圍 |  array   |
    """
    part = EnumField(TrainingPart)
    gender = EnumField(Gender)
    times = ListField(IntField())
    age = ListField(IntField())
