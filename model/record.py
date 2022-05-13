from mongoengine import Document, StringField, FloatField, ListField, DateTimeField, IntField

class Record(Document):
    user_id = StringField(required=True, max_length=20)
    part = IntField(required=True)
    type = IntField(required=True)
    times = FloatField(required=True, max_length=10)
    angles = ListField(required=True, max_length=1024)
    create_time = DateTimeField()