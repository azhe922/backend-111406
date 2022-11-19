from mongoengine import Document, StringField, IntField


class UserLoginRecord(Document):
    """
    使用者登入資料
    """
    user_id = StringField(required=True, max_length=20)
    token = StringField(required=True)
    login_time = IntField(required=True)
    registration_token = StringField(default='')