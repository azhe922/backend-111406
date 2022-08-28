from datetime import datetime as dt
import json
import datetime


def dict_to_json(data):
    return json.dumps(data)

def datetime_delta(dt, **kwargs):
    key = kwargs['key']
    value = kwargs['value']
    match key:
        case 'days':
            return dt + datetime.timedelta(days=value)
        case 'hours':
            return dt + datetime.timedelta(hours=value)
        case 'minutes':
            return dt + datetime.timedelta(minutes=value)
        case 'seconds':
            return dt + datetime.timedelta(seconds=value)
        case 'microseconds':
            return dt + datetime.timedelta(microseconds=value)

def datetime_strf(time):
    return dt.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
