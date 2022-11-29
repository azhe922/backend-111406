from mongoengine import Document, StringField, EmailField, FloatField, IntField, EnumField, DictField

from app.enums.user_role import UserRole
from app.enums.gender import Gender
import json


class User(Document):
    """
    user-使用者資料
    |   欄位名稱   |       意義       | 資料型態 |
    |:------------:|:----------------:|:--------:|
    |      id      |     流水編號     |  string  |
    |   user_id    |    使用者帳號    |  string  |
    |   birthday   | 出生年月日(西元) |  string  |
    |    email     |       信箱       |  string  |
    |    gender    |       性別       |   int    |
    |    height    |       身高       |  float   |
    |    weight    |       體重       |  float   |
    |     role     |       權限       |   int    |
    |   password   |    使用者密碼    |  string  |
    |     name     |       暱稱       |  string  |
    | create_time  |     建立時間     |   int    |
    | update_time  |     更新時間     |   int    |
    | eth_account  |    乙太坊帳號    |  string  |
    | eth_password |    乙太坊密碼    |  string  |
    |   eth_sum    |    乙太坊金額    |   int    |
    | institution  |    單位/機構     |  string  |
    | other_detail |     其他事項     |  string  |
    """
    user_id = StringField(required=True, max_length=20)
    name = StringField(max_length=10)
    password = StringField(max_length=100)
    email = EmailField(required=True, max_length=100)
    height = FloatField(max_length=10, max_value=200, min_value=130)
    weight = FloatField(max_length=10, max_value=150, min_value=30)
    gender = EnumField(Gender, required=True, max_length=1)
    birthday = StringField(required=True, max_length=10)
    role = EnumField(UserRole, required=True, max_length=1)
    reference = StringField(max_length=20)
    create_time = IntField()
    update_time = IntField()
    eth_account = StringField(max_length=100)
    eth_password = StringField(max_length=100)
    eth_sum = IntField(min_value=0)
    institution = StringField()
    other_detail = DictField()
    """ {
        "hasHypertension": boolean,
        "hasHyperglycemia": boolean,
        "hasHyperlipidemia": boolean,
        "hasExerciseHabits": boolean
        }"""

    def to_json(self, *args, **kwargs):
        result = json.loads(super().to_json(*args, **kwargs))
        result.pop('password', None)
        result['gender'] = self.gender.description
        result['role'] = self.role.description
        result['eth_sum'] = self.eth_sum or 0
        return result
