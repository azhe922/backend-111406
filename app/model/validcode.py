from mongoengine import Document, StringField, EmailField, IntField


class ValidCode(Document):
    """
    valid_code-信箱驗證

    |  欄位名稱   |   意義   | 資料型態 |
    |:-----------:|:--------:|:--------:|
    |     id      | 流水編號 |  string  |
    |    email    |   信箱   |  string  |
    |     otp     |  驗證碼  |  string  |
    | create_time | 建立時間 |  int  |
    """
    email = EmailField(required=True, max_length=100)
    otp = StringField(required=True, max_length=6)
    create_time = IntField()
