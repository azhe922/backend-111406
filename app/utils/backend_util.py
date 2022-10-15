from datetime import datetime as dt
import json
import datetime
from mongoengine import connect
from mongoengine.connection import disconnect
from flask import current_app as app
from app.enums.deltatime_type import DeltaTimeType



def dict_to_json(data):
    return json.dumps(data)

def datetime_delta(dt, **kwargs):
    key = kwargs['key']
    value = kwargs['value']
    
    match key:
        case DeltaTimeType.days:
            return dt + datetime.timedelta(days=value)
        case DeltaTimeType.hours:
            return dt + datetime.timedelta(hours=value)
        case DeltaTimeType.minutes:
            return dt + datetime.timedelta(minutes=value)
        case DeltaTimeType.seconds:
            return dt + datetime.timedelta(seconds=value)
        case DeltaTimeType.microseconds:
            return dt + datetime.timedelta(microseconds=value)

def get_week(date):
    # turn sunday into 0, monday into 1, etc.
    day_idx = 0 - (date.weekday() % 7)
    sunday = datetime_delta(date, key=DeltaTimeType.days, value=day_idx)
    date = sunday
    for n in range(7):
        yield date
        date = datetime_delta(date, key=DeltaTimeType.days, value=1)

def datetime_strf(time):
    return dt.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

def init_db():    
    return connect(host=app.config["DB_HOST"])

def close_db():
    return disconnect()
