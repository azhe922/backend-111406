from mongoengine import Document, StringField, EmailField, FloatField, IntField, EnumField

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
    |  birthday    | 出生年月日(西元) |  string  |
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
    | eth_sum      |    乙太坊金額    |   int    |
    """
    user_id = StringField(required=True, max_length=20)
    name = StringField(max_length=10)
    password = StringField(max_length=100)
    email = EmailField(required=True, max_length=100)
    height = FloatField(max_length=10)
    weight = FloatField(max_length=10)
    gender = EnumField(Gender, required=True, max_length=1)
    birthday = StringField(required=True, max_length=10)
    role = EnumField(UserRole, required=True, max_length=1)
    reference = StringField(max_length=20)
    create_time = IntField()
    update_time = IntField()
    eth_account = StringField(max_length=100)
    eth_password = StringField(max_length=100)
    eth_sum = IntField(min_value=0)
    # TODO 推薦人、個人身體狀況調查(高血壓、三酸肝等等)

    def to_json(self, *args, **kwargs):
        result = json.loads(super().to_json(*args, **kwargs))
        result.pop('password', None)
        result['gender'] = self.gender.description
        result['role'] = self.role.description
        # TODO 資料庫更新後即可刪除
        result['eth_sum'] = self.eth_sum or 0
        return result
