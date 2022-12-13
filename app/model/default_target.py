from mongoengine import Document, StringField, ListField, BooleanField

class DefaultTarget(Document):
    user_id = StringField(max_length=20)
    target_times = ListField()
    valid = BooleanField(default=True)