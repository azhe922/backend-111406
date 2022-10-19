from signal import default_int_handler
from mongoengine import EmbeddedDocument, StringField, ListField, BooleanField
import json


class UserTodo(EmbeddedDocument):
    """    
    user_todo-紀錄每周排定日期的訓練計劃

    |   欄位名稱   |     意義     | 資料型態 | 預設值 |
    |:------------:|:------------:|:--------:|:------:|
    | target_times |   目標次數   |  array   |        |
    | target_date  | 目標完成時間 |  string  |        |
    |   complete   |   完成與否   | boolean  | False  |
    | actual_times |   實際次數   |  array  |        |
    """
    target_times = ListField(required=True)
    target_date = StringField(required=True)
    complete = BooleanField(default=False)
    actual_times = ListField(default=[{
        'part': 0,
        'hand': 'left',
        'times': 0,
    },{
        'part': 0,
        'hand': 'right',
        'times': 0,
    },{
        'part': 1,
        'hand': 'left',
        'times': 0,
    },{
        'part': 1,
        'hand': 'right',
        'times': 0,
    }, {
        'part': 2,
        'times': 0
    }], max_length=5)

    def to_json(self, *args, **kwargs):
        return json.loads(super().to_json(*args, **kwargs))
