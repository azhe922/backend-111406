from mongoengine import Document, StringField, ListField, EmbeddedDocumentField
import json

from app.model.target_usertodo import UserTodo


class Target(Document):
    """
    target-運動目標

    |  欄位名稱  |             意義             | 資料型態 | 預設值 |
    |:----------:|:----------------------------:|:--------:|:------:|
    |     id     |           流水編號           |  string  |        |
    |  user_id   |          使用者帳號          |  string  |        |
    | start_date |         訓練開始時間         |  string  |        |
    |  end_date  |         訓練結束時間         |  string  |        |
    | user_todos  | 使用者在特定日期該達成的目標 |  array   |        |
    """
    user_id = StringField(required=True, max_length=20)
    start_date = StringField(required=True)
    end_date = StringField(required=True)
    user_todos = ListField(EmbeddedDocumentField(UserTodo))

    def to_json(self, *args, **kwargs):
        return json.loads(super().to_json(*args, **kwargs))
