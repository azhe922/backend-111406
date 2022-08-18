from mongoengine import Document, StringField, IntField, ListField, EnumField

from app.enums.training_part import TrainingPart

class Record(Document):
    user_id = StringField(required=True, max_length=20)
    part = EnumField(TrainingPart)
    times = IntField(required=True, max_length=3)
    angles = ListField(required=True, max_length=1024)
    fails = IntField(max_length=3)
    test_result = StringField(max_length=5)
    pr = IntField(max_length=3)
    create_time = IntField()