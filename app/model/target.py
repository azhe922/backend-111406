from mongoengine import Document, StringField, ListField
import json


class Target(Document):
    """
    target-運動目標

    |  欄位名稱  |             意義             | 資料型態 | 預設值 |
    |:----------:|:----------------------------:|:--------:|:------:|
    |     id     |           流水編號           |  string  |        |
    |  user_id   |          使用者帳號          |  string  |        |
    | start_date |         訓練開始時間         |  string  |        |
    |  end_date  |         訓練結束時間         |  string  |        |
    | user_todo  | 使用者在特定日期該達成的目標 |  array   |        |

    物件陣列 target.user_todo

    |   欄位名稱   |     意義     | 資料型態 | 預設值 |
    |:------------:|:------------:|:--------:|:------:|
    | target_times |   目標次數   |  array   |        |
    | target_date  | 目標完成時間 |  string  |        |
    |   complete   |   完成與否   | boolean  | False  |
    | actual_times |   實際次數   |  array  |        |
    """
    user_id = StringField(required=True, max_length=20)
    start_date = StringField(required=True)
    end_date = StringField(required=True)
    user_todo = ListField(required=True, max_length=1024)

    def to_json(self, *args, **kwargs):
        return json.loads(super().to_json(*args, **kwargs))
