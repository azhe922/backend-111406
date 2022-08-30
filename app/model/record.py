from mongoengine import Document, StringField, IntField, ListField, EnumField

from app.enums.training_part import TrainingPart
import json

class Record(Document):
    """
    record-測試紀錄

    |  欄位名稱   |    意義    | 資料型態 |
    |:-----------:|:----------:|:--------:|
    |     id      |  流水編號  |  string  |
    |   user_id   | 使用者帳號 |  string  |
    |   angles    |    角度    |   list   |
    | create_time |  紀錄時間  |  string  |
    |    times    |    次數    |   int    |
    |    fails     |  失敗次數  |   int    |
    |    part     |  肌力部位  |   int    |
    |     pr      |    PR值    |  string  |
    | test_result |  測試結果  |  string  |
    """
    user_id = StringField(required=True, max_length=20)
    part = EnumField(TrainingPart)
    times = IntField(required=True, max_length=3)
    angles = ListField(required=True, max_length=1024)
    fails = IntField(max_length=3)
    test_result = StringField(max_length=5)
    pr = IntField(max_length=3)
    create_time = IntField()

    def to_json(self, *args, **kwargs):
        result = json.loads(super().to_json(*args, **kwargs))
        result['part'] = self.part.description
        return result

