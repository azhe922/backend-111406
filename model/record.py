from mongoengine import Document, StringField, FloatField, ListField, DateTimeField

class Record(Document):
    user_id = StringField(required=True, max_length=20)
    part = StringField(required=True, max_length=20)
    type = StringField(required=True, max_length=5)
    times = FloatField(required=True, max_length=10)
    angles = ListField(required=True, max_length=1024)
    create_time = DateTimeField()