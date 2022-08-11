from mongoengine import Document, StringField, EmailField, FloatField, IntField, EnumField

from app.enums.user_role import UserRole
from app.enums.gender import Gender

class User(Document):
    user_id = StringField(required=True, max_length=20)
    password = StringField(required=True, max_length=100)
    email = EmailField(required=True, max_length=100)
    height = FloatField(max_length=10)
    weight = FloatField(max_length=10)
    gender = EnumField(Gender, required=True, max_length=1)
    birthday = StringField(required=True, max_length=10)
    role = EnumField(UserRole, required=True, max_length=1)
    create_time = IntField()
    update_time = IntField()