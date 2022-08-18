from mongoengine import Document, StringField, IntField, ListField, EnumField

from app.enums.training_part import TrainingPart

class Record(Document):
    user_id = StringField(required=True, max_length=20)
    part = EnumField(TrainingPart)
    times = IntField(required=True, max_length=3)
    angles = ListField(required=True, max_length=1024)
    create_time = IntField()