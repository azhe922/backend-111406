from mongoengine import Document, StringField, IntField
from app.utils.backend_util import datetime_strf_YYYYmmddHHMMSS

import json

class LogRecord(Document):
    user_id = StringField(required=True, max_length=20)
    ip = StringField(required=True, max_length=20)
    message = StringField(required=True)
    request_url = StringField(required=True)
    action_time = IntField(required=True)

    def to_json(self, *args, **kwargs):
        result = json.loads(super().to_json(*args, **kwargs))
        result['action_time'] = datetime_strf_YYYYmmddHHMMSS(self.action_time)
        return result