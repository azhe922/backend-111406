from mongoengine import Document, StringField, FloatField, ListField, DateTimeField, EnumField

from enums.training_part import TrainingPart
from enums.record_type import RecordType

class Record(Document):
    user_id = StringField(required=True, max_length=20)
    part = EnumField(TrainingPart)
    type = EnumField(RecordType)
    times = FloatField(required=True, max_length=10)
    angles = ListField(required=True, max_length=1024)
    create_time = DateTimeField()