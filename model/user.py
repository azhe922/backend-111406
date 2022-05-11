from mongoengine import Document, StringField, EmailField, FloatField, DateTimeField

class User(Document):
    user_id = StringField(required=True, max_length=20)
    password = StringField(required=True, max_length=100)
    email = EmailField(required=True, max_length=100)
    height = FloatField(required=True, max_length=10)
    weight = FloatField(required=True, max_length=10)
    sex = StringField(required=True, max_length=1)
    birthday = StringField(required=True, max_length=10)
    role = StringField(required=True, max_length=1)
    create_time = DateTimeField()
    update_time = DateTimeField()