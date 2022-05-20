from mongoengine import Document, ListField, EnumField, IntField

from enums.training_part import TrainingPart
from enums.gender import Gender

class Standard(Document):
    part = EnumField(TrainingPart)
    gender = EnumField(Gender)
    times = ListField(IntField())
    age = ListField(IntField())