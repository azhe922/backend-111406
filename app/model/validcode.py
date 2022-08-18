from mongoengine import Document, StringField, EmailField, IntField

class ValidCode(Document):
    email = EmailField(required=True, max_length=100)
    otp = StringField(required=True, max_length=6)
    create_time = IntField()